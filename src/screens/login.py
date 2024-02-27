from handlers.ColourHandler import ConsoleFormatter


# Function to load the login screen in the Gelos Enterprises application
def load_login_screen(screen):
    """
    Load the login screen with prompts for username and password input.

    Args:
        screen (ScreenManager): An instance of the ScreenManager class.

    Returns:
        None

    """
    screen.print_welcome_message('Gelos Enterprises Login')
    print(f"\nTo be {ConsoleFormatter.colorize('SUCCESSFUL', 'green', ['bold'])} "
          'you must enter a valid username and password.\n')

    # Request username and password from the user
    username = screen.request_handler.call_request('get_username')
    password = screen.request_handler.call_request('get_password')

    # Attempt to log in with the provided credentials
    action_result = screen.gelos_model.login(username, password)

    if action_result:
        # If login is successful, update user session and load the home screen
        screen.user_session.user_login(username, action_result)
        screen.load_screen('home')
    else:
        # If login fails, display an error message, wait for 3 seconds, and return to the landing screen
        message = 'Invalid username or password.'
        screen.print_error_message(message)
        screen.clear_screen(3)
        screen.load_screen('landing')
