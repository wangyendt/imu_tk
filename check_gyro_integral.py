# author: wangye(Wayne)
# license: Apache Licence
# file: check_gyro_integral.py
# time: 2024-01-27-17:57:25
# contact: wang121ye@hotmail.com
# site:  wangyendt@github.com
# software: PyCharm
# code is far away from bugs.


import matplotlib.pyplot as plt
from matplotlib.font_manager import FontManager
from pywayne.plot import *
import vqf
import qmt

fm = FontManager()
mat_fonts = set(f.name for f in fm.ttflist)
# print(mat_fonts)
# plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['font.sans-serif'] = ['FangSong']
# plt.rcParams['font.family'] = ['YouYuan']
plt.rcParams['axes.unicode_minus'] = False
from pywayne.tools import list_all_files
import collections
import numpy as np
import pandas as pd
import os
import re
import sys
import platform


def load_data(path):
    # param_file = './params/none.txt'
    # param_file = './params/with_jiaodian.txt'
    # param_file = sys.argv[1] if len(sys.argv) > 1 else './params/20240127_remote_validation/none.txt'
    # param_file = sys.argv[1] if len(sys.argv) > 1 else './params/20240127_remote_validation/with_jiaodian.txt'
    # param_file = sys.argv[1] if len(sys.argv) > 1 else './params/20240127_remote_validation/with_jiaodian_6x.txt'
    # param_file = sys.argv[1] if len(sys.argv) > 1 else './params/20240130_field_validation/imutk_arm_thick_jiaodian_right_test1.txt'
    # param_file = sys.argv[1] if len(sys.argv) > 1 else './params/20240130_field_validation/imutk_manual_test1.txt'
    # param_file = sys.argv[1] if len(sys.argv) > 1 else './params/20240130_field_validation/imutk_manual_soft_bed_test1.txt'
    param_file = sys.argv[1] if len(sys.argv) > 1 else './params/20240130_field_validation/imutk_arm_thick_jiaodian_right_locked_legfixed_test6.txt'
    print(f'{param_file=}')
    params = np.loadtxt(param_file)
    print(params.shape)
    T_g = params[:3]
    K_g = params[3:6]
    b_g = params[-1]
    print(f'{T_g=}')
    print(f'{K_g=}')
    print(f'{b_g=}')

    # files = list_all_files(path, ['IMU单向转720度震动测试数据3.txt', ''])
    # files = list_all_files(path, ['IMU正负720度厚胶垫测试数据1.txt', ''])
    # files = list_all_files(path, ['manual_check_10_rounds_test1.txt', ''])
    # files = list_all_files(path, ['manual_check_10_rounds_test2.txt', ''])
    # files = list_all_files(path, ['IMU正负720度垫硅胶镜腿固定1.txt', ''])
    # files = list_all_files(path, ['IMU正负720度垫硅胶镜腿固定2.txt', ''])
    files = list_all_files(path, ['IMU三位置720度旋转.txt', ''])
    # files = list_all_files(path, sys.argv[2:])
    for file in files:
        print(file)
        sensor_data = collections.defaultdict(list)
        sensor_data_npy = collections.defaultdict(np.array)
        # with open(file, 'r', encoding='UTF-16LE', errors='ignore') as f:
        with open(file, 'r', encoding='UTF-8', errors='ignore') as f:
            lines = f.readlines()
            print(len(lines))
            for i, line in enumerate(lines):
                line = line.strip()
                if not any(kw in line for kw in ('acc', 'gyro', 'mag')): continue
                if 'get response!!!!65' in line: continue
                sensor, data = re.findall(r'(.*) = (.*)', line)[0]
                sensor_data[sensor].append([float(d) for d in data.split(' ') if d])
        sensor_data_npy['acc'] = np.array(sensor_data['acc'])[:, :3]
        sensor_data_npy['gyro'] = np.array(sensor_data['gyro'])[:, :3]
        sensor_data_npy['mag'] = np.array(sensor_data['mag'])[:, :3]
        N = min(len(sensor_data_npy['acc']), len(sensor_data_npy['gyro']), len(sensor_data_npy['mag']))
        sensor_data_npy['acc'] = sensor_data_npy['acc'][:N]
        sensor_data_npy['gyro'] = sensor_data_npy['gyro'][:N]
        sensor_data_npy['mag'] = sensor_data_npy['mag'][:N]
        sensor_data_npy['ts'] = np.array(sensor_data['acc'])[:, 3]
        print(f"{sensor_data_npy['ts'][np.where(sensor_data_npy['mag'][:, 2] < -500)]=}")
        sensor_data_npy['ts'] -= sensor_data_npy['ts'][0]
        sensor_data_npy['ts'] /= 1e4

        acc = np.ascontiguousarray(sensor_data_npy['acc'])
        gyro = np.ascontiguousarray(sensor_data_npy['gyro'])
        mag = np.ascontiguousarray(sensor_data_npy['mag'])
        ts = np.ascontiguousarray(sensor_data_npy['ts'])

        b_g = np.mean(gyro[:2000], axis=0)

        gyro = (T_g @ K_g @ (gyro.T - b_g.reshape((3, 1)))).T
        # gyro = (gyro.T-b_g.reshape((3,1))).T
        gyro = np.ascontiguousarray(gyro)

        # acc_mat = np.c_[ts, acc]
        # gyro_mat = np.c_[ts, gyro]
        # np.savetxt(os.path.join(os.path.dirname(file),'acc.mat'),acc_mat)
        # np.savetxt(os.path.join(os.path.dirname(file),'gyro.mat'),gyro_mat)

        # for j in range(3):
        #     for i in range(1, len(mag)):
        #         if abs(mag[i, j] - mag[i - 1, j]) > 300:
        #             mag[i, j] = mag[i - 1, j]
        freq = int(1 / np.median(np.diff(ts)))
        print(freq)

        vqf3d = vqf.VQF(gyrTs=1 / freq)
        print(np.mean(gyro[:5 * freq], axis=0))
        # gyro -= np.mean(gyro[:5 * freq], axis=0)
        print(gyro.shape)
        ahrs = vqf3d.updateBatch(gyro, acc)
        q = qmt.quatFromGyrStrapdown(gyro, rate=freq, debug=True, plot=True)[0]
        print(q.shape)
        euler = qmt.eulerAngles(q)
        # start = euler[8600:9600] * 180 / np.pi # 机械臂第二次，IMU正负720度厚胶垫测试数据1
        # end = euler[13250:14250] * 180 / np.pi
        # start = euler[6500:7500] * 180 / np.pi # 机械臂第二次，IMU单向转720度震动测试数据3
        # end = euler[14400:15400] * 180 / np.pi
        start = euler[1400:2400] * 180 / np.pi # 手动第一次
        end = euler[24250:25250] * 180 / np.pi
        # start = euler[2400:3400] * 180 / np.pi # 手动第二次
        # end = euler[22500:23500] * 180 / np.pi
        # start = euler[10600:11600] * 180 / np.pi # IMU正负720度垫硅胶镜腿固定1
        # end = euler[18400:19400] * 180 / np.pi
        # start = euler[18000:19000] * 180 / np.pi # IMU正负720度垫硅胶镜腿固定2
        # end = euler[26000:27000] * 180 / np.pi
        print(np.mean(end, axis=0) - np.mean(start, axis=0))
        # plt.figure()
        # plt.plot(ts, q)
        # plt.show()
        exit()

        acc_static = acc[freq * 5:freq * 10]
        gyro_static = gyro[freq * 5:freq * 10]
        print(f'{np.std(acc_static, axis=0, ddof=1)=}m/s^2\n{np.max(acc_static, axis=0)-np.min(acc_static, axis=0)=}m/s^2')
        print(f'{np.std(gyro_static, axis=0, ddof=1)=}rad/s\n{np.max(gyro_static, axis=0)-np.min(gyro_static, axis=0)=}rad/s')

        win_time = 8
        step_time = 1
        fs = freq
        regist_projection()

        plt.figure()
        plt.subplot(321, projection='z_norm')
        plt.specgram(x=acc[:40 * fs, 0], Fs=fs, NFFT=win_time * fs, noverlap=(win_time - step_time) * fs, cmap=parula_map, mode='magnitude', scale='linear', scale_by_freq=True)
        plt.ylim([60, 90])
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.subplot(323, projection='z_norm')
        plt.specgram(x=acc[:40 * fs, 1], Fs=fs, NFFT=win_time * fs, noverlap=(win_time - step_time) * fs, cmap=parula_map, mode='magnitude', scale='linear', scale_by_freq=True)
        plt.ylim([60, 90])
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.subplot(325, projection='z_norm')
        plt.specgram(x=acc[:40 * fs, 2], Fs=fs, NFFT=win_time * fs, noverlap=(win_time - step_time) * fs, cmap=parula_map, mode='magnitude', scale='linear', scale_by_freq=True)
        plt.ylim([60, 90])
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.subplot(322, projection='z_norm')
        plt.specgram(x=gyro[:40 * fs, 0], Fs=fs, NFFT=win_time * fs, noverlap=(win_time - step_time) * fs, cmap=parula_map, mode='magnitude', scale='linear', scale_by_freq=True)
        plt.ylim([60, 90])
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.subplot(324, projection='z_norm')
        plt.specgram(x=gyro[:40 * fs, 1], Fs=fs, NFFT=win_time * fs, noverlap=(win_time - step_time) * fs, cmap=parula_map, mode='magnitude', scale='linear', scale_by_freq=True)
        plt.ylim([60, 90])
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.subplot(326, projection='z_norm')
        plt.specgram(x=gyro[:40 * fs, 2], Fs=fs, NFFT=win_time * fs, noverlap=(win_time - step_time) * fs, cmap=parula_map, mode='magnitude', scale='linear', scale_by_freq=True)
        plt.ylim([60, 90])
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.suptitle(file)
        # plt.show()
        # exit()

        fig, ax = plt.subplots(2, 1, sharex='all')
        plt.suptitle(file)
        ax[0].plot(ts, acc)
        ax[0].legend(('x', 'y', 'z'))
        ax[0].grid(True)
        ax[0].set_ylabel('$m/s^2$')
        ax[0].set_title('ACC')
        ax[1].plot(ts, gyro)
        ax[1].legend(('x', 'y', 'z'))
        ax[1].grid(True)
        ax[1].set_ylabel('rad/s')
        ax[1].set_xlabel('Time: (s)')
        ax[1].set_title('GYRO')
        plt.tight_layout()
        plt.figure()
        plt.suptitle(file)
        # plt.subplot(311)
        # plt.plot(ts, acc)
        # plt.subplot(312)
        # plt.plot(ts, gyro)
        # plt.subplot(313)
        plt.subplot(211)
        plt.title('mag-rawdata')
        plt.plot(ts, mag)
        plt.grid(True)
        plt.ylabel('(µT)')
        plt.subplot(212)
        plt.title('mag-norm')
        plt.plot(ts, np.linalg.norm(mag, axis=1))
        plt.grid(True)
        plt.xlabel('time(s)')
        plt.ylabel('(µT)')
        plt.tight_layout()
        plt.show()


def main():
    # path = '/media/psf/work/data/ost_calibration/imu_intrinsic/imu_tk/mercury_arm/aitexun' #/IMU震动测试数据1.txt'
    # path = '/Users/Wayne/Documents/work/data/ost_calibration/imu_intrinsic/imu_tk/mercury_arm/aitexun'  # /IMU震动测试数据1.txt'
    path = '/Users/Wayne/Documents' if platform.system() == 'Darwin' else '/media/psf' + '/work/data/ost_calibration/imu_intrinsic/imu_tk/mercury_arm/aitexun' #/IMU震动测试数据1.txt'
    load_data(path)


if __name__ == '__main__':
    main()
