#include <ros/ros.h>
#include <cv_bridge/cv_bridge.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl_conversions/pcl_conversions.h>
#include <sensor_msgs/Image.h>
#include <sensor_msgs/PointCloud2.h>

using namespace std;

class Img2PCL{
private:
    ros::Publisher pcl_pub_;
    ros::Publisher img_sub_;
public:
    Img2PCL(ros::NodeHandle &nh){
        pcl_pub_ = nh.advertise<sensor_msgs::PointCloud2>("/water/pts", 10);;
        img_sub_ = nh.subscribe<<sensor_msgs::Image>("/water_astra_rgbd/depth/image_raw", 10, &Img2PCL::pclCallback, this);
    }

    ~Img2PCL(){
        ;
    }

    pclCallback(const sensor_msgs::ImageConstPtr& img){
        ;
    }
};

int main(){
    
    ;
}