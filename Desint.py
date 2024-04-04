
def MCDecay1(NB, b, N):

    from numpy import linspace
    from matplotlib.pyplot import plot, show, legend, subplots
    from matplotlib.animation import FuncAnimation
    from random import random

    tauB = 46*60
    tauPb = 3.3*60
    tauTi = 2.2*60

    t = linspace(0, b, N)

    ma = NB
    NP = 0
    NBI = 0
    NTI = 0

    bp = []
    bip = []
    pbp = []
    tip = []
    for i in t:
        pB = 1-2**(-i/tauB)
        ppB = 1-2**(-i/tauPb)
        pTi = 1-2**(-i/tauTi)
        bp.append(NB)
        bip.append(NBI)
        pbp.append(NP)
        tip.append(NTI)
        for _ in range(NB):
            if random() < pB and random() < 0.9791:
                NB -= 1
                NP += 1

                if random() < ppB:
                    NBI += 1
            elif random() < pB and random() < 0.0209:
                NB -= 1
                NTI += 1
                if random() < pTi:
                    NP += 1
                    if random() < ppB:
                        NBI += 1

    fig, axis = subplots(figsize=(15, 15))
    axis.set_xlim(min(t), max(t))
    axis.set_ylim(-5, ma)
    axis.text(0.5, 1.100, "Átomos de $^{213}$ Bi | Átomos de $^{209}$ Bi | Átomos de $^{209}$ Pb | Átomos de $^{209}$ Ti | Time: ", bbox={'facecolor': 'white',
                                                                                                                                          'alpha': 0.5, 'pad': 5},
              transform=axis.transAxes, ha="center")

    def max_min_arrays(array1, array2):
        max_mayor = max(max(array1), max(array2))
        min_menor = min(min(array1), min(array2))
        if max_mayor == min_menor:
            max_mayor += 1
        return max_mayor, min_menor

    ani_plot_bp, =  axis.plot([], [], label="Átomos de $^{213}$ Bi")
    ani_plot_bip, = axis.plot([], [], label="Átomos de $^{209}$ Bi")
    ani_plot_pbp, = axis.plot([], [], label="Átomos de $^{209}$ Pb")
    ani_plot_tip, = axis.plot([], [], label="Átomos de $^{209}$ Ti")

    def udata1(frame):
        axis.text(0.5, 1.100, f"Átomos de $^{213}$ Bi {bp[frame]} | Átomos de $^{209}$ Bi {bip[frame]} | Átomos de $^{209}$ Pb {pbp[frame]} | Átomos de $^{209}$ Ti {tip[frame]} |Time: {frame*b}",
                  bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 5},
                  transform=axis.transAxes, ha="center")
        ani_plot_bp.set_data(t[:frame], bp[:frame])
        ani_plot_bip.set_data(t[:frame], bip[:frame])
        ani_plot_pbp.set_data(t[:frame], pbp[:frame])
        ani_plot_tip.set_data(t[:frame], tip[:frame])

        return ani_plot_bp, ani_plot_bip, ani_plot_pbp, ani_plot_tip

    animation1 = FuncAnimation(
        fig=fig, func=udata1, frames=len(t), interval=b/N)

    legend()
    show()  # Agregamos esta línea para mostrar la animación
    return animation1


MCDecay1(1000, 300, 100).save("GIFS/BiBiPbTi.gif")
