import numpy as np
import cv2 as cv
import glob
from DexArm_API.pydexarm.pydexarm import Dexarm


def camera_to_robot_coords(img, cam_mat_path, dist_path, pick=(924, 545)):
    """
    Converts camera image space coordinates to robot arm's coordinate system.

    Parameters:
        camera_coords (tuple): A tuple of (x, y) coordinates in the camera's image space.

    Returns:
        tuple: A tuple of (x, y, z) coordinates in the robot's coordinate system.
    """
    pick = pick[0]
    print("pick coors: ",pick)
    img = np.array(img)
    h,  w = img.shape[:2]

    cameraMatrix = np.load(cam_mat_path)
    dist = np.load(dist_path)
    newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(
        cameraMatrix, dist, (w, h), 1, (w, h))

    # # Undistort
    dst = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

    # # crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    trans_matrix = np.array(
        [[0, 1, 0, 0.40], [1, 0, 0, 0.0], [0, 0, -1, 0.455], [0, 0, 0, 1]])
    inv_new_cam_mat = np.linalg.inv(newCameraMatrix)
    pickup = np.array([pick[0], pick[1], 1])
    # print(f"pickup: {pickup}")
    cam_coor = inv_new_cam_mat@pickup
    cam_coor = cam_coor * 0.505
    # print(cam_coor.shape)
    cam_coor = np.append(cam_coor, 1)
    robo_coor = (trans_matrix@cam_coor)*1000
    # print(f"robo_coor: {robo_coor}")
    return robo_coor


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
    # print("done1")
    dexarm.move_to(dropoff_coords[0], dropoff_coords[1], height)
    # print("done12")

    dexarm.air_picker_place()
    dexarm.move_to(200, 0, 0)
    dexarm.air_picker_stop()


if __name__ == "__main__":
    # image = PIL.Image.open("caliResulttr2.png")
    img_path = ""
    cam_mat_path = "/Users/jeelshah/Documents/Fall 2023/TalkingToRobots/project/burgerbot/calib/cameraMatrix.npy"
    dist_path = "/Users/jeelshah/Documents/Fall 2023/TalkingToRobots/project/burgerbot/calib/dist.npy"
    robo_coors = camera_to_robot_coords(img_path, cam_mat_path, dist_path)
    move_item(robo_coors)
