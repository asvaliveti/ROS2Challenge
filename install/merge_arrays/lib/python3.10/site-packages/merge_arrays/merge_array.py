# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node

from std_msgs.msg import Int32MultiArray

class MergeArray(Node):

    arr1 = []
    arr2 = []
    def __init__(self):
        super().__init__('merge_array')

        # subscribe to topic 1
        self.subscription = self.create_subscription(
            Int32MultiArray,
            '/input/array1',
            self.receive_arr_1,
            10)

        # subscribe to tpoic 2
        self.subscription2 = self.create_subscription(
            Int32MultiArray,
            '/input/array2',
            self.receive_arr_2,
            10
        )

        self.subscription  # prevent unused variable warning
        self.subscription2

    def merge_arrs(self):
        # merge arrs and print
        mergedArr = self.arr1 + self.arr2
        print(mergedArr)

        # create a publisher and publish to output topic
        self.publisher = self.create_publisher(Int32MultiArray, '/output/array', 10)
        outputArr = Int32MultiArray()
        outputArr.data = mergedArr
        self.publisher.publish(outputArr)

    # recieve arr from /input/array1
    def receive_arr_1(self, msg):
        self.arr1 = msg.data

    # recieve arr from /input/array2
    def receive_arr_2(self, msg):
        self.arr2 = msg.data
        self.merge_arrs()


def main(args=None):
    rclpy.init(args=args)

    merge_array = MergeArray()

    rclpy.spin(merge_array)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    merge_array.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
