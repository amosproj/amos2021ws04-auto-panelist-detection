from pynput.keyboard import Listener
from ..registration.register import Register


class Remote:
    def __init__(self, vid):
        self.logged_in = set()
        self.vid = vid

    def pressed(self, key):
        if key.isnumeric():
            if key not in self.logged_in:
                self.logged_in.add(key)
                print('User {} logged in.'.format(key))
            else:
                self.logged_in.discard(key)
                print('User {} logged out.'.format(key))
        elif key == 'r':
            Register().register(self.vid)
        else:
            print('Only numbers are accepted for user logins. Register a new user using "r"')

    def login(self):
        key_listener = Listener(on_press=lambda key: self.pressed(key.char))
        key_listener.start()

    def get_logged_in(self):
        return list(self.logged_in)

