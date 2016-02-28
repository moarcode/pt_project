# iPOPO decorators
from pelix.ipopo.decorators import ComponentFactory, Provides, Instantiate, Validate, Invalidate
import random
from netaddr import *
import logging

# Ustawienia loggera
logger = logging.getLogger('Firewall')
hdlr = logging.FileHandler('./fw.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)         # INFO
#logger.setLevel(logging.DEBUG)       # DEBUG

# Manipulates the class and sets its (unique) factory name
@ComponentFactory("Drop Rule")
# Indicate that the components will provide a service
@Provides("drop_rule")
#@Requires("_svc", "generator")
# Tell iPOPO to instantiate a component instance as soon as the file is loaded
@Instantiate("drop_rule-provider")
# A component class must always inherit from object (new-style class)
class DropRule(object):

    """
    Reguly FW
    """
    rules = [
            {"net_src":IPNetwork('192.168.10.11/32'), 
            "net_dst":IPNetwork('192.168.10.10/31'), 
            "port_src":444, 
            "port_dst":22},

            {"net_src":IPNetwork('192.168.10.12/32'), 
            "net_dst":IPNetwork('192.168.10.10/31'), 
            "port_src":756, 
            "port_dst":80}
            ]

    @Validate
    def validate(self, context):
        print("Drop Rule Bundle has been started")

    @Invalidate
    def invalidate(self, context):
        print("Drop Rule Bundle has been stopped.")

    def get_rule(self):
        return self.rules

    def check_rule(self, p, rule): 
        """
        Sprawdzenie regul FW
        Logowanie do pliku
        """
        if p["ip_src"] in list(rule["net_src"]):
            logger.info("[DROPPED] IP_SRC=%s" % p["ip_src"])
            return True
        elif p["ip_dst"] in list(rule["net_dst"]):
            logger.info("[DROPPED] IP_DST=%s" % p["ip_dst"])
            return True
        elif p["port_src"] == rule["port_src"]:
            logger.info("[DROPPED] PORT_SRC=%s" % p["port_src"])
            return True
        elif p["port_dst"] == rule["port_dst"]:
            logger.info("[DROPPED] PORT_DST=%s" % p["port_dst"])
            return True
        else:
            logger.debug("[PASSED] IP_SRC=%s, IP_DST=%s, PORT_SRC=%s, PORT_DST=%s" %(
                        p["ip_src"], p["ip_dst"], p["port_src"], p["port_dst"])
                        )
            return False

