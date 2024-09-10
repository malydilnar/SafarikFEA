from element import *
from tensors import *
import numpy as np

class Truss(Element):

    def SetElement(self):
        self._A = self._shape._A
        self._E = self._mat._E
        self.__Ke()

    def __Ke(self):
        k = np.zeros(shape=(3, 3))
        self._l, self._n, self._s = OrientationLine2D(self._nodes[0], self._nodes[1])
        kax = self._A * self._E / self._l
        kf = kax * np.outer(self._n, self._n)

        k[0, 0] = kf[0, 0]
        k[0, 1] = kf[0, 1]
        k[1, 0] = kf[1, 0]
        k[1, 1] = kf[1, 1]

        self._ke = np.vstack((np.hstack((k, -k)), np.hstack((-k, k))))

    def Shape(self, x):
        N1 = 1-x/self._l
        N2 = x/self._l
        N = [N1, N2]

        B1 = -1/self._l
        B2 = 1/self._l
        B = [B1, B2]

        return N, B
