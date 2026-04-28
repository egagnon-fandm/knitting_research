# Node position analysis

A collection of python scripts to do manual node position analysis.

- node_position_tracking.py: Picture analysis of knitted swatches being stretched. For a selected number of stitches, mark with the mouse 7 positions: the beginning of the stitch, the first crossover point, the second crossover point, the top of the stitch, the third crossover point, the fourth crossover point, and the end of the stitch. The points are saved to file.
- node_position_analysis.py: Imports the data from the previous script and performs basic statistics on the results. Outputs average positions and error bars for each nodes.
- node_positions_plotting.py: Import the results of the analysis script and creates simple graphs.
- calibration.py: Looks at the ruler in the image with the swatch and calculates the number of points between a set distance.

