import numpy as np
import matplotlib.pyplot as plt

data_1 = np.zeros((5,14))
data_1[0,:] = np.loadtxt("./Node_position_analysis_D_F_0.1.dat")
data_1[1,:] = np.loadtxt("./Node_position_analysis_D_F_1.0.dat")
data_1[2,:] = np.loadtxt("./Node_position_analysis_D_F_2.0.dat")
data_1[3,:] = np.loadtxt("./Node_position_analysis_D_F_3.0.dat")
data_1[4,:] = np.loadtxt("./Node_position_analysis_D_F_4.0.dat")

data_2 = np.zeros((4,14))
data_2[0,:] = np.loadtxt("./Node_position_analysis_D_S1_F_0.1.dat")
data_2[1,:] = np.loadtxt("./Node_position_analysis_D_S1_F_1.0.dat")
data_2[2,:] = np.loadtxt("./Node_position_analysis_D_S1_F_2.0.dat")
data_2[3,:] = np.loadtxt("./Node_position_analysis_D_S1_F_3.0.dat")

length_1 = np.copy(data_1[:,-2])
dlength_1 = np.copy(data_1[:,-1])
length_2 = np.copy(data_2[:,-2])
dlength_2 = np.copy(data_2[:,-1])

for i in range(5):
    data_1[i,:] = data_1[i,:]/data_1[i,-2]
for i in range(4):
    data_2[i,:] = data_2[i,:]/data_2[i,-2]

force_1 = np.array([0.1, 1.0, 2.0, 3.0, 4.0])
force_2 = np.array([0.1, 1.0, 2.0, 3.0])

factor = np.sqrt(60)

fig1 = plt.figure(figsize=(10,10))
ax1a = fig1.add_subplot(221)
ax1a.errorbar(
    force_1,
    data_1[:,0],
    yerr=data_1[:,1]/factor,
    fmt="o",
    markersize=5,
    color="r",
    capsize=10,
    label="blocked"
)
ax1a.errorbar(
    force_2,
    data_2[:,0],
    yerr=data_2[:,1]/factor,
    fmt="o",
    markersize=5,
    color="b",
    capsize=10,
    label="rested"
)
ax1a.legend(loc='upper left')

ax1b = fig1.add_subplot(222)
ax1b.errorbar(
    force_1,
    data_1[:,2],
    yerr=data_1[:,3]/factor,
    fmt="o",
    markersize=5,
    color="r",
    capsize=10,
    label="blocked"
)
ax1b.errorbar(
    force_2,
    data_2[:,2],
    yerr=data_2[:,3]/factor,
    fmt="o",
    markersize=5,
    color="b",
    capsize=10,
    label="rested"
)
ax1b.legend(loc='upper right')

ax1c = fig1.add_subplot(223)
ax1c.errorbar(
    force_1,
    data_1[:,4],
    yerr=data_1[:,5]/factor,
    fmt="o",
    markersize=5,
    color="r",
    capsize=10,
    label="blocked"
)
ax1c.errorbar(
    force_2,
    data_2[:,4],
    yerr=data_2[:,5]/factor,
    fmt="o",
    markersize=5,
    color="b",
    capsize=10,
    label="rested"
)
ax1c.legend(loc='upper left')

ax1d = fig1.add_subplot(224)
ax1d.errorbar(
    force_1,
    data_1[:,6],
    yerr=data_1[:,7]/factor,
    fmt="o",
    markersize=5,
    color="r",
    capsize=10,
    label="blocked"
)
ax1d.errorbar(
    force_2,
    data_2[:,6],
    yerr=data_2[:,7]/factor,
    fmt="o",
    markersize=5,
    color="b",
    capsize=10,
    label="rested"
)
ax1d.legend(loc='upper right')

fig1.savefig("./B_sample_NPA.png")

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.errorbar(
    force_1,
    length_1,
    yerr=dlength_1/factor,
    fmt="o",
    markersize=5,
    color="r",
    capsize=10,
    label="blocked",
)
ax2.errorbar(
    force_2,
    length_2,
    yerr=dlength_2/factor,
    fmt="o",
    markersize=5,
    color="b",
    capsize=10,
    label="rested",
)
ax2.legend(loc='upper left')

fig2.savefig("./length_init.png")


fig3 = plt.figure()
ax3 = fig3.add_subplot(111)
ax3.errorbar(
    force_1,
    length_1,
    yerr=dlength_1/factor,
    fmt="o",
    markersize=5,
    color="r",
    capsize=10,
    label="blocked",
)
ax3.errorbar(
    force_2,
    length_2/1.5,
    yerr=dlength_2/factor/1.5,
    fmt="o",
    markersize=5,
    color="b",
    capsize=10,
    label="rested",
)
ax3.legend(loc='upper left')

fig3.savefig("./length.png")
plt.show()
