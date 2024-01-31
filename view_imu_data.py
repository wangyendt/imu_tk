# author: wangye(Wayne)
# license: Apache Licence
# file: view_imu_data.py
# time: 2024-01-13-20:52:17
# contact: wang121ye@hotmail.com
# site:  wangyendt@github.com
# software: PyCharm
# code is far away from bugs.


from pywayne.tools import list_all_files
import os
import numpy as np
import matplotlib.pyplot as plt


def main():
    # data_root = './bin/test_data/mercury_manual/imu_1'
    # data_root = './bin/test_data/mercury_arm/imu_10'
    data_root = './bin/test_data/aitexun/20240130_field_validation/imutk_manual_soft_bed_test1'
    acc_data = np.loadtxt(os.path.join(data_root, 'acc.mat'))
    gyro_data = np.loadtxt(os.path.join(data_root, 'gyro.mat'))
    print(acc_data.shape)
    print(gyro_data.shape)
    ts_acc = acc_data[:, 0]
    acc = acc_data[:, 1:]
    ts_gyro = gyro_data[:, 0]
    gyro = gyro_data[:, 1:]

    for i in range(200):
        interval_indices = np.ones((len(ts_acc), 1))
        interval_file = f'./data/{i}_static_intervals.txt'
        if not os.path.exists(interval_file): continue
        intervals = np.loadtxt(interval_file, delimiter=',').astype(int)
        for s, e in intervals:
            interval_indices[s:e+1] = 0
        print(interval_indices.shape)
        print(ts_acc[np.where(np.diff(interval_indices, axis=0) == 1)[0]])
        print(len(np.where(np.diff(interval_indices, axis=0) == 1)[0]))
        fig, ax = plt.subplots(2, 1, sharex='all')
        plt.suptitle(f'interval {i}')
        ax[0].plot(ts_acc, acc)
        ax[0].plot(ts_acc, interval_indices * (np.max(acc) - np.min(acc)) + np.min(acc))
        ax[0].set_title('acc')
        ax[0].set_ylabel('$m/s^2$')
        ax[1].plot(ts_gyro, gyro)
        ax[1].plot(ts_gyro, interval_indices * (np.max(gyro) - np.min(gyro)) + np.min(gyro))
        ax[1].set_title('gyro')
        ax[1].set_xlabel('Time: (s)')
        ax[1].set_ylabel('rad/s')
        plt.show()


if __name__ == '__main__':
    main()
