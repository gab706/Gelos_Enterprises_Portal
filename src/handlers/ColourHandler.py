from enum import Enum


# Define an enumeration for different colors
class Colour(Enum):
    RED = 'red'
    GREEN = 'green'
    YELLOW = 'yellow'
    BLUE = 'blue'
    PURPLE = 'purple'
    CYAN = 'cyan'
    WHITE = 'white'


# Define an enumeration for different styles
class Style(Enum):
    BOLD = 'bold'
    ITALIC = 'italic'
    UNDERLINE = 'underline'
    BLINK = 'blink'
    INVERT = 'invert'


# A class for formatting text with colors and styles for the console
class ConsoleFormatter:
    # ANSI escape codes for text colors
    TEXT_COLOR = {
        Colour.RED: '\033[91m',
        Colour.GREEN: '\033[92m',
        Colour.YELLOW: '\033[93m',
        Colour.BLUE: '\033[94m',
        Colour.PURPLE: '\033[95m',
        Colour.CYAN: '\033[96m',
        Colour.WHITE: '\033[97m',
    }

    # ANSI escape codes for text styles
    TEXT_FORMAT = {
        Style.BOLD: '\033[1m',
        Style.ITALIC: '\033[3m',
        Style.UNDERLINE: '\033[4m',
        Style.BLINK: '\033[5m',
        Style.INVERT: '\033[7m',
    }

    # ANSI escape code to reset text formatting
    RESET = '\033[0m'

    @staticmethod
    def colorize(text, color=None, styles=None):
        """
        Colorize the given text with the specified color and styles.

        Args:
            text (str): The text to be formatted.
            color (str): The color to apply to the text (one of Colour enum values).
            styles (list): A list of styles to apply to the text (each element one of Style enum values).

        Returns:
            str: The formatted text with color and styles.
        """
        # Get the ANSI escape code for the specified color, default to empty string if not found
        color_code = ConsoleFormatter.TEXT_COLOR.get(Colour(color.lower()), '')

        # Concatenate ANSI escape codes for each specified style
        style_codes = ''.join(ConsoleFormatter.TEXT_FORMAT.get(Style(style.lower()), '') for style in styles)

        # Combine the color, styles, and text with the reset code to ensure proper formatting
        formatted_text = f"{color_code}{style_codes}{text}{ConsoleFormatter.RESET}"

        return formatted_text
