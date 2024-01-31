#include <iostream>

#include "imu_tk/io_utils.h"
#include "imu_tk/calibration.h"
#include "imu_tk/filters.h"
#include "imu_tk/integration.h"
#include "imu_tk/visualization.h"

using namespace std;
using namespace imu_tk;
using namespace Eigen;

int main(int argc, char** argv)
{
  if( argc < 3 )
    return -1;

  vector< TriadData > acc_data, gyro_data;
  
  cout<<"Importing IMU data from the Matlab matrix file : "<< argv[1]<<endl;  
  importAsciiData( argv[1], acc_data, imu_tk::TIMESTAMP_UNIT_SEC );
  cout<<"Importing IMU data from the Matlab matrix file : "<< argv[2]<<endl;  
  importAsciiData( argv[2], gyro_data, imu_tk::TIMESTAMP_UNIT_SEC  );
  cout << "Get static interval path : "<< argv[3] << endl;
  std::string static_interval_path = argv[3];
  std::string save_root = argv[4];

  
  CalibratedTriad init_acc_calib, init_gyro_calib;
  init_acc_calib.setBias( Vector3d(0.0, 0.0, 0.0) );
  init_gyro_calib.setScale( Vector3d(1.0, 1.0, 1.0) );
  
  MultiPosCalibration mp_calib;


  // mp_calib.accUseMeans
  mp_calib.setStaticIntervalPath(static_interval_path);
  mp_calib.setInitStaticIntervalDuration(50.0);
  mp_calib.setInitAccCalibration( init_acc_calib );
  mp_calib.setInitGyroCalibration( init_gyro_calib );  
  mp_calib.setGravityMagnitude(9.81744);
  mp_calib.enableVerboseOutput(true);
  mp_calib.enableGyroBiasOptimization(true);
  mp_calib.setIntarvalsNumSamples(500 * 2);
  // mp_calib.enableAccUseMeans(true);
  mp_calib.setGyroDataPeriod(0.002);
  mp_calib.calibrateAccGyro(acc_data, gyro_data );
  cout << save_root + "/test_imu_acc.calib" << endl;
  mp_calib.getAccCalib().save(save_root + "/test_imu_acc.calib");
  mp_calib.getGyroCalib().save(save_root + "/test_imu_gyro.calib");
  
  
//   for( int i = 0; i < acc_data.size(); i++)
//   {
//     cout<<acc_data[i].timestamp()<<" "
//           <<acc_data[i].x()<<" "<<acc_data[i].y()<<" "<<acc_data[i].z()<<" "
//           <<gyro_data[i].x()<<" "<<gyro_data[i].y()<<" "<<gyro_data[i].z()<<endl;
//   }
//   cout<<"Read "<<acc_data.size()<<" tuples"<<endl;
  
  return 0;
}