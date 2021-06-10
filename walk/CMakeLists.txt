cmake_minimum_required(VERSION 2.8.3)
project(walk)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -O3")

find_package(catkin REQUIRED COMPONENTS
  roscpp
  std_msgs
)


catkin_package()

include_directories(
${catkin_INCLUDE_DIRS}
)

add_executable(pub src/pub.cpp)
target_link_libraries(pub ${catkin_LIBRARIES})

