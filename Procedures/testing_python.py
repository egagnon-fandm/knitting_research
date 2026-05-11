import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import cv2

x_axis = np.linspace(0,10,1000)
y_axis = np.cos(2*np.pi*x_axis/0.5)

dx = x_axis[1]-x_axis[0]
x_axis_fft = sp.fft.fftshift(sp.fft.fftfreq(x_axis.size,d=dx))
y_axis_fft = sp.fft.fftshift(sp.fft.fft(y_axis))

fig = plt.figure()
ax1 = fig.add_subplot(121)
ax1.plot(x_axis, y_axis)
ax2 = fig.add_subplot(122)
ax2.plot(x_axis_fft, np.abs(y_axis_fft))

plt.show()
