from element import *
from tensors import *
import numpy as np

class Frame(Element):

    def SetElement(self):

        self._A = self._shape._A
        self._E = self._mat._E
        self._Ix = self._shape._Ix
        self._Iy = self._shape._Iy

        if self._config['Formulation Frame'] == 'Euler':
            self.__KeEuler()

        elif self._config['Formulation Frame'] == 'Timoshenko':
            self.__KeTimoshenko()

    def __KeEuler(self):

        self._l, self._n, self._s = OrientationLine2D(self._nodes[0], self._nodes[1])
        k11 = np.zeros(shape=(3, 3))
        k12 = np.zeros(shape=(3, 3))
        k21 = np.zeros(shape=(3, 3))
        k22 = np.zeros(shape=(3, 3))

        kfu_v = 12 * self._E * self._Ix / (self._l ** 3) * np.outer(self._s, self._s)
        kfu_ax = self._A * self._E / self._l * np.outer(self._n, self._n)
        kfu = kfu_v + kfu_ax
        kmu = 6 * self._E * self._Ix / (self._l ** 2) * self._s
        kmo = 4 * self._E * self._Ix / self._l
        k_mo = 2 * self._E * self._Ix / self._l

        k11[0, 0] = kfu[0, 0]
        k11[0, 1] = kfu[0, 1]
        k11[1, 0] = kfu[1, 0]
        k11[1, 1] = kfu[1, 1]
        k11[0, 2] = kmu[0]
        k11[1, 2] = kmu[1]
        k11[2, 0] = kmu[0]
        k11[2, 1] = kmu[1]
        k11[2, 2] = kmo

        k12[0, 0] = -kfu[0, 0]
        k12[0, 1] = -kfu[0, 1]
        k12[1, 0] = -kfu[1, 0]
        k12[1, 1] = -kfu[1, 1]
        k12[0, 2] = kmu[0]
        k12[1, 2] = kmu[1]
        k12[2, 0] = -kmu[0]
        k12[2, 1] = -kmu[1]
        k12[2, 2] = k_mo

        k21[0, 0] = -kfu[0, 0]
        k21[0, 1] = -kfu[0, 1]
        k21[1, 0] = -kfu[1, 0]
        k21[1, 1] = -kfu[1, 1]
        k21[0, 2] = -kmu[0]
        k21[1, 2] = -kmu[1]
        k21[2, 0] = kmu[0]
        k21[2, 1] = kmu[1]
        k21[2, 2] = k_mo

        k22[0, 0] = kfu[0, 0]
        k22[0, 1] = kfu[0, 1]
        k22[1, 0] = kfu[1, 0]
        k22[1, 1] = kfu[1, 1]
        k22[0, 2] = -kmu[0]
        k22[1, 2] = -kmu[1]
        k22[2, 0] = -kmu[0]
        k22[2, 1] = -kmu[1]
        k22[2, 2] = kmo

        self._ke = np.vstack((np.hstack((k11, k12)), np.hstack((k21, k22))))

    def __KeTimoshenko(self):

        self._l, self._n, self._s = OrientationLine2D(self._nodes[0], self._nodes[1])
        k11 = np.zeros(shape=(3, 3))
        k12 = np.zeros(shape=(3, 3))
        k21 = np.zeros(shape=(3, 3))
        k22 = np.zeros(shape=(3, 3))

        self.__KsTimoshenko()
        self._phi = (12*self._E*self._Ix)/(self._ks*self._A*self._mat._G*self._l**2)
        const = (self._E*self._Ix)/((1+self._phi)*self._l**3)

        kfu_v = const*12 * np.outer(self._s, self._s)
        kfu_ax = self._A * self._E / self._l * np.outer(self._n, self._n)
        kfu = kfu_v + kfu_ax
        kmu = const * 6 * self._l * self._s
        kmo = const * (4 + self._phi) * self._l**2
        k_mo = const * (2 - self._phi) * self._l**2

        k11[0, 0] = kfu[0, 0]
        k11[0, 1] = kfu[0, 1]
        k11[1, 0] = kfu[1, 0]
        k11[1, 1] = kfu[1, 1]
        k11[0, 2] = kmu[0]
        k11[1, 2] = kmu[1]
        k11[2, 0] = kmu[0]
        k11[2, 1] = kmu[1]
        k11[2, 2] = kmo

        k12[0, 0] = -kfu[0, 0]
        k12[0, 1] = -kfu[0, 1]
        k12[1, 0] = -kfu[1, 0]
        k12[1, 1] = -kfu[1, 1]
        k12[0, 2] = kmu[0]
        k12[1, 2] = kmu[1]
        k12[2, 0] = -kmu[0]
        k12[2, 1] = -kmu[1]
        k12[2, 2] = k_mo

        k21[0, 0] = -kfu[0, 0]
        k21[0, 1] = -kfu[0, 1]
        k21[1, 0] = -kfu[1, 0]
        k21[1, 1] = -kfu[1, 1]
        k21[0, 2] = -kmu[0]
        k21[1, 2] = -kmu[1]
        k21[2, 0] = kmu[0]
        k21[2, 1] = kmu[1]
        k21[2, 2] = k_mo

        k22[0, 0] = kfu[0, 0]
        k22[0, 1] = kfu[0, 1]
        k22[1, 0] = kfu[1, 0]
        k22[1, 1] = kfu[1, 1]
        k22[0, 2] = -kmu[0]
        k22[1, 2] = -kmu[1]
        k22[2, 0] = -kmu[0]
        k22[2, 1] = -kmu[1]
        k22[2, 2] = kmo

        self._ke = np.vstack((np.hstack((k11, k12)), np.hstack((k21, k22))))

    def __KsTimoshenko(self):
        if self._shape._type == 'Circle':
            self._ks = 6*(1+self._mat._v)/(7+6*self._mat._v)

        elif self._shape._type == 'Rectangle':
            self._ks = 10*(1+self._mat._v)/(12+11*self._mat._v)

        else:
            raise ValueError('Shape Type {} Shear Correction Factor Not Supported'.format(self._shape._type))

    def PostProcess(self):
        self._V = []
        self._M = []
        self._Ax = []
        self._Vx_plot = []
        self._Vy_plot = []
        self._Mx_plot = []
        self._My_plot = []
        self._Ax_x_plot = []
        self._Ax_y_plot = []

        ui = self._n @ np.array([[self._nodes[0]._coord_disp[0], self._nodes[0]._coord_disp[1]]])
        uj = self._n @ np.array([[self._nodes[1]._coord_disp[0], self._nodes[1]._coord_disp[1]]])
        oi = self._nodes[0]._coord_disp[2]
        wi = self._s @ np.array([[self._nodes[0]._coord_disp[0], self._nodes[0]._coord_disp[1]]])
        wj = self._s @ np.array([[self._nodes[1]._coord_disp[0], self._nodes[1]._coord_disp[1]]])
        oj = self._nodes[1]._coord_disp[2]

        for x in np.linspace(0, self._l, self._config['Element Force Solution Steps']):
            if self._config['Formulation Frame'] == 'Euler':
                N, B, dB, Na, Ba = self.__EulerShape(x)

            if self._config['Formulation Frame'] == 'Timoshenko':
                N, B, dB, Na, Ba = self.__TimoshenkoShape(x)

            w = wi * N[0] + oi * N[1] + wj * N[2] + oj * N[3]
            dwdx = wi * B[0] + oi * B[1] + wj * B[2] + oj * B[3]
            d2wdx2 = wi * dB[0] + oi * dB[1] + wj * dB[2] + oj * dB[3]

            u = ui * Na[0] + uj * Na[1]
            dudx = ui * Ba[0] + uj * Ba[1]

            M = -self._E * self._Ix * dwdx
            V = -self._E * self._Ix * d2wdx2
            Ax = self._A * self._E * dudx

            self._V.append(V)
            self._M.append(M)
            self._Ax.append(Ax)


            # project along member
            x_project = x * self._n
            V_project = V * self._s * self._config['Element Force Plot Scale']
            M_project = M * self._s * self._config['Element Force Plot Scale']
            Ax_project = Ax * self._s * self._config['Element Force Plot Scale']

            Vx = V_project[0][0] + x_project[0] + self._nodes[0]._coord_disp[0]
            Vy = V_project[0][1] + x_project[1] + self._nodes[0]._coord_disp[1]
            Mx = M_project[0][0] + x_project[0] + self._nodes[0]._coord_disp[0]
            My = M_project[0][1] + x_project[1] + self._nodes[0]._coord_disp[1]
            Ax_x = Ax_project[0][0] + x_project[0] + self._nodes[0]._coord_disp[0]
            Ax_y = Ax_project[0][1] + x_project[1] + self._nodes[0]._coord_disp[1]

            self._Vx_plot.append(Vx)
            self._Vy_plot.append(Vy)
            self._Mx_plot.append(Mx)
            self._My_plot.append(My)
            self._Ax_x_plot.append(Ax_x)
            self._Ax_y_plot.append(Ax_y)

    def __EulerShape(self, x):
        l = self._l

        # Beam Shape FUnctions
        N1 = 1 - 3 * x ** 2 / (l ** 2) + 2 * x ** 3 / (l ** 3)
        N2 = x - 2 * x ** 2 / l + x ** 3 / (l ** 2)
        N3 = 3 * x ** 2 / (l ** 2) - 2 * x ** 3 / (l ** 3)
        N4 = -x ** 2 / l + x ** 3 / (l ** 2)
        N = [N1, N2, N3, N4]

        B1 = -6 / (l ** 2) + 12 * x / (l ** 3)
        B2 = -4 / l + 6 * x / (l ** 2)
        B3 = 6 / (l ** 2) - 12 * x / (l ** 3)
        B4 = -2 / l + 6 * x / (l ** 2)
        B = [B1, B2, B3, B4]

        dB1 = 12 / (l ** 3)
        dB2 = 6 / (l ** 2)
        dB3 = -12 / (l ** 3)
        dB4 = 6 / (l ** 2)
        dB = [dB1, dB2, dB3, dB4]

        # Axial Shape Functions
        Na1 = 1 - x / l
        Na2 = x / l
        Na = [Na1, Na2]

        Ba1 = -1 / l
        Ba2 = 1 / l
        Ba = [Ba1, Ba2]

        return N, B, dB, Na, Ba

    def __TimoshenkoShape(self, x):
        l = self._l
        phi = self._phi

        N1 = 1/(1+phi) * (1-3*(x/l)**2 + 2*(x/l)**3 + (1-x/l)*phi)
        N2 = l/(1+phi) * (x/l - 2*(x/l)**2 + (x/l)**3 + 1/2*(x/l-(x/l)**2)*phi)
        N3 = 1/(1+phi) * (3*(x/l)**2 - 2*(x/l)**3 + (x/l)*phi)
        N4 = l/(1+phi) * (-(x/l)**2 + (x/l)**3 - 1/2*(x/l - (x/l)**2)*phi)
        N = [N1, N2, N3, N4]

        B1 = 1/(1+phi) * (-6*x/l**2 + 6*x**2/l**3 + (-1/l)*phi)
        B2 = l / (1 + phi) * (1/l - 4*x/l**2 + 3*x**2/l**3 + 1/2*(1/l - 2*x/l**2)*phi)
        B3 = 1 / (1 + phi) * (6*x/l**2 - 6*x**2/l**3 + (1/l)*phi)
        B4 = l / (1 + phi) * (-2*x/l**2 + 3*x**2/l**3 - 1/2*(1/l - 2*x/l**2)*phi)
        B = [B1, B2, B3, B4]

        dB1 = 1 / (1 + phi) * (-6/l**2 + 12*x/l**3)
        dB2 = l / (1 + phi) * (-4/l**2 + 6*x/l**3 + 1/2*(-2/l**2)*phi)
        dB3 = 1 / (1 + phi) * (6/l**2 - 12*x/l**3)
        dB4 = l / (1 + phi) * (-2/l**2 + 6*x/l**3 - 1/2*(-2/l**2)*phi)
        dB = [dB1, dB2, dB3, dB4]

        # Axial Shape Functions
        Na1 = 1 - x / l
        Na2 = x / l
        Na = [Na1, Na2]

        Ba1 = -1 / l
        Ba2 = 1 / l
        Ba = [Ba1, Ba2]

        return N, B, dB, Na, Ba