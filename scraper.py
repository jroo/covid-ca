import os
import wget


print ('Hello Ontario scraper')
print ('URL: %s' % os.environ['ONTARIO_STATUS_URL'])
wget.download(os.environ['ONTARIO_STATUS_URL'], 'temp/ontario.csv')
