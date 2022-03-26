"""
A collection of pyautogui method
"""

import time
import pyautogui
import pazusoba

from typing import List
from config import Config
from random import randint
from screenshot import take_screenshot
from utils import getColumnRow, getMonitorParamsFrom

def perform(route: List[pazusoba.Location], snapshot=True):
    """
    Perform the best route step by step
    """
    config = Config()
    if config.debug_mode:
        print("- PERFORMING -")
    # setup everything
    left, top, end_left, end_top = config.board_location
    _, row = getColumnRow()
    orb_height = (end_top - top) / row
    x_start = left + orb_height / 2
    y_start = top + orb_height / 2

    # save current position
    (px, py) = pyautogui.position()
    if config.debug_mode:
        step = len(route)
        print("=> {} steps".format(step))
        start = time.time()
    
    for i in range(step):
        curr = route[i]
        x, y = curr.row, curr.column
        target_x = x_start + y * orb_height
        target_y = y_start + x * orb_height
        if i == 0:
            __holdLeftKey(target_x, target_y)  
        else:
            __moveTo(target_x, target_y, ultra_fast=True, random=False)

    # only release it when everything are all done
    pyautogui.mouseUp()
    print("=> Done")
    if config.debug_mode:
        print("=> It took %.3fs." % (time.time() - start))

    # move back to current position after everything
    pyautogui.moveTo(px, py)
    pyautogui.leftClick()

    if snapshot:
        # save final solution
        take_screenshot(getMonitorParamsFrom(config.board_location), write2disk=True, name="route.png")

def hold(x, y):
    """
    Hold the left mouse key down
    """
    pyautogui.moveTo(x, y)
    pyautogui.mouseDown()
    pyautogui.mouseUp()

def __holdLeftKey(x, y, repeat=True):
    """
    Hold the left mouse key down twice if requires to prevent `window focus` issues
    """
    pyautogui.mouseDown(x, y, button='left')
    if repeat:
        pyautogui.mouseDown(x, y, button='left')

def __moveTo(x, y, ultra_fast=False, random=False):
    """
    Move to (x, y) using default settings (duration=0, _pause=True) or ultra fast with random delays
    """
    if ultra_fast:
        pyautogui.moveTo(x, y, duration=0, _pause=False)
        # add an random offset if required
        offset = 0 if not random else randint(0, 100)

        # NOTE: 50ms is about the minimum time for the game to recognise correctly, less than it will cause some issues
        time.sleep((80 + offset) / 1000)
    else:
        pyautogui.moveTo(x, y)