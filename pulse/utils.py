from functools import wraps
from time import time
from scipy.sparse import issparse
from PyQt5.QtWidgets import QMessageBox
import configparser

def split_sequence(sequence, size):
    subsequences = []
    for start in range(0, len(sequence), size):
        end = start + size
        subsequence = sequence[start:end]
        subsequences.append(subsequence)
    return subsequences

def slicer(iterable, argument):
    if isinstance(argument, str) and argument == 'all':
        if isinstance(iterable, dict):
            for i in iterable.values():
                yield i 
        else:
            for i in iterable:
                yield i 

    elif isinstance(argument, int):
        yield iterable[argument]
    
    elif hasattr(argument, '__iter__'):
        # print("entrada 3")
        for i in argument:
            yield iterable[i]
            
    else:
        raise AttributeError('Argument not supported')

def timer(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        start_time = time()
        values = function(*args, **kwargs)
        end_time = time()
        print(f'Time to finish {function.__name__}: {end_time - start_time} [s]')
        return values
    return wrapper
    
def m_to_mm(m):
    return float(m) * 1000

def mm_to_m(mm):
    return float(mm) / 1000

def error( msg, title = " ERROR "):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setText(msg)
    msg_box.setWindowTitle(title)
    msg_box.exec_()

def info_messages(msg, title = " INFORMATION "):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setText(msg)
    msg_box.setWindowTitle(title)
    msg_box.exec_()

def remove_bc_from_file(nodes_typed, path, key_strings, message):

    try:

        _bc_list = configparser.ConfigParser()
        _bc_list.read(path)

        for node in nodes_typed:
    
            node_id = str(node)
            if not node_id in _bc_list.sections():
                return
            keys = list(_bc_list[node_id].keys())

            for str_key in key_strings:
                if str_key in keys:
                    # print("delete: {}".format(str_key))
                    _bc_list.remove_option(section=node_id, option=str_key)
                    
            if list(_bc_list[node_id].keys())==[]:
                _bc_list.remove_section(node_id)

            with open(path, 'w') as configfile:
                _bc_list.write(configfile)

        if message is not None:
            info_messages(message)

    except Exception as e:
        error(str(e))

def write_file_inside_project_folder(path, config):
        with open(path, 'w') as configfile:
            config.write(configfile)

def isInteger(value):
    try:
        int(value)
        return True
    except:
        return False

def isFloat(value):
    try:
        float(value)
        return True
    except:
        return False

def getColorRGB(color):
    temp = color[1:-1] #Remove "[ ]"
    tokens = temp.split(',')
    return list(map(int, tokens))

def sparse_is_equal(a, b):
    if not (issparse(a) and issparse(b)):
        raise TypeError('a and b should be sparse matrices')

    diference = a != b
    if isinstance(diference, bool):
        return not diference

    if issparse(diference):
        return diference.nnz == 0