from element import *
from tensors import *
import numpy as np

class CBush(Element):

    def SetElement(self):
        self._A = self._shape._A
        self._ka = self._mat._ka
        self._ks = self._mat._ks
        self._km = self._mat._km
        self.__Ke()

    def __Ke(self):
        k = np.zeros(shape=(3, 3))
        self._l, self._n, self._s = OrientationLine2D(self._nodes[0], self._nodes[1])
        kfu = self._ka * np.outer(self._n, self._n)
        kfv = self._ks * np.outer(self._s, self._s)
        kf = kfu + kfv
        kmo = self._km

        k[0, 0] = kf[0, 0]
        k[0, 1] = kf[0, 1]
        k[1, 0] = kf[1, 0]
        k[1, 1] = kf[1, 1]
        k[2, 2] = kmo

        self._ke = np.vstack((np.hstack((k, -k)), np.hstack((-k, k))))

    def LinearShape(self, x):

        Na1 = 1 - x / self._l
        Na2 = x / self._l
        N = [Na1, Na2]

        Ba1 = -1 / self._l
        Ba2 = 1 / self._l
        B = [Ba1, Ba2]

        return N, B