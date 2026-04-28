from csv import reader

import matplotlib.pyplot as plt
import numpy as np

f = "3.0"

# Input file name
in_file = "./Node_positions_D_S1_F_" + f + ".dat"

# Output file name
out_file = "./Node_position_analysis_D_S1_F_" + f + ".dat"


def calc_s_dist(x_axis, y_axis):
    s = 0.0
    for i in range(1, x_axis.size):
        s = s + np.sqrt(
            (x_axis[i] - x_axis[i - 1]) ** 2 + (y_axis[i] - y_axis[i - 1]) ** 2
        )
    return s


if __name__ == "__main__":
    # Initialize an empty coordinate array
    coordinates = []

    with open(in_file, newline="") as myfile:
        for row in reader(myfile, delimiter="\t"):
            coordinates.append(row)

    num_points = len(coordinates)
    x_axis = np.zeros((num_points, 7))
    y_axis = np.zeros((num_points, 7))
    for i in range(num_points):
        for j in range(7):
            x_axis[i, j] = int(coordinates[i][j].split("(")[1].split(",")[0])
            y_axis[i, j] = int(coordinates[i][j].split(",")[1].split(")")[0])

    # s position of markers along the yarn
    s = np.zeros((num_points, 7))
    for i in range(num_points):
        for j in range(7):
            s[i, j] = calc_s_dist(x_axis[i, 0 : (j + 1)], y_axis[i, 0 : (j + 1)])

    # Find the absolute and relative position of the nodes
    first_node_pos = np.zeros(num_points)
    second_node_pos = np.zeros(num_points)
    third_node_pos = np.zeros(num_points)
    fourth_node_pos = np.zeros(num_points)

    dist_first_second_nodes = np.zeros(num_points)
    dist_third_fourth_nodes = np.zeros(num_points)

    for i in range(num_points):
        first_node_pos[i] = s[i, 1] - s[i, 0]
        second_node_pos[i] = s[i, 2] - s[i, 0]
        third_node_pos[i] = s[i, 4] - s[i, 0]
        fourth_node_pos[i] = s[i, 5] - s[i, 0]
        dist_first_second_nodes[i] = s[i, 2] - s[i, 1]
        dist_third_fourth_nodes[i] = s[i, 5] - s[i, 4]

    output = np.zeros(14)
    output[0] = np.mean(first_node_pos)
    output[1] = np.std(first_node_pos)
    output[2] = np.mean(second_node_pos)
    output[3] = np.std(second_node_pos)
    output[4] = np.mean(third_node_pos)
    output[5] = np.std(third_node_pos)
    output[6] = np.mean(fourth_node_pos)
    output[7] = np.std(fourth_node_pos)
    output[8] = np.mean(dist_first_second_nodes)
    output[9] = np.std(dist_first_second_nodes)
    output[10] = np.mean(dist_third_fourth_nodes)
    output[11] = np.std(dist_third_fourth_nodes)
    output[12] = np.mean(s[:, -1])
    output[13] = np.std(s[:, -1])

    np.savetxt(out_file, output)
