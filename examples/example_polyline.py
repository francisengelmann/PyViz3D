import pyviz3d.visualizer as viz
import numpy as np
import json

colors = {'A_WALL': [255, 0, 0], 'A_DOOR': [0, 255, 0], 'A_FLOR_STRS': [0, 0, 255]}


def main():
    with open('./examples/data/01_OfficeLab_01_F1_floorplan.txt') as json_file:
        data = json.load(json_file)
    num_layers = data['header']['layer number']

    v = viz.Visualizer()
    for j in range(num_layers):
        for i, structure in enumerate(data['layer '+str(j)]['points']):
            points = np.reshape(structure['coordinates'], [-1, 2])
            points = np.concatenate((points, np.zeros([points.shape[0], 1])), axis=1)
            color = np.array(colors[data['layer '+str(j)]['layer name']])
            v.add_polyline('Polyline' + str(i), positions=points, edge_width=0.04, color=color)
    v.save('example_polyline')


if __name__ == '__main__':
    main()
