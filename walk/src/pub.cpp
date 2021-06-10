#include <iostream>
#include <fstream>
#include "ros/ros.h"
#include "std_msgs/Float32.h"
#include "geometry_msgs/Twist.h"
#include "sensor_msgs/LaserScan.h"
#include "nav_msgs/Odometry.h"
#include "sensor_msgs/Imu.h"
#include <tf/transform_broadcaster.h>
#include <thread>
using namespace std;

//set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -O3")


class pubVelocity{
   private:
      ros::NodeHandle nh;
      geometry_msgs::Twist vel;

      ros::Publisher pubvelmsg;
      ros::Subscriber submsg;

   public:

   pubVelocity():
        nh("~")
      {
         vel.linear.x=0;
         vel.linear.y=0;
         vel.linear.z=0;
         vel.angular.x=0;
         vel.angular.y=0;
         vel.angular.z=0;
         submsg = nh.subscribe<geometry_msgs::Twist> ("/cmd_vel_1", 2, &pubVelocity::msgHandler, this);
         //在话题/cmd_vel_1上订阅geometry_msgs::Twist消息，
         //缓存达到2 条消息后，再有新的消息到来就将开始丢弃先前接收的消息
         //发布到这个话题时，ROS 就会调用&pubVelocity::msgHandler函数 
         pubvelmsg = nh.advertise<geometry_msgs::Twist> ("/cmd_vel", 100);//在话题/cmd_vel上发布geometry_msgs/Twist消息，
         //如果我们发布的消息的频率太高，缓冲区中的消息在大于 100 个的时候就会开始丢弃先前发布的消息
      }
    
   void msgHandler(const geometry_msgs::Twist::ConstPtr& msg){
      vel = *msg;
   }

   void pubvel(){
      ros::Rate rate(100);
      while(ros::ok()){
        ros::spinOnce();
        pubvelmsg.publish(vel);
        rate.sleep();
      }
   }


};

int main(int argc, char** argv){

   ros::init(argc, argv, "pubvel");//初始化ROS
   pubVelocity MO;
   std::thread pubthread(&pubVelocity::pubvel, &MO);
   ros::spin();
   pubthread.join();
   return 0;
}



