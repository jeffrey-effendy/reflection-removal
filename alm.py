__all__ = ["alm"]

import time
import fbpca
import logging
logger = logging.getLogger(__name__)
import numpy as np
from scipy.sparse.linalg import svds

def alm(M, delta=1e-6, mu=None, maxiter=500, verbose=False, missing_data=True,
        svd_method="approximate", **svd_args):
    # Check the SVD method.
    allowed_methods = ["approximate", "exact", "sparse"]
    if svd_method not in allowed_methods:
        raise ValueError("'svd_method' must be one of: {0}"
                         .format(allowed_methods))

    # Check for missing data.
    shape = M.shape
    if missing_data:
        missing = ~(np.isfinite(M))
        if np.any(missing):
            M = np.array(M)
            M[missing] = 0.0
    else:
        missing = np.zeros_like(M, dtype=bool)
        if not np.all(np.isfinite(M)):
            logger.warn("The matrix has non-finite entries. "
                         "SVD will probably fail.")

    # Initialize the tuning parameters.
    lam = 1.0 / np.sqrt(np.max(shape))
    rho = 6
    if mu is None:
        mu = 0.5 / np.linalg.norm(M)
        if verbose:
            logger.info("mu = {0}".format(mu))

    # Convergence criterion.
    norm = np.linalg.norm(M)

    # Iterate.
    i = 0
    rank = np.min(shape)
    B = np.zeros(shape) 
    F = np.zeros(shape)

    dual_norm = lambda X: max(np.linalg.norm(X), np.linalg.norm(X, np.inf) / lam)
    Y = np.sign(M) / dual_norm(np.sign(M))

    # Convergence variable
    converged = False

    while i < max(maxiter, 1) and not converged:
        # SVD step.
        strt = time.time()
        
        primal_converged = False
        svd_time = time.time() - strt
        
        while not primal_converged:
            B_temp = B
            F_temp = F
            u, s, v = np.linalg.svd(M - F + Y / mu, full_matrices=False)
            
            s = shrink(s, 1./mu)
            rank = np.sum(s > 0.0)
            
            u, s, v = u[:, :rank], s[:rank], v[:rank, :]
             
            B = np.dot(u, np.dot(np.diag(s), v))
            F = shrink(M - B + Y / mu, lam / mu)
            if np.linalg.norm(B - B_temp) / norm < delta and np.linalg.norm(F - F_temp) / norm < delta:
                primal_converged = True
            
        # Check for convergence.
        step = M - B - F
        Y = Y + mu * step
        err = np.linalg.norm(step) / norm
        if verbose:
            logger.info(("Iteration {0}: error={1:.3e}, rank={2:d}, nnz={3:d}, "
                   "time={4:.3e}")
                  .format(i, err, np.rank(B), np.sum(F > 0), svd_time))
        if err < delta:
            converged = True
        i += 1
        mu = rho * mu
        print mu

    if i >= maxiter:
        logger.warn("convergence not reached in alm")

    return B, F, (u, s, v)


def shrink(M, tau):
    sgn = np.sign(M)
    S = np.abs(M) - tau
    S[S < 0.0] = 0.0
    return sgn * S

def _svd(method, X, rank, tol, **args):
    rank = min(rank, np.min(X.shape))
    if method == "approximate":
        return fbpca.pca(X, k=rank, raw=True, **args)
    elif method == "exact":
        return np.linalg.svd(X, full_matrices=False, **args)
    elif method == "sparse":
        if rank >= np.min(X.shape):
            return np.linalg.svd(X, full_matrices=False)
        u, s, v = svds(X, k=rank, tol=tol)
        u, s, v = u[:, ::-1], s[::-1], v[::-1, :]
        return u, s, v
    raise ValueError("invalid SVD method")
