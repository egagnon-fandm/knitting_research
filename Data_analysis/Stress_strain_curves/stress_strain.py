import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

"""
Create the reference dictionary. The keys to the dictionary are labels used to
identify the datasets within the script.

"2p0_1": First run of gauge 2.0
"2p0_2": Second run of gauge 2.0
etc.

The value of each entry is itself a dictionary with a set of keys:
- "files": Location of the data file on your computer
- "Stretch/Relax force": 2D (see below) lists of force values during the
                stretching/relaxing cycle. Values are read in directly from
                data file. Starts empty and is populated below.
- "Stretch/Relax position": Same as "Stretch/Relax force" but recording the
                motor positions matching the individual force reading.
- "Init distance fla/pict": Length of the sample when laying flat on the
                table/hanging in the machine with a ruler next to it in mm.
- "Width": Width of the sample in mm.
- "Stretch/Relax strain": 2D calculated strain from position and init distance.
                Starts empty.
- "Stretch/Relax stress": 2D calculated stress from force and width.
- "Gauge": Gauge of the knitted pattern. Used in labels. String.
- "Mass": Mass of the swatch in grams.
- "Num st course/wale": Number of stitches along the course/wale direction.
- "Num runs": Number of stretch/relax cycles in the dataset
- "Stretch/Relax stress fit": 2D structures to fit results to "fit_func".
- "Stretch/Relax modulus: 2D structures that records the value of the tangent
            modulus.


2D structures:
    - First dimension selects which run to consider.
    - Second dimension selects the element of a particular run.
    - Ex.: data_info["Stretch stress"][1][:] selects all the elements (:) of
            the stress values during the stretch cycle of the second (1) run.
"""
data_info = {
    "2p0_1": {
        "file": "/home/etienne/Documents/Research/Data/2025/2025_12_11/scan_2p0_b.dat",
        "Stretch force": [],
        "Relax force": [],
        "Stretch position": [],
        "Relax position": [],
        "Init distance flat": 210,
        "Init distance pict": 212,
        "Width": 114,
        "Stretch strain": [],
        "Stretch stress": [],
        "Relax strain": [],
        "Relax stress": [],
        "Gauge": "2",
        "Mass": 12.2,
        "Num st course": 54,
        "Num st wale": 46,
        "Num runs": 1,
        "Stretch stress fit": [],
        "Relax stress fit": [],
        "Stretch modulus": [],
        "Relax modulus": [],
    },
    "2p0_2": {
        "file": "/home/etienne/Documents/Research/Data/2025/2025_12_11/scan_2p0_c.dat",
        "Stretch force": [],
        "Relax force": [],
        "Stretch position": [],
        "Relax position": [],
        "Init distance flat": 210,
        "Init distance pict": 213,
        "Width": 123,
        "Stretch strain": [],
        "Stretch stress": [],
        "Relax strain": [],
        "Relax stress": [],
        "Gauge": "2",
        "Mass": 12.19,
        "Num st course": 54,
        "Num st wale": 46,
        "Num runs": 1,
        "Stretch stress fit": [],
        "Relax stress fit": [],
        "Stretch modulus": [],
        "Relax modulus": [],
    },
}


# Find the index of value in ordered list
def find_val_index(list, val, asc=True):
    index = 0
    for i in range(len(list)):
        # For lists with values in ascending order
        if asc and list[i] > val:
            index = i
            break

        # For lists with values in descending order
        if (not asc) and list[i] < val:
            index = i
            break

    return index


# Force value associated to zero strain
MIN_FORCE = 0.1

# Create a strain array for interpolation
N_fit = 100  # Number of points
low_lim_fit = 0.0  # Lower limit to strain in fit
high_lim_fit = 0.0  # Higher limit to strain in fit
strain_fit = np.linspace(low_lim_fit, high_lim_fit, N_fit)


# Function to create Stretch/Relax stress fit.
def fit_func(x, a, b, c, d, e):
    return a * x**4 + b * x**3 + c * x**2 + d * x + e


