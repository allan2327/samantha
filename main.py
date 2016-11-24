
from samantha.brain import Brain
from samantha.io.cmdlistenerspeaker import CommandLineListenerSpeaker
from samantha.modules.ping import Ping
from samantha.modules.administration import Administration
from samantha.modules.timeanddate import TimeAndDate


ping = Ping()
admin = Administration()

time_and_date = TimeAndDate()
brain = Brain( [ping, admin, time_and_date])

while True:
    text = input("(You): ")
    text = text.strip()
    if not text:
        continue
    response, context = brain.handle(text, {})
    print('(Samantha): {}'.format(response))
    print(context)
    print('')


