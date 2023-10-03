#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_ros2_interfaces.srv import MoveRobot
from example_ros2_interfaces.msg import RobotStatus


class ExampleInterfacesControl02(Node):
    def __init__(self, name):
        super().__init__(name)
        self.get_logger().info("已启动 %s 节点." % name)
        self.client_ = self.create_client(MoveRobot, "move_robot")
        self.robot_status_subscribe_ = self.create_subscription(
            RobotStatus, "robot_status", self.robot_status_callback, 10
        )

    def robot_status_callback(self, msg):
        self.get_logger().info(f"收到状态数据位置：{msg.pose:.5f}，当前状态：{msg.status}")

    def move_result_callback_(self, result_future):
        response = result_future.result()
        self.get_logger().info(f"收到返回结果：{response.pose:.5f}")

    def move_robot(self, distance):
        while rclpy.ok() and self.client_.wait_for_service(1) == False:
            self.get_logger().info(f"等待服务端上线...")
        request = MoveRobot.Request()
        request.distance = distance
        self.get_logger().info(f"请求服务让机器人移动 {distance}")
        self.client_.call_async(request).add_done_callback(self.move_result_callback_)


def main(args=None):
    rclpy.init(args=args)  # 初始化 rclpy
    node = ExampleInterfacesControl02("example_interfaces_control_02")  # 新建一个节点
    node.move_robot(5.0)  # 移动 5 米
    rclpy.spin(node)  # 保持节点运行，检测是否收到退出指令（Ctrl+C）
    rclpy.shutdown()  # 关闭 rclpy
