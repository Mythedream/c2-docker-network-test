# log_config.py
import logging

def setup_logging():
    logging.basicConfig(
        filename='app.log', 
        filemode='a', 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    # Logger for keystrokes
    keystroke_logger = logging.getLogger("keystroke_logger")
    keystroke_handler = logging.FileHandler("keystrokes.log")
    keystroke_formatter = logging.Formatter("%(asctime)s: %(message)s")
    keystroke_handler.setFormatter(keystroke_formatter)
    keystroke_logger.setLevel(logging.INFO)
    keystroke_logger.addHandler(keystroke_handler)