from time import time
import numpy as np
from scipy.sparse.linalg import eigs, spsolve

from pulse.processing.assembly import get_global_matrices, get_global_loads, get_all_matrices
from pulse.processing.assembly import get_prescribed_indexes, get_prescribed_values, get_unprescribed_indexes
# TODO: This code is a little messy, solve it as soon as possible
# TODO: Improve performance

def _reinsert_prescribed_dofs(solution, prescribed_indexes, prescribed_values):
    rows = solution.shape[0] + len(prescribed_indexes)
    cols = solution.shape[1]
    full_solution = np.zeros((rows, cols), dtype=complex)

    unprescribed_indexes = np.delete(np.arange(rows), prescribed_indexes)
    full_solution[unprescribed_indexes, :] = solution

    for i in range(cols):
        full_solution[prescribed_indexes, i] = prescribed_values 

    return full_solution


def get_combined_loads(mesh, frequencies, matrices, global_damping_values, lump_damping_values, is_viscous_lumped):

    F = get_global_loads(mesh, frequencies)
    
    unprescribed_indexes = get_unprescribed_indexes(mesh)
    prescribed_values = get_prescribed_values(mesh)

    alphaH_lump, betaH_lump, alphaV_lump, betaV_lump = lump_damping_values 
    alphaH, betaH, alphaV, betaV = global_damping_values

    if is_viscous_lumped:
        proportional_damping_lumped = False
    else:
        proportional_damping_lumped = True

    Kr, Mr, Kr_lump, Mr_lump, Cr_lump = matrices
    
    Kr = (Kr.toarray())[unprescribed_indexes, :]
    Mr = (Mr.toarray())[unprescribed_indexes, :]

    Kr_lump = (Kr_lump.toarray())[unprescribed_indexes, :]
    Mr_lump = (Mr_lump.toarray())[unprescribed_indexes, :]
    Cr_lump = (Cr_lump.toarray())[unprescribed_indexes, :]

    if Kr == [] or Mr == []:
        Kr_add = 0
        Mr_add = 0
    else:
        Kr_add = np.sum(Kr*prescribed_values, axis=1)
        Mr_add = np.sum(Mr*prescribed_values, axis=1)
    
    Kr_add_lump = np.sum(Kr_lump*prescribed_values, axis=1)
    Mr_add_lump = np.sum(Mr_lump*prescribed_values, axis=1)
    Cr_add_lump = np.sum(Cr_lump*prescribed_values, axis=1)

    rows = len(Kr_add)
    cols = len(frequencies)
    F_eq = np.zeros((rows,cols), dtype=complex)

    for i, freq in enumerate(frequencies):

        omega = 2*np.pi*freq

        F_Kadd = Kr_add + Kr_add_lump
        F_Madd = (-(omega**2))*(Mr_add + Mr_add_lump) 
        F_Cadd = 1j*((betaH + omega*betaV)*Kr_add + (alphaH + omega*alphaV)*Mr_add)

        if proportional_damping_lumped:
            F_Cadd_lump = 1j*((betaH_lump + omega*betaV_lump)*Kr_add_lump + (alphaH_lump + omega*alphaV_lump)*Mr_add_lump)
        else:
            F_Cadd_lump = 1j*omega*Cr_add_lump

        F_eq[:, i] = F_Kadd + F_Madd + F_Cadd + F_Cadd_lump

    F_combined = F - F_eq
    
    return F_combined


def modal_analysis(mesh, K=[], M=[], modes=20, which='LM', sigma=0.01, harmonic_analysis=False):

    prescribed_indexes = get_prescribed_indexes(mesh)
    prescribed_values = get_prescribed_values(mesh)

    if K==[] and M==[]:
        Kadd_lump, Madd_lump, _, _, _, _, _, _, _, _, _, _, _ = get_all_matrices(mesh)
    else:
        Kadd_lump = K
        Madd_lump = M
    
    eigen_values, eigen_vectors = eigs(Kadd_lump, M=Madd_lump, k=modes, which=which, sigma=sigma)

    positive_real = np.absolute(np.real(eigen_values))
    natural_frequencies = np.sqrt(positive_real)/(2*np.pi)
    modal_shape = np.real(eigen_vectors)

    index_order = np.argsort(natural_frequencies)
    natural_frequencies = natural_frequencies[index_order]
    modal_shape = modal_shape[:, index_order]

    if not harmonic_analysis:

        modal_shape = _reinsert_prescribed_dofs( modal_shape, prescribed_indexes, prescribed_values )

    return natural_frequencies, modal_shape


