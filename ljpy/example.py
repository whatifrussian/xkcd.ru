from getpass import getpass
from random import random
import logging

import lj


# Enable logging.
logging.basicConfig(level=logging.DEBUG)

# Input LJ username and password.
user = raw_input('Enter username:')
password = getpass('Enter password:')

# Create LJ server instance.
lj_server = lj.Server(user, password)
# We try to create different posts because LJ are not very happy when
# there are several identical posts.
new_post = lj.Post('this is my title', 'this is <b>text</b>' + 
                   str(random()))
result = lj_server.post(new_post) 

# Print post details.
itemid = result['itemid']
url = result['url']
print 'You have created item %d. The URL is: %s' % (itemid, url)

# Pause.
raw_input('Press enter to delete it.')
# Delete this post.
lj_server.del_event(itemid)
print 'It\'s gone.'
