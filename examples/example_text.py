import numpy as np
import pyviz3d.visualizer as viz


def main():

    # First, we set up a visualizer
    v = viz.Visualizer()

    v.add_labels('Labels',
                 ['text_x', 'texty_y', 'text_z'],
                 [np.array([1.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0]), np.array([0.0, 0.0, 1.0])],
                 [np.array([255.0, 0.0, 0.0]), np.array([0.0, 255.0, 0.0]), np.array([0.0, 0.0, 255.0])],
                 visible=False)

    # When we added everything we need to the visualizer, we save it.
    v.save('example_text')


if __name__ == '__main__':
    main()
