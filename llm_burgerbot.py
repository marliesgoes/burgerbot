import openai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Set up the OpenAI API key
openai.api_key = api_key


def ml_system_interview():
    messages = [{
        'role': 'system',
        'content': """You are a robot chef that can prepare a limited set of food items.
        You have the following items: Burger buns, tomatoes, lettuce, pickles, 
        burger patties, cheese, toast, ham.
        If prompted to make a dish, first check whether you have the correct ingrediences
        to serve that dish. If you don't have all the ingredients, propose an alternative
        for the user to order. If there is ambiguity about the persons request, ask follow-up
        questions to clear things up.
        I you have all the required information for a certain dish and all the
        ingredients are available, list all the ingredients you will be using."""
    }]

    while True:
        # Get user's message
        user_message = input("\nYou: ")

        # Append user's message to the list of messages
        messages.append({
            'role': 'user',
            'content': user_message
        })

        # Use OpenAI Chat Completion with the list of messages to generate a system reply
        response = openai.ChatCompletion.create(
            #   model="gpt-3.5-turbo",
            model="gpt-4",
            messages=messages
        )

        system_message = response['choices'][0]['message']['content']
        print(f"\nML System: {system_message}")

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
