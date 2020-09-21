from functools import wraps
from time import time
from scipy.sparse import issparse
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
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
    setWindowFlags(Qt.WindowStaysOnTopHint)
    setWindowModality(Qt.WindowModal)
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setText(msg)
    msg_box.setWindowTitle(title)
    msg_box.exec_()

def remove_bc_from_file(entries_typed, path, key_strings, message):

    try:
        bc_removed = False
        config = configparser.ConfigParser()
        config.read(path)

        for entry in entries_typed: 
            entry_id = str(entry)

            if entry_id in config.sections():
                keys = list(config[entry_id].keys())
                for str_key in key_strings:
                    if str_key in keys:
                        # print("delete {} at entry {}".format(str_key, entry_id))
                        config.remove_option(section=entry_id, option=str_key)
                        if list(config[entry_id].keys())==[]:
                            config.remove_section(entry_id)
                        bc_removed = True

        with open(path, 'w') as config_file:
            config.write(config_file)

        if message is not None and bc_removed:
            info_messages(message)

    except Exception as e:
        error(str(e))

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