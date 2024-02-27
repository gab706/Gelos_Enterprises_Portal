# A class representing a simple user account management system
class GelosModel:
    def __init__(self, accounts_file):
        """
        Initialize a GelosModel object with the specified accounts file.

        Args:
            accounts_file (str): The path to the file containing user account information.

        Raises:
            ValueError: If accounts_file is not provided.
        """
        if not accounts_file:
            raise ValueError('You must provide an accounts file')
        self.accounts_file = accounts_file
        self.account_data = {}
        self.__read_accounts()

    def login(self, username, password):
        """
        Attempt to log in a user with the provided username and password.

        Args:
            username (str): The username of the user attempting to log in.
            password (str): The password for the user attempting to log in.

        Returns:
            bool or str: The role of the user if login is successful, False otherwise.
        """
        self.__read_accounts()
        return self.account_data.get(username.lower(), {}).get('role') if (self.account_data.get(username.lower(), {})
                                                                           .get('pwd') == password) else False

    def signup(self, username, password):
        """
        Attempt to create a new user account with the provided username and password.

        Args:
            username (str): The desired username for the new user account.
            password (str): The password for the new user account.

        Returns:
            bool or str: The role of the new user if signup is successful, False otherwise.
        """
        self.__read_accounts()
        if username.lower() not in self.account_data:
            self.__write_account(username.lower(), password, '1')
            return '1'
        return False

    def change_password(self, username, new_password):
        """
        Change the password for the specified username.

        Args:
            username (str): The username for which to change the password.
            new_password (str): The new password to set for the user.

        Returns:
            bool: True if the password change is successful, False otherwise.
        """
        self.__read_accounts()
        if username.lower() in self.account_data:
            self.account_data[username.lower()]['pwd'] = new_password

            with open(self.accounts_file, 'w') as file_handle:
                for user, data in self.account_data.items():
                    password = data['pwd']
                    role = data['role']
                    file_handle.write(f"{user} {password} {role}\n")

    def toggle_ban(self, username):
        """
        Toggle the ban status (role) of a user in the account data.

        Parameters:
            username (str): The username to toggle ban status for.

        Returns:
            bool: True if the toggle was successful, False otherwise.
        """

        # Convert username to lowercase for case-insensitive comparison
        self.__read_accounts()
        username_lower = username.lower()

        if username_lower in self.account_data:
            user_data = self.account_data[username_lower]

            # Toggle the user's role between '0' and '1'
            user_data['role'] = '0' if user_data['role'] == '1' else '1'

            with open(self.accounts_file, 'w') as file_handle:
                for user, data in self.account_data.items():
                    file_handle.write(f"{user} {data['pwd']} {data['role']}\n")
            return '0' if user_data['role'] == '1' else '1'
        return False

    def make_admin(self, username):
        """
        Convert a user account to admin

        Parameters:
            username (str): The username to make an admin

        Returns:

        """

        # Convert username to lowercase for case-insensitive comparison
        self.__read_accounts()
        username_lower = username.lower()

        if username_lower in self.account_data:
            user_data = self.account_data[username_lower]

            # Toggle the user's role between '0' and '1'
            user_data['role'] = '2'

            with open(self.accounts_file, 'w') as file_handle:
                for user, data in self.account_data.items():
                    file_handle.write(f"{user} {data['pwd']} {data['role']}\n")

    # Private method to read user accounts from the specified file
    def __read_accounts(self):
        """
        Read user accounts from the specified accounts file.

        Returns:
            None
        """
        with open(self.accounts_file, 'r') as file_handle:
            self.account_data = {
                user: {'pwd': pwd, 'role': role}
                for line in map(str.strip, file_handle)
                if (parts := line.split(' ', 2)) and len(parts) == 3
                for user, pwd, role in [parts]
            }

    # Private method to write a new user account to the accounts file
    def __write_account(self, username, password, role):
        """
        Write a new user account to the accounts file.

        Args:
            username (str): The username for the new user account.
            password (str): The password for the new user account.
            role (str): The role/level of access for the new user account.

        Raises:
            ValueError: If the username is already in use.
        """
        if username.lower() in self.account_data:
            raise ValueError(f"{username} is already in use")
        with open(self.accounts_file, 'a') as file_handle:
            file_handle.write(f"{username} {password} {role}\n")
