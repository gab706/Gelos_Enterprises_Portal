from handlers.ColourHandler import ConsoleFormatter


# Function to load the register screen in the Gelos Enterprises application
def load_register_screen(screen):
    """
    Load the register screen with prompts for username and password input.

    Args:
        screen (ScreenManager): An instance of the ScreenManager class.

    Returns:
        None

    """
    screen.print_welcome_message('Gelos Enterprises Register')
    print(f"\nTo be {ConsoleFormatter.colorize('SUCCESSFUL', 'green', ['bold'])} "
          'you must enter a unique username.\n')

    # Request username from the user
    username = screen.request_handler.call_request('get_username')

    # Prompt the user to choose between generating their own password or auto-generating one
    print(f"\n{ConsoleFormatter.colorize('1. Generate your own Password', 'cyan', ['bold'])}\n"
          f"{ConsoleFormatter.colorize('2. Auto Generate Password', 'cyan', ['bold'])}\n")

    auto_generate_password = screen.request_handler.call_request('get_auto_generate_chars')

    # Prompt the user for a new password based on their choice
    password = screen.request_handler.call_request(
        'get_password') if auto_generate_password == '1' else screen.generate_random_password()

    # Attempt to register a new user with the provided credentials
    action_result = screen.gelos_model.signup(username, password)

    if action_result:
        # If registration is successful, update user session and display success message
        screen.user_session.user_login(username, action_result)
        screen.clear_screen()
        screen.print_welcome_message('Gelos Enterprises Register')
        print(f"\n\n{ConsoleFormatter.colorize(f'Please save your password: {password}', 'green', [])}")
        screen.clear_screen(5)
        screen.load_screen('home')
    else:
        # If registration fails, display an error message, wait for 3 seconds, and return to the landing screen
        screen.print_error_message(f"Username {username} already exists.")
        screen.clear_screen(3)
        screen.load_screen('landing')
