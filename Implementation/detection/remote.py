from pynput.keyboard import Listener

logged_in = set()


def login():
    print('Accepting logins.')

    def pressed(key, logged_in):
        if key.isnumeric():
            if key not in logged_in:
                logged_in.add(key)
                print('User {} logged in.'.format(key))
            else:
                logged_in.discard(key)
                print('User {} logged out.'.format(key))
        else:
            print('Only numbers are accepted for user logins.')

    key_listener = Listener(on_press=lambda key: pressed(key.char, logged_in))
    key_listener.start()


def get_logged_in():
    return logged_in
