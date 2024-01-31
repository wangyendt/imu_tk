# coding: utf-8


import numpy as np
import matplotlib.pyplot as plt
import re


path = r'./data/static_samples.txt'
data = np.loadtxt(path, delimiter=',')
print(data.shape)
ts = data[:,1]
ts -= ts[0]
acc = data[:,2:]
print(ts.shape, acc.shape)

# acc_params_path = './bin/result/mercury_manual/imu_5/test_imu_acc.calib'
acc_params_path = './bin/result/mercury_arm/imu_2/test_imu_acc.calib'
with open(acc_params_path, 'r') as f:
	lines = [[float(d) for d in re.split('\s+', l.strip())] for l in map(str.strip, f.readlines()) if l]
	print(lines)
	T = np.array(lines[:3])
	K = np.array(lines[3:6])
	b = np.array(lines[6:9])
	print(T,K,b)
	print(T.shape,K.shape,b.shape)
acc_calibrated = (T@K@(acc.T-b)).T
uncalibrated_acc_std_norm = np.linalg.norm(acc, axis=1)
calibrated_acc_std_norm = np.linalg.norm(acc_calibrated, axis=1)

plt.subplot(211)
plt.title('rawdata-acc')
plt.plot(ts, acc, 'o')
plt.legend(('x','y','z'))
plt.xlabel('Time (s)')
plt.ylabel('$m/s^2$')
plt.grid(True)
plt.subplot(212)
plt.title(f'uncalibrated_acc.std={np.std(uncalibrated_acc_std_norm,ddof=1):.6f}, calibrated_acc.std={np.std(calibrated_acc_std_norm,ddof=1):.6f}')
plt.scatter(ts, uncalibrated_acc_std_norm)
plt.scatter(ts, calibrated_acc_std_norm)
plt.grid(True)
plt.xlabel('Time (s)')
plt.ylabel('$m/s^2$')
plt.show()
