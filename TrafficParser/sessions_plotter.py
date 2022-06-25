#!/usr/bin/env python
"""
sessions_plotter.py has 3 functions to create spectogram, histogram, 2d_histogram from [(ts, size),..] session.
"""

import matplotlib.pyplot as plt
import numpy as np

MTU = 1500

def session_spectogram(ts, sizes, name=None):
    plt.scatter(ts, sizes, marker='.')
    plt.ylim(0, MTU)
    plt.xlim(ts[0], ts[-1])
    # plt.yticks(np.arange(0, MTU, 10))
    # plt.xticks(np.arange(int(ts[0]), int(ts[-1]), 10))
    plt.title(name + " Session Spectogram")
    plt.ylabel('Size [B]')
    plt.xlabel('Time [sec]')

    plt.grid(True)
    plt.show()


def session_atricle_spectogram(ts, sizes, fpath=None, show=True, tps=None):
    if tps is None:
        max_delta_time = ts[-1] - ts[0]
    else:
        max_delta_time = tps

    ts_norm = ((np.array(ts) - ts[0]) / max_delta_time) * MTU
    plt.figure()
    plt.scatter(ts_norm, sizes, marker=',', c='k', s=5)
    plt.ylim(0, MTU)
    plt.xlim(0, MTU)
    plt.ylabel('Packet Size [B]')
    plt.xlabel('Normalized Arrival Time')
    plt.set_cmap('binary')
    plt.axes().set_aspect('equal')
    plt.grid(False)
    if fpath is not None:
        # plt.savefig(OUTPUT_DIR + fname, bbox_inches='tight', pad_inches=1)
        plt.savefig(fpath, bbox_inches='tight')
    if show:
        plt.show()
    plt.close()


def session_histogram(sizes, plot=False):
    hist, bin_edges = np.histogram(sizes, bins=range(0, MTU + 1, 1))
    if plot:
        plt.bar(bin_edges[:-1], hist, width=1)
        plt.xlim(min(bin_edges), max(bin_edges)+100)
        plt.show()
    return hist.astype(np.uint16)


def session_2d_histogram(ts, sizes, plot=False, tps=None):
    if tps is None:
        max_delta_time = ts[-1] - ts[0]
    else:
        max_delta_time = tps

    # ts_norm = map(int, ((np.array(ts) - ts[0]) / max_delta_time) * MTU)
    ts_norm = ((np.array(ts) - ts[0]) / max_delta_time) * MTU
    H, xedges, yedges = np.histogram2d(sizes, ts_norm, bins=(range(0, MTU + 1, 1), range(0, MTU + 1, 1)))

    if plot:
        plt.pcolormesh(xedges, yedges, H)
        plt.colorbar()
        plt.xlim(0, MTU)
        plt.ylim(0, MTU)
        plt.set_cmap('binary')
        plt.show()
    return H.astype(np.uint16)
