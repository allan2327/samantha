
from collections import defaultdict

from dateutil.zoneinfo import getzoneinfofile_stream, ZoneInfoFile


a = ZoneInfoFile(getzoneinfofile_stream()).zones.keys()

with open('lel.txt', 'w') as output:
    for x in a:
        output.write(x + '\n')

