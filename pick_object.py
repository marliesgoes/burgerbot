from DexArm_API.pydexarm.pydexarm import Dexarm
import numpy as np
import pandas as pd

df = pd.read_csv('calib_coords.csv')

# Splitting data into robot and camera coordinates
robot_coords = df[['rob_x', 'rob_y']].to_numpy()
cam_coords = df[['cam_x', 'cam_y']].to_numpy()

# Polynomial degree
degree = 2

# Fit polynomial models
model_x = np.poly1d(np.polyfit(cam_coords[:, 0], robot_coords[:, 0], degree))
model_y = np.poly1d(np.polyfit(cam_coords[:, 1], robot_coords[:, 1], degree))


def camera_to_robot_coords(cam_x, cam_y):
    rob_x = model_x(cam_x)
    rob_y = model_y(cam_y)
    return int(rob_x), int(rob_y)


def move_item(robo_coor, dropoff_coords=(300, 100), height=-55):
    """
    Commands the robot to move an item from pickup coordinates to dropoff coordinates.

    Parameters:
        pickup_coords (tuple): The (x, y, z) coordinates where the robot will pick up the item.
        dropoff_coords (tuple): The (x, y, z) coordinates where the robot will place the item.

    Returns:
        bool: True if the item was successfully moved, False otherwise.
    """
    dexarm = Dexarm(port="/dev/tty.usbmodem308B335D34381")
    dexarm.go_home()
    dexarm.move_to(robo_coor[0], robo_coor[1], 0)
    dexarm.move_to(robo_coor[0], robo_coor[1], height)
    dexarm.air_picker_pick()
    dexarm.move_to(robo_coor[0], robo_coor[1], 0)
    dexarm.move_to(dropoff_coords[0], dropoff_coords[1], 0)
    dexarm.move_to(dropoff_coords[0], dropoff_coords[1], height)

    dexarm.air_picker_place()
    dexarm.move_to(dropoff_coords[0], dropoff_coords[1], 0)
    dexarm.go_home()
    dexarm.air_picker_stop()
