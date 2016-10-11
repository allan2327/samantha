
from samantha.brain import Brain
from samantha.io.cmdlistenerspeaker import CommandLineListenerSpeaker
from samantha.modules.ping import Ping
from samantha.modules.administration import Administration


ping = Ping()
admin = Administration()
cmd = CommandLineListenerSpeaker()
brain = Brain(cmd, cmd, [ping, admin])

brain.run()


