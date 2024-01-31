# date=20240130_field_validation
# keyword=imutk_left_of_jiaju_all_test1
date=20240130_field_validation
keyword=imutk_manual_test1
# date=20240127_remote_validation
# keyword=with_jiaodian_6x
data_root=./bin/test_data/aitexun/${date}/${keyword}
save_root=./bin/result/aitexun/${date}/${keyword}
debug_root=./debug/aitexun/${date}/${keyword}
params_root=./params/${date}

python3 check_gyro_integral.py ${params_root}/${keyword}.txt "IMU单向转720度震动测试数据3"
