__author__ = 'bromix'

from resources.lib.org.bromix import nightcrawler
from resources.lib.de import golem

nightcrawler.run(golem.Provider())
