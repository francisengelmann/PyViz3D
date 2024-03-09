import pyviz3d.visualizer as viz
import numpy as np


def main():
    v = viz.Visualizer()
    # Add arrow given start and end position
    v.add_arrow('Arrow_1',
                start=np.array([0.0, 0.2, 0.0]),
                end=np.array([1, 0.2, 0]))
    # Specify the color of the arrow (default is red)
    v.add_arrow('Arrow_2',
                start=np.array([0.0, 0.0, 0.0]),
                end=np.array([0.5, 0, 0.5]),
                color=np.array([0, 0, 255]))
    # Specify the width of the stroke, and width of the arrow head as well as its transparency
    v.add_arrow('Arrow_3',
                start=np.array([0, 1, 0]),
                end=np.array([1, 1, 1]),
                color=np.array([30, 255, 50]),
                alpha=0.5,
                stroke_width=0.04,
                head_width=0.1)
    v.save('example_arrows')

if __name__ == '__main__':
    main()
