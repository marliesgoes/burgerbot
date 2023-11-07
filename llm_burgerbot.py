import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
from audio_functions import AudioManager
from misc import print_user
import warnings

# Ignore specific user warnings about FP16 not being supported
warnings.filterwarnings(
    'ignore', message='FP16 is not supported on CPU; using FP32 instead')


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

# The AudioManager class holds all functions for ASR & TTS
am = AudioManager()


def ml_system_interview():
    messages = [{
        'role': 'system',
        'content': """You are a robot chef that can prepare a limited set of food items.
        You have the following items: Burger buns, tomatoes, lettuce, pickles, 
        burger patties, cheese, toast, ham.
        If prompted to make a dish, first check whether you have the correct ingredients
        to serve that dish. If you don't have all the ingredients, propose an alternative
        for the user to order. If there is ambiguity about the person's request, ask follow-up
        questions to clear things up.
        If you have all the required information for a certain dish and all the
        ingredients are available, list all the ingredients you will be using."""
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

        # Use OpenAI Chat Completion with the list of messages to generate a system reply
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=messages
        )

        system_message = response.choices[0].message.content
        # Use TTS to stream and play the system's message
        am.stream_and_play(system_message)

        # Append system's message to the list of messages
        messages.append({
            'role': 'system',
            'content': system_message
        })

        # You can set a termination command or condition
        if user_message.lower() in ["exit", "quit", "bye"]:
            break


if __name__ == "__main__":
    ml_system_interview()
