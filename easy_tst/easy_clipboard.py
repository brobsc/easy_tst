import pyperclip
import tst_wrapper
import time


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
    print('Starting watch mode.')
    cv = pyperclip.paste()
    try:
        while True:
            old = cv
            cv = pyperclip.paste()

            # Run checkout from clipboard when clipboard changes
            if cv != old:
                print('Trying to checkout: "{}"'.format(cv))
                checkout_from_clipboard()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print('Closing watch mode...')
        pass
