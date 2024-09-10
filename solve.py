from assembly import *

def SolveLinearStatic(nodes, elements):
    #Global stiffness matrix
    K = AssembleK(nodes, elements)
    #Global vectors
    U, F, P, C, idx_free, idx_fix = AssembleVectors(nodes)

    Kff = K[idx_free[:, None], idx_free]
    Kfs = K[idx_free[:, None], idx_fix]
    Ksf = K[idx_fix[:, None], idx_free]
    Kss = K[idx_fix[:, None], idx_fix]
    Pf = P[idx_free[:, None], 0]
    Us = U[idx_fix[:, None], 0]
    Ff = F[idx_free[:, None], 0]
    Fs = F[idx_fix[:, None], 0]

    #  Calculate U(free) and P(support)
    U[idx_free[:, None], 0] = np.linalg.solve(Kff, ((Pf + Ff) - Kfs @ Us))
    P[idx_fix[:, None], 0] = Ksf @ U[idx_free[:, None], 0] + Kss @ Us - Fs

    return U, P
