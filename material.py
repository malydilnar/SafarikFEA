
class Material(object):

    def __init__(self, mid, rho):
        self._mid = mid
        self._rho = rho
class LinearElastic(Material):

    def __init__ (self,mid,rho,E, v):
        self._mid = mid
        self._E = E
        self._rho = rho
        self._v = v
        self._G = self._E/(2*(1+self._v))

class DirectStiffness(Material):

    def __init__(self,mid,rho,ka,ks,km):
        self._mid = mid
        self._rho = rho
        self._ka = ka
        self._ks = ks
        self._km = km