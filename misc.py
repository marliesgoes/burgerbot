def print_robot(text):
    green_start = "\033[92m🤖: "
    reset = "\033[0m"
    print(green_start + text + reset)


def print_user(text):
    green_start = "\033[38;5;220m😎: "
    reset = "\033[0m"
    print(green_start + text + reset)
