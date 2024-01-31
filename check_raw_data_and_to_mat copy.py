# author: wangye(Wayne)
# license: Apache Licence
# file: check_raw_data.py
# time: 2024-01-02-14:03:08
# contact: wang121ye@hotmail.com
# site:  wangyendt@github.com
# software: PyCharm
# code is far away from bugs.


import matplotlib.pyplot as plt
from matplotlib.font_manager import FontManager
from pywayne.plot import *
from pywayne.dsp import *
import platform

fm = FontManager()
mat_fonts = set(f.name for f in fm.ttflist)
# print(mat_fonts)
# plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
# plt.rcParams['font.sans-serif'] = ['FangSong']
# plt.rcParams['font.family'] = ['YouYuan']
# plt.rcParams['axes.unicode_minus']=False
from pywayne.tools import list_all_files
import collections
import numpy as np
import pandas as pd
import os
import re
import sys


def load_data(path,date='20240130_field_validation',
    keyword='imutk_arm_thick_jiaodian_right_locked_test5',
    kw="IMU垫硅胶6轴锁紧5"):
    # files = list_all_files(path, ['底座加胶垫',''])
    # files = list_all_files(path, ['IMU全流程震动测试数据4（底座和六轴加胶垫）.txt',''])
    files = list_all_files(path, [kw])
    save_root = os.path.join('./bin/test_data/aitexun', date, keyword) if len(sys.argv) > 1 else ''
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
        print(acc.shape, gyro.shape, ts.shape, mag.shape)

        if 'IMU垫硅胶6轴锁紧4' in file:
            print('aaaaaaaaaa')
            s = 920
            acc = acc[s:]
            gyro = gyro[s:]
            mag = mag[s:]
            ts = ts[s:]
            ts -= ts[0]
        print(acc.shape, gyro.shape, ts.shape, mag.shape)
        
        acc_mat = np.c_[ts, acc]
        gyro_mat = np.c_[ts, gyro]
        print(f'{save_root=}')
        # if save_root:
        #     np.savetxt(os.path.join(save_root,'acc.mat'),acc_mat)
        #     np.savetxt(os.path.join(save_root,'gyro.mat'),gyro_mat)
        # else:
        #     np.savetxt(os.path.join(os.path.dirname(file),'acc.mat'),acc_mat)
        #     np.savetxt(os.path.join(os.path.dirname(file),'gyro.mat'),gyro_mat)
        # for j in range(3):
        #     for i in range(1, len(mag)):
        #         if abs(mag[i, j] - mag[i - 1, j]) > 300:
        #             mag[i, j] = mag[i - 1, j]
        freq = int(1/np.median(np.diff(ts)))
        print(freq)
        # acc = butter_bandpass_filter(acc, order=2, lo=200, fs=freq, btype='lowpass')
        # gyro = butter_bandpass_filter(gyro, order=2, lo=200, fs=freq, btype='lowpass')

        acc_static = acc[freq*5:freq*10]
        gyro_static = gyro[freq*5:freq*10]
        print(f'{np.std(acc_static, axis=0, ddof=1)=}m/s^2\n{np.max(acc_static, axis=0)-np.min(acc_static, axis=0)=}m/s^2')
        print(f'{np.std(gyro_static, axis=0, ddof=1)=}rad/s\n{np.max(gyro_static, axis=0)-np.min(gyro_static, axis=0)=}rad/s')

        win_time = 8
        step_time = 1
        fs = freq
        regist_projection()
        freq_min, freq_max = 0, 200

        # plt.figure()
        # plt.subplot(321, projection='z_norm')
        # plt.specgram(x=acc[:400*fs,0], Fs=fs, NFFT=win_time * fs, noverlap=(win_time - step_time) * fs, cmap=parula_map, mode='magnitude', scale='linear', scale_by_freq=True)
        # plt.ylim([freq_min, freq_max])
        # plt.xlabel('Time (s)')
        # plt.ylabel('Frequency (Hz)')
        # plt.subplot(323, projection='z_norm')
        # plt.specgram(x=acc[:400*fs,1], Fs=fs, NFFT=win_time * fs, noverlap=(win_time - step_time) * fs, cmap=parula_map, mode='magnitude', scale='linear', scale_by_freq=True)
        # plt.ylim([freq_min, freq_max])
        # plt.xlabel('Time (s)')
        # plt.ylabel('Frequency (Hz)')
        # plt.subplot(325, projection='z_norm')
        # plt.specgram(x=acc[:400*fs,2], Fs=fs, NFFT=win_time * fs, noverlap=(win_time - step_time) * fs, cmap=parula_map, mode='magnitude', scale='linear', scale_by_freq=True)
        # plt.ylim([freq_min, freq_max])
        # plt.xlabel('Time (s)')
        # plt.ylabel('Frequency (Hz)')
        # plt.subplot(322, projection='z_norm')
        # plt.specgram(x=gyro[:400*fs,0], Fs=fs, NFFT=win_time * fs, noverlap=(win_time - step_time) * fs, cmap=parula_map, mode='magnitude', scale='linear', scale_by_freq=True)
        # plt.ylim([freq_min, freq_max])
        # plt.xlabel('Time (s)')
        # plt.ylabel('Frequency (Hz)')
        # plt.subplot(324, projection='z_norm')
        # plt.specgram(x=gyro[:400*fs,1], Fs=fs, NFFT=win_time * fs, noverlap=(win_time - step_time) * fs, cmap=parula_map, mode='magnitude', scale='linear', scale_by_freq=True)
        # plt.ylim([freq_min, freq_max])
        # plt.xlabel('Time (s)')
        # plt.ylabel('Frequency (Hz)')
        # plt.subplot(326, projection='z_norm')
        # plt.specgram(x=gyro[:400*fs,2], Fs=fs, NFFT=win_time * fs, noverlap=(win_time - step_time) * fs, cmap=parula_map, mode='magnitude', scale='linear', scale_by_freq=True)
        # plt.ylim([freq_min, freq_max])
        # plt.xlabel('Time (s)')
        # plt.ylabel('Frequency (Hz)')
        # plt.suptitle(file)
        # plt.show()
        # exit()


        plt.suptitle(file)
        ax[0].plot(ts, acc)
        ax[0].legend(('x','y','z'))
        ax[0].grid(True)
        ax[0].set_ylabel('$m/s^2$')
        ax[0].set_title('ACC')
        ax[1].plot(ts, gyro)
        ax[1].legend(('x','y','z'))
        ax[1].grid(True)
        ax[1].set_ylabel('rad/s')
        ax[1].set_xlabel('Time: (s)')
        ax[1].set_title('GYRO')
        # plt.tight_layout()
        # plt.figure()
        # plt.suptitle(file)
        # # plt.subplot(311)
        # # plt.plot(ts, acc)
        # # plt.subplot(312)
        # # plt.plot(ts, gyro)
        # # plt.subplot(313)
        # plt.subplot(211)
        # plt.title('mag-rawdata')
        # plt.plot(ts, mag)
        # plt.grid(True)
        # plt.ylabel('(µT)')
        # plt.subplot(212)
        # plt.title('mag-norm')
        # plt.plot(ts, np.linalg.norm(mag, axis=1))
        # plt.grid(True)
        # plt.xlabel('time(s)')
        # plt.ylabel('(µT)')
        # plt.tight_layout()


# def main():
    # path = '/media/psf/work/data/ost_calibration/imu_intrinsic/imu_tk/mercury_arm/aitexun' #/IMU震动测试数据1.txt'



if __name__ == '__main__':
    fig,ax = plt.subplots(2,1,sharex='all')
    path = '/Users/Wayne/Documents' if platform.system() == 'Darwin' else '/media/psf' + '/work/data/ost_calibration/imu_intrinsic/imu_tk/mercury_arm/aitexun' #/IMU震动测试数据1.txt'


    load_data(path,date='20240130_field_validation',
    keyword='imutk_arm_thick_jiaodian_right_locked_test4',
    kw="IMU垫硅胶6轴锁紧4")
    
    load_data(path,date='20240130_field_validation',
    keyword='imutk_arm_thick_jiaodian_right_locked_test5',
    kw="IMU垫硅胶6轴锁紧5")

    plt.show()

    # main()
