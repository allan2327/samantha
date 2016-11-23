
import sys
from samantha.baseclasses import ListenerBase, SpeakerBase

## hack for python 2
if sys.version_info[0] < 3:
    input = raw_input

class CommandLineListenerSpeaker(ListenerBase, SpeakerBase):
    
    def listen(self):
        while True:
            text = input("(You): ")
            text = text.strip()
            if text:
                return text

    def speak(self, text):
        print('(Samantha): {}'.format(text))
