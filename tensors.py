
import numpy as np

def OrientationLine2D(nodei, nodej):
    xi = nodei._coord[0]
    yi = nodei._coord[1]
    xj = nodej._coord[0]
    yj = nodej._coord[1]
    n = np.array([xj - xi, yj - yi])
    s = RotateZ2D(90) @ np.transpose(n)
    ll = np.dot(n, n)
    l = ll ** (1 / 2)

    n_unit = n / l
    s_unit = s / l

    return l, n_unit, s_unit

def ConvertDeg2Rad(deg):
        rad = (np.pi / 180) * deg
        cos = np.cos(rad)
        sin = np.sin(rad)
        return rad, cos, sin

def RotateZ2D(deg):
    rad, cos, sin = ConvertDeg2Rad(deg)
    R = np.array([[cos, -sin],
                  [sin, cos]])
    return R

def RotateX3D(deg):
    rad, cos, sin = ConvertDeg2Rad(deg)
    R = np.array([[1, 0, 0],
                  [0, cos, -sin],
                  [0, sin, cos]])
    return R

def RotateY3D(deg):
    rad, cos, sin = ConvertDeg2Rad(deg)
    R = np.array([[cos, 0, -sin],
                  [0, 1, 0],
                  [sin, 0, cos]])
    return R

def RotateZ3D(deg):
    rad, cos, sin = ConvertDeg2Rad(deg)
    R = np.array([[cos, -sin, 0],
                  [sin, cos, 0],
                  [0, 0, 1]])
    return R