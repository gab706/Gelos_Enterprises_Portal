from handlers.ColourHandler import ConsoleFormatter


# Function to load the landing screen in the Gelos Enterprises application
def load_landing_screen(screen):
    """
    Load the landing screen with prompts for user authentication type (Login or Register).

    Args:
        screen (ScreenManager): An instance of the ScreenManager class.

    Returns:
        None

    """
    screen.print_welcome_message('Welcome to Gelos Enterprises')
    print(f"\n{ConsoleFormatter.colorize('1. Login', 'cyan', ['bold'])}\n"
          f"{ConsoleFormatter.colorize('2. Register', 'cyan', ['bold'])}\n")

    # Request user to choose between Login (1) or Register (2)
    authenticate_type = screen.request_handler.call_request('get_one_or_other')

    if not authenticate_type or authenticate_type not in ('1', '2'):
        # If an invalid choice is made, display an error message, wait for 3 seconds, and clear the screen
        screen.print_error_message('Invalid request type.')
        return screen.clear_screen(3)

    # Load either the login or register screen based on the user's choice
    screen.load_screen('login' if authenticate_type == '1' else 'register')
