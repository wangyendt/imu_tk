# author: wangye(Wayne)
# license: Apache Licence
# file: detect_static_intervals.py
# time: 2024-01-15-21:02:17
# contact: wang121ye@hotmail.com
# site:  wangyendt@github.com
# software: PyCharm
# code is far away from bugs.


from pywayne.tools import list_all_files
from pywayne.dsp import CalcEnergy, peak_det
import os
import numpy as np
import matplotlib.pyplot as plt


def main():
    data_root = './bin/test_data'
    kw = 'mercury_manual/imu_1'
    acc_data = np.loadtxt(os.path.join(data_root, kw, 'acc.mat'))
    gyro_data = np.loadtxt(os.path.join(data_root, kw, 'gyro.mat'))
    print(acc_data.shape)
    print(gyro_data.shape)
    ts_acc = acc_data[:, 0]
    acc = acc_data[:, 1:]
    ts_gyro = gyro_data[:, 0]
    gyro = gyro_data[:, 1:]
    energy = CalcEnergy(alpha=100, beta=200)
    eng = energy.apply(acc)
    eng_max = np.max(np.abs(eng), axis=1)
    moving = np.zeros((eng_max.shape[0], 1))
    start, end = [], []
    for i in range(1, eng_max.shape[0]):
        # print(eng_max[i])
        if moving[i - 1] == 0 and eng_max[i] > 0.6:
            moving[i] = 1
            start.append(i - 500)
        elif moving[i - 1] == 1 and eng_max[i] < 0.2:
            moving[i] = 0
            end.append(i + 200)
        else:
            moving[i] = moving[i - 1]
    moving_real = np.zeros_like(moving)
    print(len(start), len(end))
    os.makedirs(os.path.join('debug', kw), exist_ok=True)
    with open(os.path.join('debug', kw, 'static_intervals.txt'), 'w') as f:
        for s, e in zip(start, end):
            moving_real[s:e] = 1
            f.write(f'{s},{e}\n')
    plt.figure()
    plt.plot(eng_max)
    plt.plot(moving_real * (eng_max.max() - eng_max.min()) + eng_max.min())
    plt.figure()
    plt.subplot(211)
    plt.plot(ts_acc, acc)
    plt.plot(ts_acc, moving_real * (np.max(acc) - np.min(acc)) + np.min(acc))
    plt.subplot(212)
    plt.plot(ts_gyro, gyro)
    plt.plot(ts_gyro, moving_real * (np.max(gyro) - np.min(gyro)) + np.min(gyro))
    plt.show()


if __name__ == '__main__':
    main()
