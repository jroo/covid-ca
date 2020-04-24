import os
import time
import threading
import wget

print ('Hello Ontario scraper')
print ('Listening for changes to %s' % os.environ['ONTARIO_STATUS_URL'])


# check for update every 30 minutes
def check_url():
    print ("Checking %s" % time.ctime())
    threading.Timer(1800, check_url).start()
    wget.download(os.environ['ONTARIO_STATUS_URL'], 'temp/ontario.csv')


if __name__ == '__main__':
    check_url()
