from matplotlib.pyplot import plot, show, legend


def LV2(a, b, alph, bet, gam, delt, ic):
    from numpy import linspace, array
    from matplotlib.pyplot import plot, show, legend, subplots
    from matplotlib.animation import FuncAnimation

    def fx(x, y, t):
        return alph * x - bet * x * y

    def fy(x, y, t):
        return gam * x * y - delt * y

    def f(r, t):
        x = r[0]
        y = r[1]
        return array([fx(x, y, t), fy(x, y, t)], float)

    N = 100
    tp = linspace(a, b, N)
    r = array(ic, float)

    xp = []
    yp = []
    h = (b - a) / N
    for t in tp:
        xp.append(r[0])
        yp.append(r[1])
        k1 = h * f(r, t)
        k2 = h * f(r + k1 / 2, t + h / 2)
        k3 = h * f(r + k2 / 2, t + h / 2)
        k4 = h * f(r + k3, t + h)
        r += 1 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    fig, axis = subplots()
    axis.set_xlim(min(tp), max(tp))

    def max_min_arrays(array1, array2):
        max_mayor = max(max(array1), max(array2))
        min_menor = min(min(array1), min(array2))
        if max_mayor == min_menor:
            max_mayor += 1
        return max_mayor, min_menor
    may, miy = max_min_arrays(xp, yp)
    axis.set_ylim(miy, may)

    axis.set_title(
        r"$\frac{dx}{dt}=\alpha x-\beta xy$ \n $\frac{dy}{dt}=\gamma xy-\delta y$")

    ani_plot_c, = axis.plot([], [], label='Prey population')
    ani_plot_z, = axis.plot([], [], label='Predator population')

    def udata1(frame):
        ani_plot_z.set_data(tp[:frame], yp[:frame])
        ani_plot_c.set_data(tp[:frame], xp[:frame])
        return ani_plot_c, ani_plot_z

    animation1 = FuncAnimation(
        fig=fig, func=udata1, frames=len(tp), interval=b)

    legend()
    show()  # Agregamos esta línea para mostrar la animación
    return animation1


# Llama a la función para iniciar la animación
LV2(0, 300, 0.1, 0.002, 0.0025, 0.2, [20, 80])


""" def LV2(a, b, alph, bet, gam, delt, ic):

    
    This is a time evolution animation of the 
       

    from numpy import linspace, array
    from matplotlib.pyplot import plot, show, legend, subplots
    from matplotlib.animation import FuncAnimation

    def fx(x, y, t):
        return alph * x - bet * x * y # Prey function

    def fy(x, y, t):
        return gam * x * y - delt * y

    def f(r, t):
        x = r[0]
        y = r[1]
        return array([fx(x, y, t), fy(x, y, t)], float)

    N = 100
    tp = linspace(a, b, N)
    r = array(ic, float)

    xp = []
    yp = []
    h = (b - a) / N
    for t in tp:
        xp.append(r[0])
        yp.append(r[1])
        k1 = h * f(r, t)
        k2 = h * f(r + k1 / 2, t + h / 2)
        k3 = h * f(r + k2 / 2, t + h / 2)
        k4 = h * f(r + k3, t + h)
        r += 1 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    fig, axis = subplots()
    axis.set_xlim(min(xp), max(xp))

    def max_min_arrays(array1, array2):
        max_mayor = max(max(array1), max(array2))
        min_menor = min(min(array1), min(array2))
        return max_mayor, min_menor
    may, miy = max_min_arrays(xp, yp)
    axis.set_ylim(min(yp), max(yp))
    axis.set_ylim(min(yp), max(yp))

    ani_plot_cz, = axis.plot([], [], label='Prey population')
    ani_plot_z, = axis.plot([], [], label='Predator population')

    def udata1(frame):
        # ani_plot_z.set_data(tp[:frame], yp[:frame])
        ani_plot_cz.set_data(xp[:frame], yp[:frame])
        return ani_plot_cz

    animation1 = FuncAnimation(
        fig=fig, func=udata1, frames=len(tp), interval=b/N)

    legend()
    show()  # Agregamos esta línea para mostrar la animación
    return animation1 """


# Llama a la función para iniciar la animación
# LV2(0, 40, 1, 1, 1, 1, [2, 3])
