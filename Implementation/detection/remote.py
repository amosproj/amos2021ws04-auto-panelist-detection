from pynput.keyboard import Listener


class Remote:
    def __init__(self, settings: dict, vid):
        self.logged_in = set()
        self.vid = vid
        self.settings = settings
        self.key_listener = None

    def pressed(self, key):
        if key.isnumeric():
            if key not in self.logged_in:
                self.logged_in.add(key)
                print('User {} logged in.'.format(key))
            else:
                self.logged_in.discard(key)
                print('User {} logged out.'.format(key))
        elif key == 'r':
            self.settings['register'] = True
            if self.key_listener is not None:
                self.key_listener.stop()
        else:
            print('Only numbers are accepted for user logins. Register a new user using "r"')

    def login(self):
        self.key_listener = Listener(on_press=lambda key: self.pressed(key.char))
        self.key_listener.start()

    def get_logged_in(self):
        return list(self.logged_in)

