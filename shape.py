import numpy as np
class Shape (object):

    def __init__(self, sid):
        self._sid = sid

class Circle (Shape):

    def __init__(self, sid, r):
        self._type = 'Circle'
        self._sid = sid
        self._r = r
        self.__Area()
        self.__I()

    def __I(self):
        self._Ix = np.pi / 4 * self._r ** 4
        self._Iy = self._Ix

    def __Area(self):
        self._A = np.pi * self._r ** 2

class Rectangle(Shape):

    def __init__(self, sid, b, h):
        self._type = 'Rectangle'
        self._sid = sid
        self._b = b
        self._h = h
        self.__Area()
        self.__Ix()
        self.__Iy()
    def __Ix(self):
        self._Ix = self.b * self.h ** 3 / 12

    def __Iy(self):
        self._Iy = self.b ** 3 * self.h / 12

    def __Area(self):
        self._A = self.b * self.h