# Load data and fill out the lists in the data dictionary
for run in data_info:
    # Load data and discard first data point
    scan_data = np.loadtxt(data_info[run]["file"])[1:]
    scan_data[:, 0] = -scan_data[:, 0]  # Invert the sign on the position
    scan_data[:, 0] = scan_data[:, 0] * 1000  # Convert to mm

    # Num of points in each stretch and relax runs
    num_runs = data_info[run]["Num runs"]
    num_points = scan_data[:, 0].size // (2 * num_runs)

    # Save stretch and relax runs to dictionary list
    for j in range(num_runs):
        data_info[run]["Stretch position"].append(
            scan_data[2 * j * num_points : (2 * j + 1) * num_points, 0]
        )
        data_info[run]["Stretch force"].append(
            scan_data[2 * j * num_points : (2 * j + 1) * num_points, 1]
        )

        data_info[run]["Relax position"].append(
            scan_data[(2 * j + 1) * num_points : 2 * (j + 1) * num_points, 0]
        )
        data_info[run]["Relax force"].append(
            scan_data[(2 * j + 1) * num_points : 2 * (j + 1) * num_points, 1]
        )

    # Calculate strain and save to dictionary list
    for j in range(num_runs):
        zero_pos_index = find_val_index(
            data_info[run]["Stretch force"][j], MIN_FORCE, asc=True
        )
        zero_pos = data_info[run]["Stretch position"][j][zero_pos_index]

        init_distance = data_info[run]["Init distance flat"]

        strain = [
            (pos - zero_pos) / init_distance
            for pos in data_info[run]["Stretch position"][j]
        ]

        data_info[run]["Stretch strain"].append(strain)

        strain = [
            (pos - zero_pos) / init_distance
            for pos in data_info[run]["Relax position"][j]
        ]
        data_info[run]["Relax strain"].append(strain)

    # Calculate stress and save to dictionary list
    for j in range(num_runs):
        stress = [
            force / data_info[run]["Width"]
            for force in data_info[run]["Stretch force"][j]
        ]
        data_info[run]["Stretch stress"].append(stress)

        stress = [
            force / data_info[run]["Width"]
            for force in data_info[run]["Relax force"][j]
        ]
        data_info[run]["Relax stress"].append(stress)

    # Calculate the fitted stress
    for j in range(num_runs):
        popt, pcov = curve_fit(
            fit_func,
            data_info[run]["Stretch strain"][j],
            data_info[run]["Stretch stress"][j],
        )
        stress = [
            fit_func(strain, popt[0], popt[1], popt[2], popt[3], popt[4])
            for strain in strain_fit
        ]
        data_info[run]["Stretch stress fit"].append(stress)

        popt, pcov = curve_fit(
            fit_func,
            data_info[run]["Relax strain"][j],
            data_info[run]["Relax stress"][j],
        )
        stress = [
            fit_func(strain, popt[0], popt[1], popt[2], popt[3], popt[4])
            for strain in strain_fit
        ]
        data_info[run]["Relax stress fit"].append(stress)

    # Calculate the modulus
    for j in range(num_runs):
        modulus = [
            stress / strain
            for stress, strain in zip(
                data_info[run]["Stretch stress"][j], data_info[run]["Stretch strain"][j]
            )
        ]
        data_info[run]["Stretch modulus"].append(modulus)

        modulus = [
            stress / strain
            for stress, strain in zip(
                data_info[run]["Relax stress"][j], data_info[run]["Relax strain"][j]
            )
        ]
        data_info[run]["Relax modulus"].append(modulus)


## Example plotting
fig2 = plt.figure(figsize=(10, 5))  # Create a figure
ax2 = fig2.add_subplot(111)  # Create axes on figure
ax2.plot(  # Stress vs strain of first run of first dataset
    data_info["2p0_1"]["Stretch strain"][0],
    data_info["2p0_1"]["Stretch stress"][0],
    linestyle="dashed",
    color="r",
    label="Gauge= 2",
)
ax2.plot(  # Stress vs strain of first run of second dataset
    data_info["2p0_2"]["Stretch strain"][0],
    data_info["2p0_2"]["Stretch stress"][0],
    linestyle="dashed",
    color="r",
)
ax2.legend(loc="upper left")
ax2.set_xlabel("Strain")
ax2.set_ylabel("Stress (N/mm)")

fig2.savefig("./Saved_file_name.png")

plt.show()
