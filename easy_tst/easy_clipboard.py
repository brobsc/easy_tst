# coding: utf-8

import pyperclip
import time
import tst_wrapper


# Do the checkout from what is in the clipboard
def checkout_from_clipboard():
    # Get what is in clipboard and store it in cv variable
    cv = pyperclip.paste()

    # Remove spaces from cv
    cv = cv.replace(' ', '')

    # Check if cv is a valid code
    if len(cv) != 4:  # Checkout codes always have 4 letters/numbers
        print('Code does not meet base criteria. Skipping...')
    else:
        # Try checkout with code
        try:
            tst_wrapper.get_exercise_stats(cv)
            tst_wrapper.full_checkout(cv)
        except IndexError:
            print('"{}" is not a valid code.'.format(cv))


# Auto-do the checkout if the clipboard changes
def watch_mode():
    # Startup confirmation message and store clipboard
    print('Starting watch mode.')
    cv = pyperclip.paste()

    # Auto-checks changes in the clipboard and interrupt if KeyboardInterrupt
    try:
        while True:
            # Define old clipboard value
            old = cv
            cv = pyperclip.paste()

            # Run checkout from clipboard when clipboard changes
            if cv != old:
                print('Trying to checkout: "{}"'.format(cv))
                checkout_from_clipboard()
            time.sleep(0.1)
    except KeyboardInterrupt:
        # Stop confirmation message
        print('Closing watch mode...')
        pass
