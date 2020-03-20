import os
import logging

from commands import activate_commands
from values import updater, dispatcher

def main():
    # Log for errors
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s -%(message)s',
                        level=logging.INFO)

    # Get all commands
    activate_commands()

    # Start polling
    updater.start_polling()


if __name__ == '__main__':
    main()