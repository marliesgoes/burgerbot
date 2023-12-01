from segmentation_utils import detect, groundingdino_model, sam_predictor, segment, draw_mask, transform_image
import PIL
from PIL import Image
import numpy as np
import cv2


def get_camera_image():
    """
    Captures an image using the system's webcam and returns it.

    Returns:
        image: An image object that can be processed by other functions. The image
               will be in the format used by OpenCV.
    """
    # Initialize the webcam (0 is the default camera)
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    # Capture a single frame
    ret, frame = cap.read()

    # Release the webcam
    cap.release()

    # Check if the frame was captured correctly
    if not ret:
        raise IOError("Failed to capture image")

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(frame)

    return image


def find_center_of(ingredient, image, max_num=1, visualize=False):
    """
    Locates the center of a specified ingredient in the given image.

    Parameters:
        ingredient (str): The name of the ingredient to locate in the image.
        image: The image object captured from the camera in which to find the ingredient.

    Returns:
        list[tuple]: A list of tuples of (x, y) coordinates representing the central point(s) of 
        the detected instances of the ingredient in the image space.
    """
    image_source, image = transform_image(image)
    detected_boxes = detect(image, text_prompt=ingredient,
                            model=groundingdino_model)
    print(
        f"Detected {len(detected_boxes)} instances of {ingredient}, picking the top {max_num}...")
    detected_boxes = detected_boxes[:max_num]
    segmented_frame_masks = segment(
        image_source, sam_predictor, boxes=detected_boxes)

    if visualize:
        print("Visualizing the top segmentation mask")
        annotated_frame_with_mask = draw_mask(
            segmented_frame_masks[0][0], image_source)
        # Visualize the annotated frame with mask
        image = PIL.Image.fromarray(annotated_frame_with_mask)
        image.show()

    # Find the center of the masks
    centers = []
    for mask in segmented_frame_masks:
        mask = mask[0]
        mask = mask.cpu().numpy()
        pixels = np.argwhere(mask > 0)
        center = np.mean(pixels, axis=0)
        y, x = center
        centers.append((int(x), int(y)))

    return centers


def camera_to_robot_coords(camera_coords):
    """
    Converts camera image space coordinates to robot arm's coordinate system.

    Parameters:
        camera_coords (tuple): A tuple of (x, y) coordinates in the camera's image space.

    Returns:
        tuple: A tuple of (x, y, z) coordinates in the robot's coordinate system.
    """
    pass


def move_item(pickup_coords, dropoff_coords):
    """
    Commands the robot to move an item from pickup coordinates to dropoff coordinates.

    Parameters:
        pickup_coords (tuple): The (x, y, z) coordinates where the robot will pick up the item.
        dropoff_coords (tuple): The (x, y, z) coordinates where the robot will place the item.

    Returns:
        bool: True if the item was successfully moved, False otherwise.
    """
    pass
