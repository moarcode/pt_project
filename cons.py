from pelix.ipopo.decorators import ComponentFactory, Requires, Instantiate, \
    Validate, Invalidate, Provides
from pelix.shell import SHELL_COMMAND_SPEC
from netaddr import *

@ComponentFactory("service_consumer-factory")
# Dostep do uslug poprzez zdef. zmienne
@Requires('_generator', "generator")
@Requires('_rule', "drop_rule")
# Shell do obslugi uslug
@Provides(SHELL_COMMAND_SPEC)
@Instantiate("service-consumer")
class ServiceConsumer(object):
    def __init__(self):
        """
        Bundle wymanage przez klienta
        """
        self._generator = None
        self._rule = None

    @Validate
    def validate(self, context):
        print "SERVICE CONSUMER STARTED"
    @Invalidate
    def invalidate(self, context):
        print("SERVICE CONSUMER STOPPED")

    def get_namespace(self):
        return "go"

    def get_methods(self):
        return [("go", self.command_line)]

    def command_line(self, io_handler):
        """
        Linia polecen
        """
        passage = None
        rules = self._rule.get_rule()
        packets = []

        while passage != 'quit':
            passage = io_handler.prompt("Command:")
            # Zaladowane reguly
            if passage == "rules":
                for e in rules:
                    print e

            # Generacja pakietow
            elif passage == 'gen':
                passage = io_handler.prompt("Packets:")
                for i in xrange(int(passage)):
                    packets.append(self._generator.run())

            # Sprawdzenie regul
            elif passage == 'check':
                for e in rules:
                    for i in packets:
                        self._rule.check_rule(i, e)
            else:
                print("""   HELP: 
                            gen     =>  generate packets 
                            rules   =>  retrive loaded FW rules
                            check   =>  check FW rules against generated packets
                            quit    =>  quit command-line
                            """)
        io_handler.write_line("Commandline left")

