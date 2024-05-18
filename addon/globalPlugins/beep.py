import speech
import tones
import globalPluginHandler
import logging
import ui

# Configure logging
logging.basicConfig(filename="nvda_plugin.log", level=logging.DEBUG,
                    format='%(asctime)s %(message)s')


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self):
        """Initialize the GlobalPlugin."""
        super(GlobalPlugin, self).__init__()
        self.bindGestures()
        logging.info("Text Sound Addon initialized")
        self.originalSpeak = speech.speak
        speech.speak = self.customSpeak
        logging.debug("Original speech function overridden with customSpeak")

    def customSpeak(self, text, *args, **kwargs):
        """Custom speech function to intercept and modify speech output."""
        try:
            logging.info(f"customSpeak called with text: {text}")
            self.onSpeech(text)
            self.originalSpeak(text, *args, **kwargs)
        except Exception as e:
            logging.error(f"Error in customSpeak: {e}")

    def onSpeech(self, text):
        """Handle speech text and provide custom messages."""
        try:
            logging.info(f"onSpeech called with text: {text}")
            ui.message("Dos")
            logging.debug("Message 'Dos' sent to UI")
        except Exception as e:
            logging.error(f"Error in onSpeech: {e}")

    def terminate(self):
        """Restore the original speech function when the plugin is terminated."""
        speech.speak = self.originalSpeak
        super(GlobalPlugin, self).terminate()
        logging.info("Text Sound Addon terminated")

    def bindGestures(self):
        """Bind gestures to specific actions."""
        self.bindGesture("kb:NVDA+shift+s", "playSound")

    def script_playSound(self, gesture):
        """Play a simple beep sound."""
        logging.info("script_playSound called")
        tones.beep(750, 200)  # Beep at 750 Hz for 200 ms

    # Provide a description for the script
    script_playSound.__doc__ = "Plays a beep sound when pressed."
    