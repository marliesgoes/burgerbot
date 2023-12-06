from DexArm_API.pydexarm.pydexarm import Dexarm
import numpy as np
import pandas as pd
import time

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


def move_items(found_items, recipe):
    """
    Commands the robot to move an item from pickup coordinates to dropoff coordinates.

    Parameters:
        found_items (dict): Dictionary of items with their corresponding coordinates.
        recipe (list): List of items to be moved.

    Returns:
        bool: True if all items were successfully moved, False otherwise.
    """
    dropoff_coords = (300, 100)
    pickup_height = -65

    dexarm = Dexarm(port="/dev/tty.usbmodem308B335D34381")
    dexarm.go_home()
    i = 0

    try:
        for item in recipe:
            robo_coor = found_items[item].pop()
            dropoff_height = -55 + (i * 10)
            dexarm.move_to(robo_coor[0], robo_coor[1], 0)
            dexarm.move_to(robo_coor[0], robo_coor[1], pickup_height)
            dexarm.air_picker_pick()
            time.sleep(1)
            dexarm.move_to(robo_coor[0], robo_coor[1], 0)

            dexarm.move_to(dropoff_coords[0], dropoff_coords[1], 0)
            dexarm.move_to(dropoff_coords[0],
                           dropoff_coords[1], dropoff_height)

            dexarm.air_picker_place()
            dexarm.move_to(dropoff_coords[0], dropoff_coords[1], 0)
            i += 1
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        dexarm.go_home()
        dexarm.air_picker_stop()

    return True
