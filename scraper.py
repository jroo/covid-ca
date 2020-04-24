import os
import threading
import time
import wget

print ('Hello Ontario scraper')
print ('Listening for changes to %s' % os.environ['ONTARIO_STATUS_URL'])


# check for update every 30 minutes
def check_url():
    print ("Checking %s" % time.ctime())
    threading.Timer(60, check_url).start()
    wget.download(os.environ['ONTARIO_STATUS_URL'], 'temp')


if __name__ == '__main__':
    check_url()
