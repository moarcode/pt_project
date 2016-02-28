# iPOPO decorators
from pelix.ipopo.decorators import ComponentFactory, Provides, Instantiate, Validate, Invalidate
import random
from netaddr import *

# Manipulates the class and sets its (unique) factory name
@ComponentFactory("Packet Generator")
# Indicate that the components will provide a service
@Provides("generator")
# Tell iPOPO to instantiate a component instance as soon as the file is loaded
@Instantiate("packet_generator-provider")
# A component class must always inherit from object (new-style class)


class Generator(object):
    @Validate
    def validate(self, context):
        print("Generator has been has been started.")

    @Invalidate
    def invalidate(self, context):
        print("Packet generator has been stopped.")

    def run(self):
        self.ip_src = IPAddress('192.168.10.10') + random.getrandbits(3)
        self.port_src = random.randint(1,256),
        self.ip_dst = IPAddress('0.0.0.0') + random.getrandbits(32)
        self.port_dst = random.randint(1,256)

        return {"ip_src":self.ip_src, "port_src":self.port_src, 
                "ip_dst":self.ip_dst, "port_dst":self.port_dst}

