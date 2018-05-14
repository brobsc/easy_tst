import re
import pyperclip
import tst_wrapper

# Hardcoded regex
# Useless for now
# REGEX_STRING = '.*@ccc\.ufcg\.edu\.br\n*(.*)(?:\n.*ndo\.\.\.)*\n+(.*)'
# Get contents from clipboard

def checkout_from_clipboard():
    cv = pyperclip.paste()

    cv = cv.replace(' ', '')
    # Checkout codes always have 4 letters/numbers
    if len(cv) != 4:
        print('Code does not meet base criteria. Skipping...')
    else:
        try:
            tst_wrapper.get_exercise_stats(cv)
            tst_wrapper.full_checkout(cv)
        except IndexError:
            print('"{}" is not a valid code.'.format(cv))


def watch_mode():
    cv = pyperclip.paste()
    old = ''
    try:
        while True:
            old = cv
            cv = pyperclip.paste()

            # Run checkout from clipboard when clipboard changes
            if cv != old:
                print('Trying to checkout: "{}"'.format(cv))
                checkout_from_clipboard()
    except (KeyboardInterrupt):
        print('Closing watch mode...')
        pass
