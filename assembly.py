from node import *
import numpy as np
def TransformGlobalIndex(node):

    base = node._nid * 2 + node._nid
    global_idx = [base, base + 1, base + 2]
    node.StoreGlobalIndex(global_idx)
    return global_idx

def AssembleK(nodes, elements):
    k = np.zeros(shape=(len(nodes)*3, len(nodes)*3))
    for ele in elements:
        ele.SetElement()
        global_idxi = TransformGlobalIndex(ele._nodes[0])
        global_idxj = TransformGlobalIndex(ele._nodes[1])
        global_idx = np.array(global_idxi + global_idxj)
        k[global_idx[:, None], global_idx] += ele._ke

    return k

def AssembleVectors(nodes):
    u = np.zeros(shape=(len(nodes) * 3, 1)) #displacement vector
    f = np.zeros(shape=(len(nodes) * 3, 1)) #applied force vector
    p = np.zeros(shape=(len(nodes) * 3, 1)) #react force vector
    constraints = np.zeros(shape=(len(nodes) * 3, 1))
    for node in nodes:
        global_idx = np.array(TransformGlobalIndex(node))
        u[global_idx,0] += node._applied_disp
        f[global_idx,0] += node._applied_force
        constraints[global_idx, 0] += node._constraint

    idx_free = np.asarray(constraints == 0).nonzero()[0]
    idx_fix = np.asarray(constraints == 1).nonzero()[0]

    return u,f,p,constraints, idx_free, idx_fix
