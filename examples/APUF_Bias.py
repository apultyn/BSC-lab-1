from array import *
from pypuf.simulation import ArbiterPUF
from pypuf.metrics import bias
import numpy as np
from pypuf.io import random_inputs

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator

Num_of_challenges = 10_000
puf_bias = 0.0
size_tab = np.array(
    [8, 16, 24, 32, 48, 54, 64, 72, 80, 88, 96, 104, 112, 120, 128], dtype="int"
)
noisiness_tab = np.array(
    [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], dtype="float"
)

Z = np.empty(shape=[len(size_tab), len(noisiness_tab)], dtype="float")


for size in range(len(size_tab)):
    for noise in range(len(noisiness_tab)):
        print("Rozmiar APUF", size_tab[size], "Noisiness", noisiness_tab[noise])

        puf = ArbiterPUF(n=size_tab[size], seed=1, noisiness=noisiness_tab[noise])
        r = puf.eval(random_inputs(n=size_tab[size], N=Num_of_challenges, seed=1))

        hist, bin_edges = np.histogram(r, bins=2)
        print(hist)

        puf_bias = bias(
            ArbiterPUF(n=size_tab[size], seed=1, noisiness=noisiness_tab[noise]),
            seed=1,
            N=Num_of_challenges,
        )
        print(
            "puf_bias:",
            puf_bias,
            "size",
            size_tab[size],
            "Noisiness",
            noisiness_tab[noise],
        )
        Z[size][noise] = puf_bias

        print("---------------------------------------")

X, Y = np.meshgrid(size_tab, noisiness_tab, indexing="ij")

wykres = matplotlib.pyplot.figure()
w = wykres.add_subplot(projection="3d")
w.set_proj_type("ortho")
w.view_init(elev=30, azim=45)
# print (np.amin(Z), np.amax(Z))

w.plot_surface(X, Y, Z, cmap=plt.cm.Blues, linewidth=0.5, rstride=1, cstride=1)
# w.plot_wireframe( X,Y, Z, rstride=1, cstride=1,color='#FF0000')
# plt.show()

plt.savefig("APUF_bias.png", dpi=300)
