import numpy as np
from cython_functions import calculate_scatters, calculate_change_points


def calc_scatters(K):
    """
    Calculate scatter matrix:
    scatters[i,j] = {scatter of the sequence with starting frame i and ending frame j} 
    """
    n = K.shape[0]
    
    K1 = np.cumsum([0] + np.diag(K).tolist()) #13.4 us
    K2 = np.zeros((n+1, n+1))
    K2[1:, 1:] = np.cumsum(np.cumsum(K, 0), 1) #70.8 us
    scatters = calculate_scatters(K1, K2, n) # 6.64 ms
    return scatters

def cpd_nonlin(K, ncp, lmin=1, lmax=100000, backtrack=True, verbose=True,
    out_scatters=None):
    """ Change point detection with dynamic programming
    K - square kernel matrix 
    ncp - number of change points to detect (ncp >= 0)
    lmin - minimal length of a segment
    lmax - maximal length of a segment
    backtrack - when False - only evaluate objective scores (to save memory)
    
    Returns: (cps, obj)
        cps - detected array of change points: mean is thought to be constant on [ cps[i], cps[i+1] )    
        obj_vals - values of the objective function for 0..m changepoints
        
    """
    m = int(ncp) # prevent numpy.int64

    n, n1 = K.shape
    assert n == n1, "Kernel matrix awaited."

    assert n >= (m+1)*lmin
    assert n <= (m+1)*(lmax)
    assert lmax >= lmin >= 1

    if verbose:
        print("Precomputing scatters...")
    J = calc_scatters(K)

    if out_scatters != None:
        out_scatters[0] = J

    if verbose:
        print("Inferring best change points")

    I = 1e101 * np.zeros((m+1, n+1))
    # I[k, l] - value of the objective for k change-points and l first frames
    I[0, lmin:lmax] = J[0, lmin-1:lmax-1]

    if backtrack:
        # p[k, l] --- "previous change" --- best t[k] when t[k+1] equals l
        p = np.zeros((m+1, n+1), dtype=int)
    else:
        p = np.zeros((1,1), dtype=int)
        
    bt = int(1) if backtrack else int(0)

    calculate_change_points(m, n, I, J, lmin, lmax, p, bt)
    
    # Collect change points
    cps = np.zeros(m, dtype=int)
    
    if backtrack:
        cur = n
        for k in range(m, 0, -1):
            cps[k-1] = p[k, cur]
            cur = cps[k-1]

    scores = I[:, n].copy() 
    scores[scores > 1e99] = np.inf
    return cps, scores
    