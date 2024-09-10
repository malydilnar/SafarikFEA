import numpy as np

from material import *
from shape import *
from property import *
from node import *
from element_truss import *
from element_frame import *
from element_cbush import *
from solve import *
from postprocess import *


if __name__ == '__main__':

    #constants
    E = 10000000
    rho = 0.1
    v = 0.33
    r = 0.1
    ka = 1000
    ks = 500
    km = 100
    P = 100
    config =  {'Formulation Truss': 'Linear',
               'Formulation Frame': 'Timoshenko',
               'Formulation CBush': 'Linear',
               'Element Force Solution Steps': 2,
               'Element Force Plot Scale': 0.003,
               }

    length = 1
    num_ele = 10
    num_node = num_ele + 1
    y_coord = np.linspace(0, length, num_node)

    mat_info = [LinearElastic(0, rho, E, v),
                DirectStiffness(1,rho,ka,ks,km)]

    shape_info = [Circle(0, r)]
    prop_info = [Property(0, mat_info[0], shape_info[0]),
                 Property(1, mat_info[1], shape_info[0])]

    n_info = []
    e_info = []

    for ii in range(0, num_node):
        if ii == 0:
            n_info.append(Node(ii, (0, y_coord[ii]), (1, 1, 1), (0, 0, 0), (0, 0, 0), config))
        elif ii == num_node-1:
            n_info.append(Node(ii, (0, y_coord[ii]), (0, 0, 0), (0, 0, 0), (P, 100*P, 0), config))
        else:
            n_info.append(Node(ii, (0, y_coord[ii]), (0, 0, 0), (0, 0, 0), (0, 0, 0), config))

    for jj in range(0, num_ele):
        e_info.append(Frame(jj, [n_info[jj], n_info[jj+1]], prop_info[0], config))






    #n_info = [Node(0, (0, 0), (1, 1, 1), (0, 0, 0), (0, 0, 0)),
    #          Node(1, (0, 1), (0, 0, 0), (0, 0, 0), (0, 0, 0)),
    #          Node(2, (0, 2), (0, 0, 0), (0, 0, 0), (0, 0, 0)),
    #         Node(3, (0, 3), (0, 0, 0), (0, 0, 0), (P, 0, 0))]


    #e_info = [Frame(0, [n_info[0], n_info[1]], prop_info[0]),
    #          Frame(1, [n_info[1], n_info[2]], prop_info[0]),
    #          Frame(2, [n_info[2], n_info[3]], prop_info[0])]

    U, P = SolveLinearStatic(n_info, e_info)
    PlotDisplacement(n_info, e_info, U, P)



