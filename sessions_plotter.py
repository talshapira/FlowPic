import matplotlib.pyplot as plt
import numpy as np

MTU = 1500


def session_spectogram(ts, sizes, name=None):
    plt.scatter(ts, sizes, marker='.')
    plt.ylim(0, MTU + 100)
    plt.xlim(ts[0], ts[-1])
    # plt.yticks(np.arange(0, MTU, 10))
    # plt.xticks(np.arange(int(ts[0]), int(ts[-1]), 10))
    plt.title(name + " Session Spectogram")
    plt.ylabel('Size [B]')
    plt.xlabel('Time [sec]')

    plt.grid(True)
    plt.show()


def session_histogram(sizes, plot=False):
    hist, bin_edges = np.histogram(sizes, bins=range(0, MTU + 1, 1))
    if plot:
        plt.bar(bin_edges[:-1], hist, width=1)
        plt.xlim(min(bin_edges), max(bin_edges)+100)
        plt.show()
    return hist.astype(np.uint16)


def session_2d_histogram(ts, sizes, plot=False):
    # ts_norm = map(int, ((np.array(ts) - ts[0]) / (ts[-1] - ts[0])) * MTU)
    ts_norm = ((np.array(ts) - ts[0]) / (ts[-1] - ts[0])) * MTU
    H, xedges, yedges = np.histogram2d(sizes, ts_norm, bins=(range(0, MTU + 1, 1), range(0, MTU + 1, 1)))

    if plot:
        plt.pcolormesh(xedges, yedges, H)
        plt.colorbar()
        plt.xlim(0, MTU)
        plt.ylim(0, MTU)
        plt.set_cmap('binary')
        plt.show()
    return H.astype(np.uint16)
