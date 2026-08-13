import numpy as np
from scipy.sparse import random, csc_matrix
from scipy.sparse.linalg import eigs, LinearOperator
from tqdm import tqdm
from pypardiso import PyPardisoSolver

# 1. Simulação das suas matrizes (Substitua pelas suas matrizes reais)
N = 10000
# K e M precisam estar no formato CSR ou CSC para o PyPardiso
K = random(N, N, density=0.005, format='csr') * 1000
M = random(N, N, density=0.001, format='csr') * 10

# 2. Definição do Alvo (Shift). 
# Geralmente queremos os primeiros modos físicos (frequências mais baixas), 
# então buscamos os modos mais próximos de zero (sigma = 0).
sigma = 0.0

# Matriz que será fatorada: (K - sigma * M). Se sigma=0, é a própria rigidez K.
Matriz_Fatorada = K - sigma * M

# 3. Inicializando e Fatorando com PyPardiso (Uma única vez)
solver = PyPardisoSolver()
solver.factorize(Matriz_Fatorada)

# 4. Configuração da barra de progresso
k_desejado = 100
max_iteracoes = 300
ncv = 2 * k_desejado + 1
total_solves_estimado = max_iteracoes * (ncv - k_desejado) / k_desejado

pbar = tqdm(total=total_solves_estimado, desc="Calculando Modos Vibracionais", unit="it")

# 5. O Operador Linear Customizado para K e M
# Para o problema generalizado, a operação por iteração deve ser: (K - sigma*M)^-1 * (M * v)
def op_generalized_inverse(v):
    pbar.update(1)
    
    # Passo A: Multiplica o vetor do ARPACK pela matriz de Massa
    M_v = M.dot(v)
    
    # Passo B: Resolve o sistema linear usando a rigidez fatorada pelo PyPardiso
    solucao = solver.solve(Matriz_Fatorada, M_v)
    
    return solucao

OP_custom = LinearOperator(shape=K.shape, matvec=op_generalized_inverse, dtype=K.dtype)

# 6. Execução do eigs
try:
    # PASSAMOS OP_custom, sigma=None (pois o shift já está embutido na fatoração),
    # e 'LM' para pegar as maiores magnitudes do operador inverso (menores frequências reais).
    autovalores_inv, autovetores = eigs(OP_custom, k=k_desejado, which='LM', maxiter=max_iteracoes)
    
    # 7. Convertendo os autovalores de volta para a física do problema
    # lambda_físico = (1 / lambda_operador) + sigma
    autovalores_reais = (1.0 / autovalores_inv) + sigma
    
    # Extraindo as frequências naturais em Hertz: f = sqrt(lambda) / (2 * pi)
    # (Evitando erros se houver resíduos numéricos complexos insignificantes usando .real)
    frequencias_hz = np.sqrt(np.abs(autovalores_reais.real)) / (2 * np.pi)
    
    print("\n\n=== RESULTADOS ENCONTRADOS ===")
    for i, f in enumerate(frequencias_hz):
        print(f"Modo {i+1}: {f:.4f} Hz")

except Exception as e:
    print(f"\nErro durante a resolução: {e}")
finally:
    pbar.close()