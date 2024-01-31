#acc_file=./bin/test_data/xsens_acc.mat
#gyro_file=./bin/test_data/xsens_gyro.mat
acc_file=./bin/test_data/mercury_manual/imu_1/acc.mat
gyro_file=./bin/test_data/mercury_manual/imu_1/gyro.mat
static_interval_file=./debug/mercury_manual/imu_1/static_intervals.txt
save_root=./bin/cross_validate/mercury_manual/imu_1


cd build && make -j12 && cd ..
./bin/cross_validate_calib $acc_file $gyro_file $static_interval_file $save_root

