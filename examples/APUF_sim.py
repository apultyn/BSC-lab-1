from array import *
from pypuf.simulation import ArbiterPUF
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

# Rozkład odpowiedzi APUF, oddzielnie dla "0" i "1"
Z0 = np.empty(shape=[len(size_tab), len(noisiness_tab)], dtype="float")
Z1 = np.empty(shape=[len(size_tab), len(noisiness_tab)], dtype="float")


for size in range(len(size_tab)):
    for noise in range(len(noisiness_tab)):
        print("Rozmiar APUF", size_tab[size], "Noisiness", noisiness_tab[noise])

        puf = ArbiterPUF(n=size_tab[size], seed=1, noisiness=noisiness_tab[noise])
        r = puf.eval(random_inputs(n=size_tab[size], N=Num_of_challenges, seed=1))

        hist, bin_edges = np.histogram(r, bins=2)
        print(hist)

        Z0[size][noise] = hist[0]
        Z1[size][noise] = hist[1]
        print("---------------------------------------")

X, Y = np.meshgrid(size_tab, noisiness_tab, indexing="ij")

wykres = matplotlib.pyplot.figure()
w = wykres.add_subplot(projection="3d")
w.set_proj_type("ortho")
w.view_init(elev=30, azim=45)
# print (np.amin(Z0), np.amax(Z0), np.amin(Z1), np.amax(Z1))

w.plot_surface(X, Y, Z0, cmap=plt.cm.Blues, linewidth=0.5, rstride=1, cstride=1)
w.plot_surface(X, Y, Z1, cmap=plt.cm.Reds, linewidth=0.5, rstride=1, cstride=1)

# w.plot_wireframe( X,Y, Z0, rstride=1, cstride=1,color='#FF0000')
# w.plot_wireframe( X,Y, Z1, rstride=1, cstride=1,color='#0000FF')


# plt.show()
# plt.savefig('APUF_zeros_ones.png', dpi=300)
