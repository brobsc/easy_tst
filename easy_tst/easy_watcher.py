# coding: utf-8

from __future__ import print_function, unicode_literals

import pyperclip
import time

import tst_wrapper
import easy_helper


def clipboard_try():
    # Get what is in clipboard and remove spaces
    clipboard = pyperclip.paste().replace(' ', '')

    # Check if clipboard is a valid code
    if len(clipboard) == 4:  # Checkout codes always have 4 letters/numbers
        # Try checkout with code
        try:
            tst_wrapper.main(clipboard)
        except IndexError:
            print('"{}" is not a valid code.'.format(clipboard))
    else:
        print('Trying to checkout: "{}..."'.format(clipboard[:10]).replace('\n', ' '))
        print('Code does not meet base criteria. Skipping...')


def watcher():
    clipboard = pyperclip.paste()

    try:
        started = False
        while True:
            # Define old clipboard value
            old = clipboard
            clipboard = pyperclip.paste()

            # Run checkout from clipboard when clipboard changes or first execution
            if clipboard != old or not started:
                if not started:
                    started = True
                clipboard_try()

            time.sleep(0.1)
    except KeyboardInterrupt:
        # Stop confirmation message
        print('Closing watch mode...')
        return


def main():
    easy_helper.is_logged_in()
    print('Starting watch mode.')

    # Auto-checks changes in the clipboard and interrupt if KeyboardInterrupt
    watcher()
