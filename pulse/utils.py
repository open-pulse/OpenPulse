'''
utils
=====

Utils module provides a bunch of general utility functions and classes 
that may be usefull for some applications.

'''


from functools import wraps
from time import time

def split_sequence(sequence, size):
    '''
    Function used to divide a sequence in a list of sequences with given size.


    PARAMETERS
    ----------
    sequence : list, tuple, np.ndarray, and other array like objects
    size: int


    RETURNS
    -------
    subsequences : list


    EXAMPLE
    --------
    >>> sequence = [1, 2, 3, 4, 5, 6]
    >>> split_sequence(sequence, 2)
    [[1,2], [3,4], [5,6]]
    '''

    subsequences = []
    for start in range(0, len(sequence), size):
        end = start + size
        subsequence = sequence[start:end]
        subsequences.append(subsequence)
    return subsequences


def slicer(iterable, argument):
    '''
    Function used to create a custom slice of an iterable.

    PARAMETERS
    ----------
    iterable : any iterable object
    argument : can be a list of indexes, integer index, or string 'all'


    YELDS
    -----
    value of iterable in given indexes


    EXAMPLE
    -------
    >>> sequence = ['a', 'b', 'c', 'd']
    >>> for i in slicer(sequence, [1,2]):
    ...     print(i)
    ... 
    'b'
    'c'
    >>> for i in slicer(sequence, 'all'):
    ...     print(i)
    ... 
    'a'
    'b'
    'c'
    'd'
    '''

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
    '''
    Decorator to calculate the time taken for a function to run.
    

    EXAMPLE
    -------
    >>> @timer
    ... def foo():
    ...     print('foo')
    ...
    >>> foo()
    foo
    Time to finish foo: 0.0 [s]
    '''
    @wraps(function)
    def wrapper(*args, **kwargs):
        start_time = time()
        values = function(*args, **kwargs)
        end_time = time()
        print(f'Time to finish {function.__name__}: {end_time - start_time} [s]')
        return values
    return wrapper
    

def m_to_mm(m):
    '''
    Simple function to convert meters to milimeters.
    

    PARAMETERS
    ----------
    m : int, float


    RETURNS
    -------
    mm : float

    EXAMPLE
    -------
    >>> m_to_mm(7)
    7000
    '''
    return float(m) * 1000

def mm_to_m(mm):
    '''
    Simple function to convert meters to milimeters.
    

    PARAMETERS
    ----------
    mm : int, float


    RETURNS
    -------
    m : float


    EXAMPLE
    -------
    >>> mm_to_m(7000)
    7
    '''
    return float(mm) / 1000