import time
from handlers.ColourHandler import ConsoleFormatter


def load_admin_screen(screen):
    """
    Perform admin-related actions based on user input.

    Parameters:
    - screen (Screen): The screen object representing the admin interface.

    Returns:
    - None
    """

    screen.print_welcome_message(f'Welcome back {screen.user_session.username} to Gelos Admin\n')

    actions = ['View Users', 'Change User Password', 'Toggle Shadow Ban', 'Make User Admin', 'Go Back']

    formatted_actions = [ConsoleFormatter.colorize(f"{i + 1}. {action}", 'cyan', ['bold']) for i, action in
                         enumerate(actions)]
    actions_str = "\n".join(formatted_actions)

    print(f"{actions_str}\n")

    action_type = screen.request_handler.call_request('get_action_type')

    if int(action_type) > len(actions):
        # Display an error message if the chosen action is not valid
        screen.print_error_message(f'{action_type} is not a valid choice.')
        screen.clear_screen(3)
        return

    user_chosen_action = actions[int(action_type) - 1]

    if user_chosen_action == 'Go Back':
        screen.load_screen('home')
    elif user_chosen_action == 'View Users':
        view_users_action(screen)
    elif user_chosen_action == 'Toggle Shadow Ban':
        toggle_shadow_ban_action(screen)
    elif user_chosen_action == 'Change User Password':
        change_password_action(screen)
    elif user_chosen_action == 'Make User Admin':
        make_user_admin_action(screen)


def view_users_action(screen):
    """
    View the list of Gelos Enterprise accounts with their roles.

    Parameters:
    - screen (Screen): The screen object representing the admin interface.

    Returns:
    - None
    """

    screen.clear_screen()
    screen.print_welcome_message('Gelos Enterprises Accounts')
    print(f"\n{ConsoleFormatter.colorize('NOTE: ', 'purple', ['bold'])}"
          'This page will auto redirect in 15 seconds\n')

    users = {user: data for user, data in screen.gelos_model.account_data.items()
             if user.lower() != screen.user_session.username.lower()}

    print(f"{ConsoleFormatter.colorize('Normal User', 'green', ['bold'])} - "
          f"{ConsoleFormatter.colorize('Shadow Banned', 'red', ['bold'])}\n")

    for username, data in users.items():
        role = data['role']
        print(ConsoleFormatter.colorize(username, 'red', []) if role == '0' else
              ConsoleFormatter.colorize(f"{username} (Admin)", 'green', ['bold']) if role == '2' else
              ConsoleFormatter.colorize(username, 'green', []))

    time.sleep(15)


def toggle_shadow_ban_action(screen):
    """
    Toggle the shadow-ban status of a user.

    Parameters:
    - screen (Screen): The screen object representing the admin interface.

    Returns:
    - None
    """

    screen.clear_screen()
    screen.print_welcome_message('Gelos Enterprises Shadow Ban')
    print(f"\n\nShadow banning is a {ConsoleFormatter.colorize('SERIOUS', 'red', ['bold', 'underline'])} "
          'action, please ensure you have a valid reason.\n\n'
          f"{ConsoleFormatter.colorize('NOTE: ', 'purple', ['bold'])}"
          'This is a toggle action, so a shadow banned user will be unbanned and vice versa\n')

    user_to_toggle = screen.request_handler.call_request('get_user')
    user_data = screen.gelos_model.account_data.get(user_to_toggle, {})

    if user_data.get('role') == '2':
        screen.print_error_message(f"{user_to_toggle} is an admin, you CANNOT ban admins.")
        screen.clear_screen(3)
        return

    result = screen.gelos_model.toggle_ban(user_to_toggle)
    screen.clear_screen()
    screen.print_welcome_message('Gelos Enterprises Shadow Ban\n')

    if result == '1':
        print(ConsoleFormatter.colorize(f"{user_to_toggle} is now banned", 'red', ['bold']))
    elif result == '0':
        print(ConsoleFormatter.colorize(f"{user_to_toggle} is now unbanned", 'green', ['bold']))
    else:
        print(ConsoleFormatter.colorize(f"{user_to_toggle} is not a valid user. Please try again", 'red', ['bold']))

    screen.clear_screen(3)


def change_password_action(screen):
    """
    Change the password for a Gelos Enterprise account.

    Parameters:
    - screen (Screen): The screen object representing the admin interface.

    Returns:
    - None
    """

    screen.clear_screen()
    screen.print_welcome_message('Gelos Enterprises Password Editor\n')
    user = screen.request_handler.call_request('get_user')

    if user not in screen.gelos_model.account_data:
        screen.print_error_message(f"{user} is not a valid user.")
        screen.clear_screen(3)
        return

    if screen.gelos_model.account_data[user]['role'] == '2':
        screen.print_error_message(f"{user} is an admin, you CANNOT edit admins.")
        screen.clear_screen(3)
        return

    print(f"\n{ConsoleFormatter.colorize('1. Generate your own Password', 'cyan', ['bold'])}\n"
          f"{ConsoleFormatter.colorize('2. Auto Generate Password', 'cyan', ['bold'])}\n")

    auto_generate_password = screen.request_handler.call_request('get_one_or_other')
    password = screen.request_handler.call_request(
        'get_password') if auto_generate_password == '1' else screen.generate_random_password()

    screen.gelos_model.change_password(user, password)

    print(f"\n\n{ConsoleFormatter.colorize(f'Please save the new password for {user}: {password}', 'green', [])}")
    screen.clear_screen(5)


def make_user_admin_action(screen):
    """
    Make a Gelos Enterprise user an admin.

    Parameters:
    - screen (Screen): The screen object representing the admin interface.

    Returns:
    - None
    """

    screen.clear_screen()
    screen.print_welcome_message('Gelos Enterprises Role Editor\n')
    user = screen.request_handler.call_request('get_user')

    if user not in screen.gelos_model.account_data:
        screen.print_error_message(f"{user} is not a valid user.")
        screen.clear_screen(3)
        return

    if screen.gelos_model.account_data[user]['role'] == '2':
        screen.print_error_message(f"{user} is already an admin.")
        screen.clear_screen(3)
        return

    print(f"\nAre you absolutely sure you want to make {user} an admin, you "
          f"{ConsoleFormatter.colorize('CANNOT', 'red', ['bold'])} undo this")
    print(f"\n{ConsoleFormatter.colorize('1. Yes', 'green', ['bold'])}\n"
          f"{ConsoleFormatter.colorize('2. No', 'red', ['bold'])}\n")

    confirmation = screen.request_handler.call_request('get_one_or_other')

    if confirmation == '1':
        screen.gelos_model.make_admin(user)
        print(ConsoleFormatter.colorize(f"\n{user} is now an admin", 'green', ['bold']))
    else:
        print(ConsoleFormatter.colorize(f"\nThe request to make {user} an admin has been cancelled", 'red', ['bold']))

    screen.clear_screen(3)
