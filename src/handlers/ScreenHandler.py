import random
import string
import time
import os

from handlers.ColourHandler import ConsoleFormatter

from screens.login import load_login_screen
from screens.register import load_register_screen
from screens.landing import load_landing_screen
from screens.home import load_home_screen
from screens.admin import load_admin_screen


# A class managing different screens in the Gelos Enterprises application
class ScreenManager:
    def __init__(self, gelos_model, user_session, request_handler):
        """
        Initialize a ScreenManager object with GelosModel, UserSession, and RequestHandler instances.

        Args:
            gelos_model (GelosModel): An instance of the GelosModel class.
            user_session (UserSession): An instance of the UserSession class.
            request_handler (RequestHandler): An instance of the RequestHandler class.

        """
        self.gelos_model = gelos_model
        self.user_session = user_session
        self.request_handler = request_handler

        # Dictionary mapping screen names to corresponding load functions
        self.screens = {
            'login': load_login_screen,
            'register': load_register_screen,
            'landing': load_landing_screen,
            'home': load_home_screen,
            'admin': load_admin_screen
        }

    def load_screen(self, screen_name):
        """
        Load the specified screen based on the provided screen_name.

        Args:
            screen_name (str): The name of the screen to be loaded.

        Returns:
            None

        Raises:
            ValueError: If the requested screen does not exist.

        """
        self.clear_screen(0)
        if screen_name.lower() in self.screens:
            self.user_session.set_current_screen(screen_name.lower())
            self.screens[screen_name.lower()](self)
        else:
            raise ValueError(f"Screen {screen_name} not found.")

    ###################
    # Global Functions
    ###################

    def generate_random_password(self):
        """
        Generate a random password based on user input for character types and length.

        Returns:
            str: The generated password.

        """
        self.clear_screen()
        self.print_welcome_message('Gelos Enterprises Register')

        print('\nPlease select what kinds of characters you want\n\n'
              f"{ConsoleFormatter.colorize('NOTE: ', 'purple', ['bold'])}"
              'You can select multiple by adding a space between the numbers. Example "1 2 3" selects all '
              'options.\n\n'
              f"{ConsoleFormatter.colorize('1. Letters', 'cyan', ['bold'])}\n"
              f"{ConsoleFormatter.colorize('2. Numbers', 'cyan', ['bold'])}\n"
              f"{ConsoleFormatter.colorize('3. Symbols', 'cyan', ['bold'])}\n")
        allowed_chars = self.request_handler.call_request('get_auto_generate_chars')

        print(f"\n{ConsoleFormatter.colorize('1. Use default length (10)', 'cyan', ['bold'])}\n"
              f"{ConsoleFormatter.colorize('2. Choose your own length', 'cyan', ['bold'])}\n")

        auto_generate_length_permission = self.request_handler.call_request('get_one_or_other')

        auto_generate_length = 10 if auto_generate_length_permission == '1' else self.request_handler.call_request(
            'get_auto_generate_length')

        password = self.__generate_random_password(allowed_chars, auto_generate_length)

        return password

    @staticmethod
    def print_welcome_message(msg):
        """
        Print a welcome message in a stylized format.

        Args:
            msg (str): The message to be displayed.

        Returns:
            None

        """
        print(ConsoleFormatter.colorize(msg, 'yellow', ['bold']))

    @staticmethod
    def print_error_message(msg):
        """
        Print an error message in a stylized format.

        Args:
            msg (str): The error message to be displayed.

        Returns:
            None

        """
        print(ConsoleFormatter.colorize(f"\n{msg} Please try again.\n", 'red', ['bold']))

    @staticmethod
    def clear_screen(delay=None):
        """
        Clear the console screen with an optional delay.

        Args:
            delay (float): Optional delay in seconds before clearing the screen.

        Returns:
            None

        """
        if delay is not None:
            time.sleep(delay)
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def __generate_random_password(allowed_chars, length):
        """
        Generate a random password based on allowed characters and specified length.

        Args:
            allowed_chars (str): String containing selected character types.
            length (int): The desired length of the password.

        Returns:
            str: The generated password.

        Raises:
            ValueError: If no valid characters are selected.

        """
        chars = ''.join([string.ascii_letters if '1' in allowed_chars else '',
                         string.digits if '2' in allowed_chars else '',
                         string.punctuation.replace(" ", "") if '3' in allowed_chars else ''])
        if not chars:
            raise ValueError('No valid characters selected.')
        return ''.join(random.choice(chars) for _ in range(int(length)))
