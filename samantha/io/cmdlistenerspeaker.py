
from samantha.baseclasses import ListenerBase, SpeakerBase

class CommandLineListenerSpeaker(ListenerBase, SpeakerBase):
    
    def listen(self):
        while True:
            text = input("(You): ")
            text = text.strip()
            if text:
                return text

    def speak(self, text):
        print('(Samantha): {}'.format(text))
