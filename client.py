#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import sys
import time

import rospy
import argparse
from intera_motion_interface import (
    MotionTrajectory,
    MotionWaypoint,
    MotionWaypointOptions
)
from intera_interface import Limb

def main():
    # if len(sys.argv) < 4:
    #     print('{0} <BindIP><Server IP><Message>'.format(sys.argv[0]))
        # sys.exit()

    bindIP = '192.168.101.5' #sys.argv[1]
    serverIP = '192.168.101.12' #sys.argv[2]

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # SOCK_STREAM은 TCP socket을 뜻함
    sock.bind((bindIP, 0))

    sock.connect((serverIP, 5425)) # 서버에 연결 요청

    rospy.init_node('sawyer_client')

    arg_fmt = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=arg_fmt,
                                     description=main.__doc__)
    # parser.add_argument(
    #     "-q", "--joint_angles", type=float,
    #     nargs='+', default=[0.0, -0.9, 0.0, 1.8, 0.0, -0.9, 0.0],
    #     help="A list of joint angles, one for each of the 7 joints, J0...J6")
    parser.add_argument(
        "-s",  "--speed_ratio", type=float, default=0.5,
        help="A value between 0.001 (slow) and 1.0 (maximum joint velocity)")
    parser.add_argument(
        "-a",  "--accel_ratio", type=float, default=0.5,
        help="A value between 0.001 (slow) and 1.0 (maximum joint accel)")
    parser.add_argument(
        "--timeout", type=float, default=None,
        help="Max time in seconds to complete motion goal before returning. None is interpreted as an infinite timeout.")
    args = parser.parse_args(rospy.myargv()[1:])

    goal_joint_angles = [0.0, -0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    while True:
        # 서버로 부터 수신
        rbuff = sock.recv(1024) # 메시지 수신
        received = str(rbuff)
        # print('수신:{0}'.format(received))

        if received.count >= 5:

            center_str = received.split('SM')[1].split('SE')[0]
            print(center_str)

            if  center_str == 'Q':
                break
            elif center_str == 'A':
                goal_joint_angles = [0.0, -0.9, 0.0, 1.8, 0.0, -0.9, 0.0]
            elif center_str == 'B':
                goal_joint_angles = [0.0, -0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

            limb = Limb()
            traj = MotionTrajectory(limb = limb)

            wpt_opts = MotionWaypointOptions(max_joint_speed_ratio=args.speed_ratio,
                                                    max_joint_accel=args.accel_ratio)
            waypoint = MotionWaypoint(options = wpt_opts.to_msg(), limb = limb)

            joint_angles = limb.joint_ordered_angles()

            waypoint.set_joint_angles(joint_angles = joint_angles)
            traj.append_waypoint(waypoint.to_msg())

            waypoint.set_joint_angles(joint_angles = goal_joint_angles)
            traj.append_waypoint(waypoint.to_msg())

            result = traj.send_trajectory(timeout=args.timeout)

    sock.close()

    # try:

    #     # 서버로 송신
    #     sbuff = bytes(message)
    #     sock.send(sbuff) # 메시지 송신
    #     print('송신:{0}'.format(message))


    #     # 서버로 부터 수신
    #     rbuff = sock.recv(1024) # 메시지 수신
    #     received = str(rbuff)
    #     print('수신:{0}'.format(received))

    # finally:
    #     sock.close()

if __name__ == '__main__':
    main()
