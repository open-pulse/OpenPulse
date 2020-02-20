def split_sequence(sequence, size):
    subsequences = []
    for start in range(0, len(sequence), size):
        end = start + size
        subsequence = sequence[start:end]
        subsequences.append(subsequence)
    return subsequences

def m_to_mm(m):
    return float(m) * 1000

def mm_to_m(mm):
    return float(mm) / 1000