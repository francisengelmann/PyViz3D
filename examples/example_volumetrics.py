import pyviz3d.visualizer as viz
import numpy as np
import math


def main():
    v = viz.Visualizer()
    v.add_arrow('Arrow_1', start=np.array([0, 0.2, 0]), end=np.array([1, 0.2, 0]))
    v.add_arrow('Arrow_2', start=np.array([0, 0.5, 0.5]), end=np.array([0.5, 0, 0.5]), color=np.array([0, 0, 255]))
    v.add_arrow('Arrow_3', start=np.array([0, 1, 0]), end=np.array([1, 1, 1]), color=np.array([30, 255, 50]),
                           alpha=0.5, stroke_width=0.04, head_width=0.1)

    v.save('example_arrows')


if __name__ == '__main__':
    main()
