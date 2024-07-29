from numpy import linspace, array, pi, sin, cos
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def f(r, t, O=5):
    from numpy import sin, cos, pi
    g = 9.81
    l = 10e-2
    th = r[0]*pi/180
    w = r[1]
    return array([w, -g/l*sin(th)+2*cos(th)*sin(O*t)], float)


a = 0
b = 100
N = 1000
tp = linspace(a, b, N)
l = 10e-2

r = array([0, 0], float)
xp = []
yp = []
h = (b-a)/N
fig, axs = plt.subplots(2, 3, figsize=(15, 20))
for i in range(0, 2):
    xp.clear()
    yp.clear()
    for t in tp:
        xp.append(r[0])
        yp.append(r[1])
        k1 = h*f(r, t)
        k2 = h*f(r+k1/2, t+h/2, i)
        k3 = h*f(r+k2/2, t+h/2, i)
        k4 = h*f(r+k3, t+h, i)
        r += 1/6*(k1+2*k2+2*k3+k4)

    # Configurar subgráficas en una fila

    # Primera gráfica: xp respecto a tp
    ani_plot_z, = axs[i, 0].plot([], [])
    axs[i, 0].set_xlim(0, max(tp))
    axs[i, 1].set_xlim(0, max(tp))
    axs[i, 2].set_xlim(min(xp), max(xp))
    axs[i, 2].set_ylim(min(yp), max(yp))
    axs[0, 0].set_title('xp respecto a tp')

    # Segunda gráfica: yp respecto a tp
    ani_plot_c, = axs[i, 1].plot([], [])
    axs[0, 1].set_title('yp respecto a tp')

    # Tercera gráfica: xp respecto a yp
    ani_plot, = axs[i, 2].plot([], [])
    axs[0, 2].set_title('xp respecto a yp')

    # Añadir título a la fila con el valor de i
    axs[i, 0].set_ylabel(f'\u03A9 = {i}')

    def udata1(frame):
        ani_plot_z.set_data(tp[:frame], yp[:frame])
        ani_plot_c.set_data(tp[:frame], xp[:frame])
        ani_plot.set_data(xp[:frame], yp[:frame])

        return ani_plot_c, ani_plot_z

    animation1 = FuncAnimation(
        fig=fig, func=udata1, frames=len(tp), interval=b/N)

    # Ajustes y mostrar las gráficas
    plt.tight_layout()
    plt.show()
