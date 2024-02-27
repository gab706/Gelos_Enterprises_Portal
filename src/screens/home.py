from handlers.ColourHandler import ConsoleFormatter


# Function to load the home screen in the Gelos Enterprises application
def load_home_screen(screen):
    """
    Load the home screen based on the user's role, allowing various actions.

    Args:
        screen (ScreenManager): An instance of the ScreenManager class.

    Returns:
        None

    """
    screen.clear_screen()
    role = screen.user_session.role

    # Define available actions based on user roles
    actions = {
        '0': ['Logout'],
        '1': ['Change Password', 'Logout'],
        '2': ['Change Password', 'Manage Other Users', 'Logout']
    }.get(role, [])

    # Format and display available actions
    formatted_actions = [ConsoleFormatter.colorize(f"{i + 1}. {action}", 'cyan', ['bold']) for i, action in
                         enumerate(actions)]
    actions_str = "\n".join(formatted_actions)

    screen.print_welcome_message(f'Welcome back {screen.user_session.username}')
    print(f"\nTo better redirect you, you can do the following. \n\n{actions_str}\n")

    # Request user to choose an action
    action_type = screen.request_handler.call_request('get_action_type')

    if int(action_type) > len(actions):
        # Display an error message if the chosen action is not valid
        screen.print_error_message(f'{action_type} is not a valid choice.')
        screen.clear_screen(3)
        return

    user_chosen_action = actions[int(action_type) - 1]

    if user_chosen_action == 'Logout':
        # Logout the user, display a message, wait for 3 seconds, and return to the landing screen
        screen.user_session.user_logout()
        print(f"\n\n{ConsoleFormatter.colorize('Logging you out . . .', 'green', ['bold'])}\n")
        screen.clear_screen(3)
        screen.load_screen('landing')
    elif user_chosen_action == 'Change Password':
        # Prompt the user to choose between generating their own password or auto-generating one
        print(f"\n{ConsoleFormatter.colorize('1. Generate your own Password', 'cyan', ['bold'])}\n"
              f"{ConsoleFormatter.colorize('2. Auto Generate Password', 'cyan', ['bold'])}\n")

        auto_generate_password = screen.request_handler.call_request('get_one_or_other')

        # Prompt the user for a new password based on their choice
        password = screen.request_handler.call_request(
            'get_password') if auto_generate_password == '1' else screen.generate_random_password()

        # Change the user's password and display the new password
        screen.gelos_model.change_password(screen.user_session.username, password)

        print(f"\n\n{ConsoleFormatter.colorize(f'Please save your new password: {password}', 'green', [])}")
        screen.clear_screen(5)
        screen.load_screen('home')
    elif user_chosen_action == 'Manage Other Users':
        # Load the admin screen for managing other users
        screen.load_screen('admin')
