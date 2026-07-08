#!/usr/bin/env python2

########
# Name: funfact_manager.py
#
# Purpose: Manages fun facts and jokes for the robot.
#
# Usage: Initialize this class and use the get_random_event method to retrieve a random event.
#
# Author: Pragna Guntupalli <sguntupalli@ucsd.edu>
#
# Acknowledgements: Used some code from ROS 2 Tutorials and MangDang's ROS git repo
#
# Date: 07 June 2026
########

import random


class FunFactManager(object):
    def __init__(self):
        self.previous_event = None
        self.events = [
            "joke1",
            "joke2",
            "joke3",
            "fact1",
            "fact2",
        ]

    def get_random_event(self):
        available = [
            event
            for event in self.events
            if event != self.previous_event
        ]

        robot_event = random.choice(available)
        self.previous_event = robot_event
        return robot_event