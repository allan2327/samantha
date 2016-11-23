
from samantha.brain import Brain
from samantha.io.cmdlistenerspeaker import CommandLineListenerSpeaker
from samantha.modules.ping import Ping
from samantha.modules.administration import Administration
from samantha.modules.timeanddate import TimeAndDate


ping = Ping()
admin = Administration()
cmd = CommandLineListenerSpeaker()
time_and_date = TimeAndDate()
brain = Brain(cmd, cmd, [ping, admin, time_and_date])

brain.run()


