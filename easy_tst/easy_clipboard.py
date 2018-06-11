# coding: utf-8

from __future__ import print_function, unicode_literals

import pyperclip
import time
import tst_wrapper

CACHE = {}


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
            current_exercise = tst_wrapper.get_exercise_stats(cv, CACHE)
            tst_wrapper.full_checkout(current_exercise)
        except IndexError:
            print('"{}" is not a valid code.'.format(cv))


# Auto-do the checkout if the clipboard changes
def watch_mode():
    # Check login first.
    # FIXME: Don't use global variable. Currently a workaround
    global CACHE

    r = tst_wrapper.request_to_tst()
    CACHE = r.json()

    logged_in = (r.status_code != 400)

    if not logged_in:
        print('Please log on tst (Run tst login).')
        raise RuntimeError('Not logged in tst.')

    # Startup confirmation message and store clipboard
    print('Starting watch mode.')
    cv = pyperclip.paste()

    # Auto-checks changes in the clipboard and interrupt if KeyboardInterrupt
    try:
        started = False
        while True:
            # Define old clipboard value
            old = cv
            cv = pyperclip.paste()


            # Run checkout from clipboard when clipboard changes
            if cv != old or not started:
                if not started: started = True

                if len(cv) > 4:
                    print('Trying to checkout: "{}..."'.format(cv[:10]).replace('\n',' '))
                else:
                    print('Trying to checkout: "{}"'.format(cv))
                checkout_from_clipboard()
            time.sleep(0.1)
    except KeyboardInterrupt:
        # Stop confirmation message
        print('Closing watch mode...')
        pass
