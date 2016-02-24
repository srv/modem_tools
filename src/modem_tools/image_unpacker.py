#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Software License Agreement (BSD License)
#
#  Copyright (c) 2014, Ocean Systems Laboratory, Heriot-Watt University, UK.
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above
#     copyright notice, this list of conditions and the following
#     disclaimer in the documentation and/or other materials provided
#     with the distribution.
#   * Neither the name of the Heriot-Watt University nor the names of
#     its contributors may be used to endorse or promote products
#     derived from this software without specific prior written
#     permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
#  FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
#  COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
#  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
#  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
#  ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#  POSSIBILITY OF SUCH DAMAGE.
#
#  Original authors:
#   Valerio De Carolis, Marian Andrecki, Corina Barbalata, Gordon Frost
from __future__ import division

import numpy as np
import cv2
import Image
import zlib
import roslib
roslib.load_manifest('modem_tools')

import rospy

# Messages
from diagnostic_msgs.msg import KeyValue

# Services
from std_msgs.msg import String
from std_srvs.srv import Trigger, TriggerResponse

# Constants
TOPIC_MODEM_CONSTRUCTOR = '/modem/unpacker/image'
SRV_SIGNAL = '/image_packer/signal'
LOOP_RATE = 1  # Hz

class ImageUnpacker(object):
    def __init__(self, name):
        self.name = name

        # Subscribers
        self.sub_modem = rospy.Subscriber(TOPIC_MODEM_CONSTRUCTOR, String, self.handle_image, tcp_nodelay=True, queue_size=1)

        # Publishers

        # Services

    def handle_image(self, msg):
        rospy.loginfo('Image!')

        im = np.zeros(len(msg.payload)).astype(np.uint8)
        for i, value in enumerate(msg.payload):
            im[i] = ord(value)

        im = cv2.imdecode(im, cv2.CV_LOAD_IMAGE_GRAYSCALE)

        larger = cv2.resize(im, (0,0), fx=3, fy=3)
        cv2.imshow('image', larger)
        cv2.waitKey()

    def loop(self):
        pass

if __name__ == '__main__':
    rospy.init_node('image_unpacker')
    name = rospy.get_name()

    unpacker = ImageUnpacker(name)
    loop_rate = rospy.Rate(LOOP_RATE)

    while not rospy.is_shutdown():
        try:
            unpacker.loop()
            loop_rate.sleep()
        except rospy.ROSInterruptException:
            rospy.loginfo('%s caught ros interrupt!', name)
        # except Exception as e:
        #     rospy.logfatal('%s', e)
        #     rospy.logfatal('%s caught exception and dying!', name)
        #     sys.exit(-1)


