from segmentation_utils import detect, groundingdino_model, transform_image
from groundingdino.util.inference import annotate
import PIL
from PIL import Image
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
    # Flip the image
    image = image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
    image_source, image = transform_image(image)

    detected_boxes, logits, phrases = detect(
        image, text_prompt=ingredient, model=groundingdino_model)
    print(
        f"Detected {len(detected_boxes)} instances of {ingredient}, picking the top {max_num}...")
    detected_boxes = detected_boxes[:max_num]
    print("detected_boxes:", detected_boxes)

    if visualize:
        # Visualize the detected boxes
        annotated_frame = annotate(
            image_source=image_source, boxes=detected_boxes, logits=logits, phrases=phrases)
        annotated_frame = annotated_frame[..., ::-1]  # BGR to RGB
        annotated_image = Image.fromarray(annotated_frame)
        annotated_image.show()

    # Find the center of the masks
    centers = []
    for detected_box in detected_boxes:
        x1, y1, w, h = detected_box
        center = x1, y1
        center = (int(center[1] * image_source.shape[0]),
                  int(center[0] * image_source.shape[1]))
        centers.append(center)

    return centers
