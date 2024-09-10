import numpy as np


class Node(object):

    def __init__(self,
                 nid,
                 coords,
                 constraints,
                 applied_disp,
                 applied_force,
                 config):

        self._nid = nid
        self._config = config
        #x,y
        self._coord = (coords[0],
                       coords[1])
        #tx, ty, rz 0=free, 1=fixed
        self._constraint = (constraints[0],constraints[1],constraints[2])
        self._applied_disp = (applied_disp[0],applied_disp[1],applied_disp[2])
        self._applied_force = (applied_force[0],applied_force[1],applied_force[2])

    def StoreGlobalIndex(self, global_idx):
        self._global_idx = global_idx

    def StorePostProcessDisp(self, U):
        slice = np.array(self._global_idx)
        disp = U[slice[:, None], 0]
        self._disp = (disp[0], disp[1], disp[2])
        self._coord_disp = (self._coord[0] + self._disp[0],
                            self._coord[1] + self._disp[1],
                            self._disp[2]
                            )