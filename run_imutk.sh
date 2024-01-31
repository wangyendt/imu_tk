#acc_file=./bin/test_data/xsens_acc.mat
#gyro_file=./bin/test_data/xsens_gyro.mat

# acc_file=./bin/test_data/mercury_manual/imu_6/acc.mat
# gyro_file=./bin/test_data/mercury_manual/imu_6/gyro.mat
# static_interval_file=./debug/mercury_manual/imu_6/static_intervals.txt
# save_root=./bin/result/mercury_manual/imu_6

# for idx in {10..11}
# do

# 	acc_file=./bin/test_data/mercury_arm/imu_${idx}/acc.mat
# 	gyro_file=./bin/test_data/mercury_arm/imu_${idx}/gyro.mat
# 	static_interval_file=./debug/mercury_arm/imu_${idx}/static_intervals.txt
# 	save_root=./bin/result/mercury_arm/imu_${idx}


# 	cd build && make -j12 && cd ..
# 	./bin/test_imu_calib $acc_file $gyro_file $static_interval_file $save_root

# done

# acc_file=./bin/test_data/aitexun/all_none/acc.mat
# gyro_file=./bin/test_data/aitexun/all_none/gyro.mat
# static_interval_file=./debug/aitexun/all_none/static_intervals.txt
# save_root=./bin/result/aitexun/all_none

# acc_file=./bin/test_data/aitexun/all_with_jiaodian/acc.mat
# gyro_file=./bin/test_data/aitexun/all_with_jiaodian/gyro.mat
# static_interval_file=./debug/aitexun/all_with_jiaodian/static_intervals.txt
# save_root=./bin/result/aitexun/all_with_jiaodian

# acc_file=./bin/test_data/aitexun/all_with_jiaodian_6x/acc.mat
# gyro_file=./bin/test_data/aitexun/all_with_jiaodian_6x/gyro.mat
# static_interval_file=./debug/aitexun/all_with_jiaodian_6x/static_intervals.txt
# save_root=./bin/result/aitexun/all_with_jiaodian_6x


date=20240130_field_validation
# keyword=imutk_arm_thick_jiaodian_right_unlocked_test1
keyword=imutk_arm_thick_jiaodian_right_locked_legfixed_test7
# keyword=imutk_arm_none_test1
data_root=./bin/test_data/aitexun/${date}/${keyword}
save_root=./bin/result/aitexun/${date}/${keyword}
debug_root=./debug/aitexun/${date}/${keyword}
params_root=./params/${date}
log_root=./logs/aitexun/${date}
mkdir -p ${data_root}
mkdir -p ${save_root}
mkdir -p ${debug_root}
mkdir -p ${params_root}
mkdir -p ${log_root}
acc_file=${data_root}/acc.mat
gyro_file=${data_root}/gyro.mat
static_interval_file=${debug_root}/static_intervals.txt


# python3 ./check_raw_data_and_to_mat.py ${date} ${keyword} "IMU垫硅胶6轴不锁紧1"
python3 ./check_raw_data_and_to_mat.py ${date} ${keyword} "IMU垫硅胶6轴锁紧镜腿固定7"
# exit
cd build && make -j12 && cd ..
./bin/test_imu_calib $acc_file $gyro_file $static_interval_file $save_root | tee ${log_root}/${keyword}.log
