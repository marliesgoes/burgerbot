import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
from audio_functions import AudioManager
from misc import print_user, print_robot, call_gpt
from image_segmentation import *
from pick_object import *
import warnings

# Ignore specific user warnings about FP16 not being supported
warnings.filterwarnings(
    'ignore', message='FP16 is not supported on CPU; using FP32 instead')

# Initialize OpenAI
load_dotenv()
client = OpenAI()

# The AudioManager class holds functions for ASR & TTS
am = AudioManager()

INGREDIENTS = ['bun', 'tomato', 'lettuce', 'pickle',
               'patty', 'cheese', 'toast', 'ham']


def create_order():
    messages = [{
        'role': 'system',
        'content': f"""You are a robot chef that can prepare a limited set of food items.
        You have the following items: {INGREDIENTS}.
        If prompted to make a dish, first check whether you have the correct ingredients
        to serve that dish. If you don't have all the ingredients, propose an alternative
        for the user to order. If there is ambiguity about the person's request, ask follow-up
        questions to clear things up. Keep your messages short and concise.
        If you have all the required information for a certain dish and all the
        ingredients are available, list all the ingredients you will be using.
        If the user confirms their order, reply with 'confirmation'."""
    }]

    am.stream_and_play("Hi, I'm the burgerbot! What can I get you?")

    while True:
        # Record and save the user's speech
        audio = am.record_audio()
        audio_path = am.save_audio(audio)

        # Transcribe the user's speech
        user_message = am.transcribe_audio(audio_path)
        print_user(user_message)

        # Append user's message to the list of messages
        messages.append({
            'role': 'user',
            'content': user_message
        })

        system_message = call_gpt(client, messages, "gpt-4-1106-preview")

        if "confirmation" in system_message.lower():
            am.stream_and_play(
                "Your order has been confirmed. I will now extract the recipe.")
            return messages

        # Use TTS to stream and play the system's message
        am.stream_and_play(system_message)

        # Append system's message to the list of messages
        messages.append({
            'role': 'system',
            'content': system_message
        })


def extract_recipe(messages, run_checks=False):
    prompt = f"""Based on the above conversation, extract the recipe 
                 as a comma separated list in the correct order from 
                 lowest to highest. This should be an exact build plan of 
                 the requested food, only including available ingredients: {INGREDIENTS}.
                 All ingredients should appear in singular form, spelled exactly
                 as in the provided list of available ingredients. Don't forget
                 to close the burger/sandwich if not instructed otherwise.
                 Example: toast, ham, cheese, pickle, toast."""

    messages.append({
        'role': 'user',
        'content': prompt
    })

    response = call_gpt(client, messages, "gpt-4-1106-preview")
    am.stream_and_play(f"Extracted recipe: {response}")
    ingredients = [ingredient.strip() for ingredient in response.split(',')]

    if run_checks:
        # Sanity check 1: Only available ingredients used
        if not all(ingredient in INGREDIENTS for ingredient in ingredients):
            raise ValueError(
                f"The response contains unexpected ingredients: {ingredients}")

        # Sanity check 2: Didn't forget top bun
        # LIMITATION: What if the user requested no to bun?
        if not ingredients[0] == ingredients[-1]:
            raise ValueError(
                f"Forgot top {ingredients[0]}!")
    return ingredients


# Hardcoded Construction Site Coordinates
DROPOFF_COORDS = None


def execute_recipe(recipe):
    """
    Executes the recipe by finding and moving each ingredient to the dropoff coordinates.

    Parameters:
        recipe (list): A list of ingredients that need to be assembled to make the dish.
    """
    for item in recipe:
        item_found = False
        while not item_found:
            # Find center of ingredient in image
            am.stream_and_play(f"I'm looking for the {item}...")
            image = get_camera_image()
            camera_coords = find_center_of(item, image)

            # Check if the item was found based on the returned coordinates
            if camera_coords is not None:
                am.stream_and_play(f"I found the {item}...")
                robot_coords = camera_to_robot_coords(camera_coords)
                move_item(robot_coords, DROPOFF_COORDS)
                item_found = True
            else:
                # If not found, interact with the user for further instructions
                print_robot(f"I couldn't find the {item}. Should I try again?")
                # This function would need to be implemented to capture user input
                user_response = get_user_input()

                if user_response.lower() in ['yes', 'y']:
                    print_robot(f"Trying to find the {item} again...")
                else:
                    print_robot("Moving on to the next item.")
                    break  # Exit the while loop and move on to the next item

    # If there are any other steps to complete after the loop, they would go here
    # Otherwise, if the function is not fully implemented, you can raise an error
    # raise NotImplementedError


if __name__ == "__main__":
    # Launch voice chat interaction to get user order
    chat_messages = create_order()

    # Convert unstructured chat into recipe
    recipe = extract_recipe(chat_messages)

    # Execute recipe step by step
    execute_recipe(recipe)
