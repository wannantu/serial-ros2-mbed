import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=None)

class PubSerialNode(Node):
    def __init__(self):
        super().__init__('serial_node')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        self.timer = self.create_timer(1, self.timer_callback)
        self.i = 0
    
    def timer_callback(self):
        msg = String()
        msg.data = str(self.i)
        self.publisher_.publish(msg)
        self.get_logger().info(f'Sending data: {self.i}')
        ser.write(str(self.i).encode())
        self.i += 1

def main():
    rclpy.init()
    node = PubSerialNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print('Push Ctrl + C')
    finally:
        node.destroy_node()
        rclpy.shutdown()
        print('Finish program')

if __name__ == '__main__':
    main()