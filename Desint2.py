def get_elemnts(user):
    """Crea un dataframe de pandas con los nombres de los elementos padres e hijos en una cadena de desintegración; además
    de las propiedades de probabilidad de desintegración del núcleo padre, tiempo de vida medio del nucleo padre

    Prameters:
    User: Elemento de los cuales se quiere obtener la cadena de desintegración

    Returns:
    base2: Dataframe con los datos de todos los elementos de la cadena"""
    import pandas as pd

    # the service URL
    livechart = "https://nds.iaea.org/relnsd/v1/data?"

    # There have been cases in which the service returns an HTTP Error 403: Forbidden
    # use this workaround
    import urllib.request

    def lc_pd_dataframe(url):
        req = urllib.request.Request(url)
        req.add_header(
            "User-Agent",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0",
        )
        return pd.read_csv(urllib.request.urlopen(req))

    final_data = []
    # Hacemos la consulta a la api
    df_a = lc_pd_dataframe(
        livechart + f"fields=decay_rads&nuclides={user}&rad_types=a "
    )
    # Hacemos la consulta a la api
    df_bm = lc_pd_dataframe(
        livechart + f"fields=decay_rads&nuclides={user}&rad_types=bm"
    )
    # Hacemos la consulta a la api
    df_bp = lc_pd_dataframe(
        livechart + f"fields=decay_rads&nuclides={user}&rad_types=bp"
    )
    # Hacemos la consulta a la api
    df_g = lc_pd_dataframe(
        livechart + f"fields=decay_rads&nuclides={user}&rad_types=g "
    )

    frames = [df_a, df_bm, df_bp, df_g]
    base = pd.concat(frames)
    while not base.empty:
        try:
            base = (
                base[
                    [
                        "d_symbol",
                        "d_z",
                        "d_n",
                        "decay",
                        "half_life_sec",
                        "decay_%",
                        "p_z",
                        "p_n",
                        "p_symbol",
                    ]
                ]
                .drop_duplicates()
                .dropna()
            )
            base = base[
                (base["decay"] == "A")
                | (base["decay"] == "B-")
                | (base["decay"] == "B+")
            ]
            base["suma_d"] = base["d_z"] + base["d_n"]
            base["d_name"] = base["suma_d"].astype(int).astype(str) + base[
                "d_symbol"
            ].astype(str)
            base["d_name"] = base["d_name"].str.lower()

            base["suma_p"] = base["p_z"] + base["p_n"]
            base["p_name"] = base["suma_p"].astype(int).astype(str) + base[
                "p_symbol"
            ].astype(str)
            base["p_name"] = base["p_name"].str.lower()
            base["decay_%"] = base["decay_%"] / 100

            base = base[["d_name", "p_name", "decay_%", "half_life_sec", "decay"]]

            final_data.append(base)

            base.drop_duplicates(inplace=True)

            # Convertir base['d_name'] a una lista para evitar problemas en la URL
            names_list = base["d_name"].tolist()

            frames = []
            for name in names_list:
                df_a = lc_pd_dataframe(
                    livechart + f"fields=decay_rads&nuclides={name}&rad_types=a"
                )
                df_bm = lc_pd_dataframe(
                    livechart + f"fields=decay_rads&nuclides={name}&rad_types=bm"
                )
                df_bp = lc_pd_dataframe(
                    livechart + f"fields=decay_rads&nuclides={name}&rad_types=bp"
                )
                df_g = lc_pd_dataframe(
                    livechart + f"fields=decay_rads&nuclides={name}&rad_types=g"
                )
                frames.extend([df_a, df_bm, df_bp, df_g])

            base = pd.concat(frames)

        except Exception as e:
            print(f"{e}")
            continue

    base2 = pd.concat(final_data)
    return base2


def create_lists_and_counters(df):
    """
    Crea un diccionario basado en los valores únicos de la columna 'd_name' del DataFrame,
    donde cada entrada contiene una lista de registros, una lista adicional para números y un contador.

    Parameters:
    df (pd.DataFrame): DataFrame que contiene la columna 'd_name'.

    Returns:
    dict: Diccionario donde las claves son los valores únicos de 'd_name' y los valores son diccionarios con
          una lista de registros, una lista para números y un contador.
    """
    # Crear un diccionario basado en los valores únicos de 'd_name'
    dict_of_data = {
        p_name: {"records": [], "numbers_list": [], "counter": 0}
        for p_name in df["p_name"].unique()
    }

    # Rellenar el diccionario con las filas correspondientes
    for p_name in dict_of_data:
        dict_of_data[p_name]["records"] = df[df["p_name"] == p_name].to_dict("records")

    return dict_of_data


def aupdate_data(user, b, N):
    import numpy as np
    import random
    from matplotlib.pyplot import plot, show, legend, subplots
    from matplotlib.animation import FuncAnimation

    base = get_elemnts(user)
    dict = create_lists_and_counters(base)
    t = np.linspace(0, b, N)
    initial_counts = 1000
    dict[user]["counter"] = initial_counts
    for i in t:
        for key, value in dict.items():
            dict[key]["numbers_list"].append(dict[key]["counter"])
            for _ in range(dict[key]["counter"]):

                for j in value["records"]:
                    prob = 1 - 2 ** (-i / j["half_life_sec"])

                    if random.random() < prob and random.random() < j["decay_%"]:

                        if j["d_name"] in dict.keys():
                            dict[key]["counter"] -= 1
                            dict[j["d_name"]]["counter"] += 1
                        else:
                            break
    aniplots = []
    fig, axis = subplots(figsize=(15, 15), ncols=2)
    axis[0].set_ylim(-5, initial_counts)
    axis[0].set_xlim(min(t), max(t))
    for key, value in dict.items():
        aniplots.append(
            axis[0].plot([], [], label=f"Átomos de {key}"),
        )

    def udata1(frame):
        for anis, (key, value) in zip(aniplots, dict.items()):
            anis[0].set_data(t[:frame], value["numbers_list"][:frame])
        return tuple(aniplots)

    animation1 = FuncAnimation(fig=fig, func=udata1, frames=len(t), interval=b / N)

    legend()
    show()  # Agregamos esta línea para mostrar la animación
    return animation1


user = "222rn"
aupdate_data(user, 30000, 300).save(f"GIFS/{user}_chain.gif")
