#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class ServiceClient02(Node):
    def __init__(self, name):
        super().__init__(name)
        self.get_logger().info("已启动 %s 节点." % name)
        self.client_ = self.create_client(AddTwoInts, "add_two_ints_srv")

    def result_callback_(self, result_future):
        response = result_future.result()
        self.get_logger().info(f"收到返回结果：{response.sum}")

    def send_request(self, a, b):
        while rclpy.ok() and self.client_.wait_for_service(1) == False:
            self.get_logger().info(f"等待服务端上线....")

        request = AddTwoInts.Request()
        request.a, request.b = a, b
        self.get_logger().info(f"发送申请计算：{request.a} + {request.b}")
        # 同样是异步请求，rclpy客户端库定义的是call_async
        # 并且使用add_done_callback添加回调函数
        self.client_.call_async(request).add_done_callback(self.result_callback_)


def main(args=None):
    rclpy.init(args=args)  # 初始化rclpy
    node = ServiceClient02("service_client_02")  # 新建一个节点
    node.send_request(3, 4)
    rclpy.spin(node)  # 保持节点运行，检测是否收到退出指令（Ctrl+C）
    rclpy.shutdown()  # 关闭rclpy
