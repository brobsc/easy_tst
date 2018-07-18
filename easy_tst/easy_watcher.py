# coding: utf-8

from __future__ import print_function, unicode_literals

import sys
import pyperclip
import time
import tst_wrapper
import easy_helper
import logging

logger = logging.getLogger('easy_tst')

def clipboard_try():
    logger.debug('Triggered checkout from clipboard')
    # Get what is in clipboard and remove spaces
    clipboard = pyperclip.paste().replace(' ', '')

    # Check if clipboard is a valid code
    if len(clipboard) == 4:  # Checkout codes always have 4 letters/numbers
        # Try checkout with code
        try:
            tst_wrapper.main(clipboard)
        except IndexError:
            logger.warning('"{}" is not a valid code'.format(clipboard))
    else:
        logger.debug('Clipboard contents are greater than 4 chars')
        logger.info('Tried to checkout: "{}..."'.format(clipboard[:10]).replace('\n', ' '))
        logger.info('Code does not meet base criteria. Skipping...')


def watcher():
    clipboard = pyperclip.paste()

    started = False
    while True:
        try:
            # Define old clipboard value
            old = clipboard
            clipboard = pyperclip.paste()

            # Run checkout from clipboard when clipboard changes or first execution
            if clipboard != old or not started:
                if not started:
                    logger.debug('Watch is checking clipboard contents for the first time')
                    started = True
                else:
                    logger.debug('Clipboard has changed')
                clipboard_try()

            time.sleep(0.1)
        except KeyboardInterrupt:
            # Stop confirmation message
            sys.stdout.write("\033[K")  # Clear to the end of line
            logger.info('Closing watch mode...')
            break


def main():
    easy_helper.is_logged_in()
    logger.info('Starting watch mode')

    # Auto-checks changes in the clipboard and interrupt if KeyboardInterrupt
    watcher()