def direct_method(mesh, frequencies, global_damping_values=(0,0,0,0), lump_damping_values=(0,0,0,0), is_viscous_lumped=False):

    """ 
        Perform an harmonic analysis through direct method and returns the response of
        all nodes due the external or internal equivalent load. It has been implemented two
        different damping models: Viscous Proportional and Hysteretic Proportional
        Entries for Viscous Proportional Model Damping: (alpha_v, beta_v)
        Entries for Hyteretic Proportional Model Damping: (alpha_h, beta_h)
    """

    prescribed_indexes = get_prescribed_indexes(mesh)
    prescribed_values = get_prescribed_values(mesh)

    alphaH, betaH, alphaV, betaV = global_damping_values
    alphaH_lump, betaH_lump, alphaV_lump, betaV_lump = lump_damping_values

    if is_viscous_lumped:
        proportional_damping_lumped = False
    else:
        proportional_damping_lumped = True
    
    Kadd_lump, Madd_lump, K, M, Kr, Mr, K_lump, M_lump, C_lump, Kr_lump, Mr_lump, Cr_lump, _ = get_all_matrices(mesh)

    def matrices(Kr=Kr, Mr=Mr, Kr_lump=Kr_lump, Mr_lump=Mr_lump, Cr_lump=Cr_lump):
        return Kr, Mr, Kr_lump, Mr_lump, Cr_lump
    
    F = get_combined_loads(mesh, frequencies, matrices(), global_damping_values, lump_damping_values, is_viscous_lumped)

    rows = K.shape[0]
    cols = len(frequencies)
    solution = np.zeros((rows, cols), dtype=complex)

    alphaH, betaH, alphaV, betaV = global_damping_values
  
    for i, freq in enumerate(frequencies):

        omega = 2*np.pi*freq
        
        F_K = Kadd_lump
        F_M =  (-(omega**2))*Madd_lump
        F_C = 1j*(( betaH + omega*betaV )*K + ( alphaH + omega*alphaV )*M)

        if is_viscous_lumped:
            F_Clump = 1j*omega*C_lump
        
        if proportional_damping_lumped:
            F_Clump = 1j*(( betaH_lump + omega*betaV_lump )*K_lump + ( alphaH_lump + omega*alphaV_lump )*M_lump)

        A = F_K + F_M + F_C + F_Clump
        solution[:,i] = spsolve(A, F[:,i])

    solution = _reinsert_prescribed_dofs(solution, prescribed_indexes, prescribed_values)

    return solution

def modal_superposition(mesh, frequencies, modes, F_loaded=None, global_damping_values=(0,0,0,0), lump_damping_values=(0,0,0,0), fastest=True):
    
    """ 
        Perform an harmonic analysis through superposition method and returns the response of
        all nodes due the external or internal equivalent load. It has been implemented two
        different damping models: Viscous Proportional and Hysteretic Proportional
        Entries for Viscous Proportional Model Damping: (alpha_v, beta_v)
        Entries for Hyteretic Proportional Model Damping: (alpha_h, beta_h)
    """
    alphaH, betaH, alphaV, betaV = global_damping_values
    prescribed_indexes = get_prescribed_indexes(mesh)
    prescribed_values = get_prescribed_values(mesh)

    if np.sum(prescribed_values)>0:
        print("Warning: The Harmonic Analysis of prescribed DOF's problems had been solved through the Direct Method!")
        solution = direct_method(mesh, frequencies, global_damping_values=global_damping_values, lump_damping_values=lump_damping_values)
        return solution
    else:
        F = get_global_loads(mesh, frequencies, loads_matrix3D=fastest)
        Kadd_lump, Madd_lump, _, _, _, _, _, _, _, _, _, _, flag_Clump = get_all_matrices(mesh)

    #TODO: in the future version implement lets F_loaded operational

    natural_frequencies, modal_shape = modal_analysis(mesh, K=Kadd_lump, M=Madd_lump, modes=modes, harmonic_analysis=True)
    rows = Kadd_lump.shape[0]
    cols = len(frequencies)

    if fastest:    
    
        number_modes = len(natural_frequencies)
        omega = 2*np.pi*frequencies.reshape(cols,1,1)
        omega_n = 2*np.pi*natural_frequencies
        F_kg = (omega_n**2)
        F_mg =  - (omega**2)
        F_cg = 1j*((betaH + betaV*omega)*(omega_n**2) + (alphaH + omega*alphaV)) 
        diag = np.divide(1, (F_kg + F_mg + F_cg))*np.eye(number_modes)
        F_aux = modal_shape.T @ F
        solution = modal_shape @ (diag @ F_aux)
        solution = solution.reshape(cols, rows).T
    
    else:
      
        solution = np.zeros((rows, cols), dtype=complex)
        F_aux = modal_shape.T @ F
        omega_n = 2*np.pi*natural_frequencies
        F_kg = (omega_n**2)

        for i, freq in enumerate(frequencies):

            omega = 2*np.pi*freq
            F_mg =  - (omega**2)
            F_cg = 1j*((betaH + betaV*omega)*(omega_n**2) + (alphaH + omega*alphaV)) 
            data = np.divide(1, (F_kg + F_mg + F_cg))
            diag = np.diag(data)
            solution[:,i] = modal_shape @ (diag @ F_aux[:,i])

    solution = _reinsert_prescribed_dofs(solution, prescribed_indexes, prescribed_values)

    if flag_Clump:
            print("WARNING: There are external dampers connecting nodes to the ground. The damping, treated as \n" +  
            "         a viscous non-proportional model, will be ignored in mode superposition. It's recommended \n" +
            "         to solve the harmonic analysis through direct method if you want to get more accurate results!")

    return solution

def get_reactions_at_fixed_nodes(mesh, frequencies, U, global_damping_values=(0,0,0,0)):
    ''' This method returns reaction forces/moments at fixed points.
        load_reactions = [lines=frequencies; columns=reactions_at_node]'''

    alphaH, betaH, alphaV, betaV = global_damping_values
    _, _, Kr, Mr = get_global_matrices(mesh)

    if not U==[]:    

        if Kr == [] or Mr == []:

            Kr_U, Mr_U = 0, 0

        else:

            Kr = Kr.toarray()
            Mr = Mr.toarray()
            rows, cols = len(frequencies), Kr.shape[1] 
                        
            load_reactions = np.zeros( (rows, cols+1), dtype=complex )
            load_reactions[:,0] = frequencies
            U_t = U.T

            Kr_U = U_t@Kr
            Mr_U = U_t@Mr
        
        omega = 2*np.pi*frequencies
        omega = omega.reshape(rows,1)
        F_K = Kr_U
        F_M = -(omega**2)*Mr_U
        F_C = 1j*(betaH + omega*betaV)*Kr_U + (alphaH + omega*alphaV)*Mr_U
        load_reactions[:, 1:] = F_K + F_M + F_C

    else:
        load_reactions = []
    return load_reactions        
