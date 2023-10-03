#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"

class ServiceClient01 : public rclcpp::Node
{
public:
    // 构造函数,有一个参数为节点名称
    ServiceClient01(std::string name) : Node(name)
    {
        RCLCPP_INFO(this->get_logger(), "已启动：%s 节点.", name.c_str());
        // 创建客户端
        client_ = this->create_client<example_interfaces::srv::AddTwoInts>("add_two_ints_srv");
    }

    void send_request(int a, int b)
    {
        RCLCPP_INFO(this->get_logger(), "计算 %d + %d.", a, b);

        // 等待服务端上线，1s 等一次
        while (!client_->wait_for_service(std::chrono::seconds(1)))
        {
            // 等待时检测 rclcpp 的状态
            if (!rclcpp::ok())
            {
                RCLCPP_ERROR(this->get_logger(), "等待服务的过程中被打断...");
                return;
            }
            RCLCPP_INFO(this->get_logger(), "等待服务端上线中...");
        }

        // 构造请求
        auto request = std::make_shared<example_interfaces::srv::AddTwoInts_Request>();
        request->a = a, request->b = b;

        // 发送异步请求，然后等待返回，返回时调用回调函数
        client_->async_send_request(
            request,
            std::bind(&ServiceClient01::result_callback_, this, std::placeholders::_1));
    }

private:
    // 声明客户端
    rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedPtr client_;

    // 类模板 std::shared_future 提供访问异步操作结果的机制
    // 类似 std::future ，除了允许多个线程等候同一共享状态。
    void result_callback_(
        rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedFuture result_future)
    {
        auto response = result_future.get();
        RCLCPP_INFO(this->get_logger(), "计算结果：%ld.", response->sum);
    }
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    /*创建对应节点的共享指针对象*/
    auto node = std::make_shared<ServiceClient01>("service_client_01");
    /* 运行节点，并检测退出信号*/
    // 增加这一行，node->send_request(5, 6);，计算5+6结果
    node->send_request(5, 6);
    /* 运行节点，并检测退出信号*/
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
