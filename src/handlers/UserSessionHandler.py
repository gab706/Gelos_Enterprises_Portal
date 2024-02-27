# A class representing a user session with basic login/logout functionality
class UserSession:
    def __init__(self):
        """
        Initialize a UserSession object with default values.
        """
        self.logged_in = False  # Indicates whether a user is currently logged in
        self.username = None  # Stores the username of the logged-in user
        self.role = 0  # Stores the role/level of access for the logged-in user
        self.current_screen = 'landing'  # Stores the current screen a user is viewing

    def set_current_screen(self, screen_name):
        """
        Set the current screen of a user

        Args:
            screen_name (str): The current screen a user is viewing

        Returns:
            None
        """
        self.current_screen = screen_name.lower()

    def user_login(self, username, role):
        """
        Log in a user by setting the logged_in status, username, and role.

        Args:
            username (str): The username of the user logging in.
            role (int): The role/level of access for the user.

        Returns:
            None
        """
        self.logged_in, self.username, self.role = True, username.lower(), role

    def user_logout(self):
        """
        Log out the current user by resetting the logged_in status, username, and role.

        Returns:
            None
        """
        self.logged_in, self.username, self.role = False, None, 0
