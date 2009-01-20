#!/usr/bin/env python
# -*- coding: utf-8 -*-
# this file comes from git://github.com/egv/zapys-maemo.git/ 


import xmlrpclib, time, md5

LJ_TIME_FORMAT = r"%Y-%m-%d %H:%M:%S"

class rpcServer:
        username = ''
        password = ''
        initialized = False

        last_event = {}

        def __init__(self, user, password):
                self.username = user
                self.hpassword = md5.md5(password).hexdigest()

        def connect(self):
                if not self.initialized:
                        self.server = xmlrpclib.Server("http://www.livejournal.com/interface/xmlrpc:80")
                        self.initialized = True

        def get_challenge(self):
		self.connect()
                result = self.server.LJ.XMLRPC.getchallenge()
                return result

	def get_auth(self):
		challenge = self.get_challenge()
		auth = {'auth_method': 'challenge',
			'auth_challenge': challenge['challenge'],
			'auth_respnse': md5.md5(challenge['challenge'] +
					       self.hpassword)}
		return auth

        def get_last(self):
                self.connect()
		request = {'username': self.username,
			   'ver': '1',
			   'lineendings': '0x0A',
			   "selecttype": "lastn",
			   "itemid": -1,
			   "howmany": 1}
		request.update(self.get_auth()))
                result = self.server.LJ.XMLRPC.getevents(

                return result['events'][0]

        def del_event(self, itemid):
		request = {'username': self.username,
			   'ver': '1',
			   "itemid": itemid}
		request.update(self.get_auth())
                return self.server.LJ.XMLRPC.editevent(request)


        # post is Post or dict with subj, text and tags
        def post(self, post, eventtime = None):
                self.connect()
                if eventtime == None:
                        moment = time.localtime()
                else:
                        moment = time.strptime(eventtime, LJ_TIME_FORMAT)

		request = {'username': self.username,
			   'clientversion': 'Zapys/0.8',
			   'ver':'1',
			   'event': post['text'],
			   'subject': post['subj'],
			   'props': {'taglist': post['tags'],
				     'opt_preformatted': True},
			   'year': moment[0],
			   'mon': moment[1],
			   'day': moment[2],
			   'hour': moment[3],
			   'min': moment[4],
			   'lineendings':'0x0A'}
		request.update(self.get_auth())
                return self.server.LJ.XMLRPC.postevent(request)

        # post is disct {subj, tags, text}
        def edit(self, itemid, eventtime, post ):
                moment = time.strptime(eventtime, LJ_TIME_FORMAT)

		request = {'username': self.username,
			   'ver': '1',
			   "itemid": itemid,
			   'event': post['text'],
			   'subject': post['subj'],
			   'props': {'taglist': post['tags'],
				     'opt_preformatted': True},
			   'year': moment[0],
			   'mon': moment[1],
			   'day': moment[2],
			   'hour' : moment[3],
			   'min': moment[4]}
		request.update(self.get_auth())
                return self.server.LJ.XMLRPC.editevent(request)


class Post(dict):
	def __init__(self, subject, text, tags=''):
		self['subj'] = subject
		self['text'] = text
		self['tags'] = tags
