
from samantha.brain import Brain
from samantha.grammar import create_grammar
from samantha.io.cmdlistenerspeaker import CommandLineListenerSpeaker
from samantha.modules.ping import Ping
from samantha.modules.administration import Administration
from samantha.modules.timeanddate import TimeAndDate

modules_and_rules = [
    (Administration, "samantha/rules/admin.yaml"),
    (Ping, "samantha/rules/ping.yaml"),
    (TimeAndDate, "samantha/rules/timeanddate.yaml")
]

modules = []
for module, rules in modules_and_rules:
    g = create_grammar(rules)
    modules.append(module(g))

brain = Brain(modules)


while True:
    text = input("(You): ")
    text = text.strip()
    if not text:
        continue
    response, context = brain.handle(text)
    print('(Samantha): {}'.format(response))
    print(context)
    print('')


