project(imu_tk)

cmake_minimum_required (VERSION 2.8) 
cmake_policy(SET CMP0015 NEW)

SET( CMAKE_CXX_FLAGS "-std=c++17 -O3")
add_compile_options(-g -ggdb -O0 -Wall -fstack-protector-all -march=native -fnon-call-exceptions)


if ("${CMAKE_BUILD_TYPE}" STREQUAL "")
    set(CMAKE_BUILD_TYPE "Release")
endif()

if(NOT DEFINED BUILD_IMU_TK_EXAMPLES)
    set(BUILD_IMU_TK_EXAMPLES "ON")
endif(NOT DEFINED BUILD_IMU_TK_EXAMPLES)

find_package(Boost REQUIRED)  
find_package(Eigen3 REQUIRED)
find_package(Ceres REQUIRED)

include_directories(./include
    /usr/include
    ${Boost_INCLUDE_DIRS}
    ${EIGEN3_INCLUDE_DIR}
    ${CERES_INCLUDE_DIRS})

#Vis3D
#find_package(Qt5 COMPONENTS QtCore QtGui QtOpenGL REQUIRED )
find_package(Qt5 COMPONENTS Core Gui Widgets OpenGL  REQUIRED)
find_package(OpenGL REQUIRED)
find_package(GLUT REQUIRED)

#include(${QT_USE_FILE})
add_definitions(${QT_DEFINITIONS})
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_INCLUDE_CURRENT_DIR ON)

include_directories(
    include
    ${OPENGL_INCLUDE_DIRS}
    ${GLUT_INCLUDE_DIRS}
    ${CMAKE_CURRENT_BINARY_DIR}
    )

set(IMU_TK_VIS_EXTRA_SOURCES 
    ./src/vis_extra/gl_camera.cpp
    ./src/vis_extra/opengl_3d_scene.cpp )
set(IMU_TK_VIS_EXTRA_HEADERS
    ./include/imu_tk/vis_extra/opengl_3d_scene.h )

qt5_wrap_cpp(IMU_TK_VIS_EXTRA_HEADERS_MOC ${IMU_TK_VIS_EXTRA_HEADERS})

aux_source_directory( ./src IMU_TK_CORE_SRC )
set( IMU_TK_SRC ${IMU_TK_CORE_SRC} ${IMU_TK_VIS_EXTRA_HEADERS_MOC} ${IMU_TK_VIS_EXTRA_SOURCES} )

add_library(imu_tk ${IMU_TK_SRC})
target_link_libraries(imu_tk Qt5::Core Qt5::Gui Qt5::Widgets Qt5::OpenGL)
set_target_properties(imu_tk PROPERTIES ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/lib)

set (IMU_TK_INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/include CACHE STRING "imu_tk include directories")
set (IMU_TK_LIB_DIR ${CMAKE_CURRENT_SOURCE_DIR}/lib CACHE STRING "imu_tk libraries directories")
set (IMU_TK_LIBS imu_tk ${CERES_LIBRARIES} Qt5::Core Qt5::Gui Qt5::Widgets Qt5::OpenGL ${OPENGL_LIBRARIES} ${GLUT_LIBRARY}
    CACHE STRING "imu_tk libraries")

message( "${IMU_TK_LIBS}" )

if( BUILD_IMU_TK_EXAMPLES )

    add_executable(test_imu_calib apps/test_imu_calib.cpp)
    #qt5_use_modules(test_imu_calib Core Gui Widgets OpenGL)
    target_link_libraries( test_imu_calib ${IMU_TK_LIBS})
    set_target_properties( test_imu_calib PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)


    add_executable(test_integration apps/test_integration.cpp)
    #qt5_use_modules(test_integration Core Gui Widgets OpenGL)
    target_link_libraries( test_integration ${IMU_TK_LIBS})

    set_target_properties( test_integration PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)

endif( BUILD_IMU_TK_EXAMPLES )
