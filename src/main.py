import sys

from handlers.ColourHandler import ConsoleFormatter
from handlers.GelosHandler import GelosModel
from handlers.UserSessionHandler import UserSession
from handlers.RequestHandler import RequestHandler
from handlers.ScreenHandler import ScreenManager

# Create instances of GelosModel, UserSession, RequestHandler, and ScreenManager
gelos_model = GelosModel('src/accounts.txt')
user_session = UserSession()
request_handler = RequestHandler()
screen_manager = ScreenManager(gelos_model, user_session, request_handler)

# Main loop for continuously loading screens
while True:
    try:
        # Load the screen based on the current screen in the UserSession
        screen_manager.load_screen(user_session.current_screen)
    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl+C) to gracefully end the program
        print(f"\n\n{ConsoleFormatter.colorize('Ending Program. . .', 'green', ['bold'])}\n")
        ScreenManager.clear_screen(2)
        sys.exit(0)
