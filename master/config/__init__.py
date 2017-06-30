# Load local options.
import os
import ConfigParser
options = ConfigParser.RawConfigParser()
options.read(os.path.join(os.path.dirname(__file__), 'local.cfg'))
print(os.path.dirname(__file__))
import builders
# import schedulers
import slaves
import status

