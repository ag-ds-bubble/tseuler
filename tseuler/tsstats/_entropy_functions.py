import numpy as np

def ApproximateEntropry(U, m, r):
    try:
        def _maxdist(x_i, x_j):
            return max([abs(ua - va) for ua, va in zip(x_i, x_j)])

        def _phi(m):
            x = [[U[j] for j in range(i, i + m - 1 + 1)]
                    for i in range(N - m + 1)]
            C = [len([1 for x_j in x if _maxdist(x_i, x_j) <= r]) /
                    (N - m + 1.0) for x_i in x]
            _calc = (N - m + 1.0)**(-1) * sum(np.log(C))
            return _calc
        N = len(U)
        if N < 200:
            return abs(_phi(m+1) - _phi(m))
        else:
            return '--'
    except:
        return '--'

def SampleEntropy(U, m, r):
    try:
        def _maxdist(x_i, x_j):
            return max([abs(ua - va) for ua, va in zip(x_i, x_j)])

        def _phi(m):
            x = [[U[j] for j in range(i, i + m - 1 + 1)]
                    for i in range(N - m + 1)]
            C = [len([1 for j in range(len(x)) if i != j and _maxdist(
                x[i], x[j]) <= r]) for i in range(len(x))]
            return sum(C)
        
        N = len(U)
        if N < 200:
            return -np.log(_phi(m+1) / _phi(m))
        else:
            return '--'
    except:
        return '--'
