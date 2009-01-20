import lj

# Input LJ username and password.
print 'Enter username:',
user = raw_input()
print 'Enter password:',
password = raw_input()

# Create LJ server instance.
lj_server = lj.rpcServer(user, password)
new_post = lj.Post('this is my title', 'this is <b>text</b>')
result = lj_server.post(new_post) 

# Print post details.
itemid = result['itemid']
url = result['url']
print 'You have created item %d. The URL is: %s' % (itemid, url)

# Pause.
print 'Press enter to delete it.'
raw_input()
# Delete this post.
lj_server.del_event(itemid)
print 'It\'s gone.'
