def print_robot(text):
    green_start = "\033[92m🤖: "
    reset = "\033[0m"
    print(green_start + text.strip() + reset)


def print_user(text):
    green_start = "\033[38;5;220m😎: "
    reset = "\033[0m"
    print(green_start + text.strip() + reset)


def call_gpt(client, messages, model):
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    return response.choices[0].message.content.strip()
