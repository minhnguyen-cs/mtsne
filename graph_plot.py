__author__ = 'minh'

from mpl_toolkits.mplot3d import Axes3D
# from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import gif

color_list = ['r', 'y', '#fdb462', 'b','m','c', 'w', 'k','g']
marker_list = ['o', 'v', '8', 'D', 's', '^', '<', '>', 'p', '*', 'h', 'H', 'd']

"""
gen markers/colors depends on the labels and the marker_list/color_list
"""
def gen_markers_colors(labels, marker_color_list):
    distinct_markers = marker_color_list[0:len(labels) + 1]

    # create a mapping from label to color
    label_to_color = dict(zip(set(labels), distinct_markers))

    # generate colors corresponding to labels
    markers = []
    for label in labels:
        markers.append(label_to_color[label])
    return markers



"""
output: a graph visualizing data points
"""
def dump_graph(Y, labels, output_graph, annotations = None, d=2):

    # generate a random color corresponding to each label
    colors = gen_markers_colors(labels, color_list)
    markers = gen_markers_colors(labels, marker_list)

    fig = plt.figure(figsize=(12,8))
    if d == 3:
        ax = fig.gca(projection='3d')
        # ax = fig.add_subplot(111, projection='3d')
    else:
        ax = fig.gca()

    scats, anots = [], []
    for (i, cla) in enumerate(set(labels)):
        xc = [p for (j, p) in enumerate(Y[:, 0]) if labels[j] == cla]
        yc = [p for (j, p) in enumerate(Y[:, 1]) if labels[j] == cla]
        if d == 3:
            zc = [p for (j, p) in enumerate(Y[:, 2]) if labels[j] == cla]

        if annotations is not None:
            ac = [annotations[j] for (j, _) in enumerate(Y[:, 0]) if labels[j] == cla]

        cols = [c for (j, c) in enumerate(colors) if labels[j] == cla]
        mars = [m for (j, m) in enumerate(markers) if labels[j] == cla]

        # ax.set_xlabel('PC1')
        # ax.set_ylabel('PC2')
        ax.set_xlabel('Latent space')
        ax.set_ylabel('Latent space')
        scat = None
        if d == 2:
            # scat = ax.scatter(xc, yc, s=40, marker=mars[0], c=cols, label=cla)
            scat = ax.scatter(xc, yc, s=40)
        elif d == 3:
            # scat = ax.scatter(xc, yc, zc, s=40, marker=mars[0], c=cols, label=cla, depthshade=False)
            scat = ax.scatter(xc, yc, zc, s=40, depthshade=False)
            ax.set_zlabel('Latent space')

        # add anotations to each data point
        if annotations is not None:
            for j in range(len(xc)):
                anot = None
                if d == 2:
                    anot = ax.annotate(ac[j], (xc[j], yc[j]), fontsize=10.5, xytext=(2, 6),
                             ha='right', textcoords='offset points')
                elif d == 3:
                    anot = ax.text(xc[j], yc[j], zc[j], ac[j]) #,  fontsize=8, xytext=(2, 5), ha='right', textcoords='offset points')
                anots.append(anot)
        scats.append(scat)

    # fig.suptitle('PCA', fontsize=14)
    # ax.legend(scatterpoints=1, loc=1, fontsize=12)

    if d == 3:
        angles = np.linspace(90, 450, 30)[:-1]  # Take 30 angles between 0 and 360
        # create an animated gif (100ms between frames)
        gif.rotanimate(ax, angles, output_graph+".gif", delay=100)

    if d==2:
        plt.show();

	for scat in scats:
        scat.remove()
    for anot in anots:
        anot.remove()

