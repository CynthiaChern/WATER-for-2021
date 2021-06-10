# WATER-for-2021
Code for Intelligent Engineering Experiment on WATER(two wheeled differential robot)
## real action of water
## Gmapping
rosrun gmapping slam_gmapping

roslaunch water_nav makemap_launch

rosrun teleop_twist_keyboard teleop_twist_keyboard.py

## Navigation
### DWA
roslaunch water_nav move_base.launch
### TEB
(Please download teb_local_planner,teb_local_planner_tutorials,g2o first.)

roslaunch water_nav navteb.launch

## Follow
### Laser
roslaunch simple_follower laser_follower.launch
### opencv_color
rosrun ball_tracking ball_follower.py
### yolo_target
(Please download darknet first)

rosrun darknet_ros speed_control.py

#### If you need code for simulation，please click https://github.com/DingJianquan/water_simulation .
