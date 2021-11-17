from pynput import keyboard


class Remote:
    def __init__(self):
        self.logged_in = set()

    def login(self) -> None:
        print('Accepting logins. Press ESC when done.')

        with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()

    def on_press(self, key):
        if hasattr(key, 'name') and key.name == 'esc':
            return

        key = key.char
        try:
            if key.isnumeric():
                if key not in self.logged_in:
                    self.logged_in.add(key)
                    print('User {} logged in.'.format(key))
                else:
                    self.logged_in.discard(key)
                    print('User {} logged out.'.format(key))
            else:
                print('Only numbers are accepted for user logins.')
        except AttributeError:
            print('Only numbers are accepted for user logins.')

    def on_release(self, key):
        if key == keyboard.Key.esc:
            print('Login process done')
            return False

    def get_logged_in(self):
        return list(self.logged_in)

