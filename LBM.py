import numpy as np
import matplotlib.pyplot as plt


def distance(x1, y1, x2, y2):
    return np.sqrt((x2-x1)**2+(y2-y1)**2)


def main():

    Nx, Ny, Nt = 100, 400, 3000  # Dimensions of the lattice and time of simulation

    tau = 0.53  # Visocsity
    NL = 9
    cxs = np.array([0, 0, 1, 1, 1, 0, -1, -1, -1], int)  # x velocities
    cys = np.array([0, 1, 1, 0, -1, -1, -1, 0, 1], int)  # y velocities

    weights = np.array(
        [4/9, 1/9, 1/36, 1/9, 1/36, 1/9, 1/36, 1/9, 1/36], float)

    # Initial condictions

    F = np.ones((Nx, Ny, NL)) + 0.01*np.random.randn(Nx, Ny, NL)

    F[:, :, 3] = 2.3

    cylinder = np.full((Nx, Ny), False)

    for y in range(0, Ny):
        for x in range(0, Nx):
            if distance(Nx//4, Ny//4, x, y) < 13:
                cylinder[x][y] = True

    for ii in range(Nt):
        print(ii)

        for i, cx, cy in zip(range(NL), cxs, cys):
            F[:, :, i] = np.roll(F[:, :, i], cx, axis=0)
            F[:, :, i] = np.roll(F[:, :, i], cy, axis=1)

        bondaryF = F[cylinder, :]
        bondaryF = bondaryF[:, [0, 5, 6, 7, 8, 1, 2, 3, 4]]

        # Fluid variables

        rho = np.sum(F, 2)
        ux = np.sum(F*cxs, 2)/rho
        uy = np.sum(F*cys, 2)/rho

        F[cylinder, :] = bondaryF

        ux[cylinder] = 0  # Velocities on the cylinder
        uy[cylinder] = 0  # Velocities on the cylinder

        # Collision

        Feq = np.zeros(F.shape)
        for i, cx, cy, w in zip(range(NL), cxs, cys, weights):

            Feq[:, :, i] = rho*w*(1+3*(cx*ux + cy*uy) +
                                  9*(cx*ux + cy*uy)**2/2 - 3*(ux**2+uy*2)/2)

        F += -(1/tau)*(F-Feq)

        if ii % 50 == 0:
            plt.imshow(np.sqrt(ux**2+uy**2))
            plt.pause(0.1)
            plt.cla()


if __name__ == "__main__":
    main()
