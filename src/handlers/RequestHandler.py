# A class handling user input requests with predefined prompts and optional validation
class RequestHandler:
    def __init__(self):
        """
        Initialize a RequestHandler object with a dictionary of available user input requests.

        Each request has a corresponding prompt/question and optional validation function.

        """
        self.available_requests = {
            'get_username': {'question': 'Enter your Gelos Enterprises Username'},
            'get_password': {'question': 'Enter your Gelos Enterprises Password'},
            'get_user': {'question': 'Enter the username of the user'},
            'get_one_or_other': {'question': 'Enter your option',
                                 'validation': lambda x: x in {'1', '2'}},
            'get_auto_generate_chars': {'question': 'Enter your option',
                                        'validation': lambda x: all(digit.isdigit() and 1 <= int(digit) <= 3
                                                                    for digit in x.split())},
            'get_auto_generate_length': {'question': 'Enter your desired length (Min. 1, Max. 20)',
                                         'validation': lambda x: x.isdigit() and 1 <= int(x) <= 20},
            'get_action_type': {'question': 'Enter what action you would like to do',
                                'validation': lambda x: int(x) if x.isdigit() else False}
        }

    def call_request(self, request_name):
        """
        Call a specific user input request by providing the request_name.

        Args:
            request_name (str): The name of the requested input.

        Returns:
            str or int or False: The user's input if it passes validation, False otherwise.

        Raises:
            ValueError: If the requested input does not exist.

        """
        request = self.available_requests.get(request_name)

        if not request:
            raise ValueError(f"Request {request_name} does not exist")

        user_input = input(f"{request['question']}: ")
        validation_function = request.get('validation')

        if (validation_function is None or
                (callable(validation_function) and validation_function(user_input))):
            return user_input
        return False
