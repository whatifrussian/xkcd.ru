#!/usr/bin/env python

# -*- coding: utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import time
import logging
import md5
import xmlrpclib


LJ_TIME_FORMAT = r"%Y-%m-%d %H:%M:%S"


class rpcServer:
        def __init__(self, user, password):
                self.username = user
                self.hpassword = md5.md5(password).hexdigest()
		self.server = xmlrpclib.Server(
			"http://www.livejournal.com/interface/xmlrpc:80")
		self.initialized = True

        def get_challenge(self):
                result = self.server.LJ.XMLRPC.getchallenge()
                return result

	def get_auth(self):
		challenge = self.get_challenge()
		auth = {'auth_method': 'challenge',
			'auth_challenge': challenge['challenge'],
			'auth_response': md5.md5(challenge['challenge'] +
					       self.hpassword).hexdigest()}

		return auth

        def get_last(self):
		request = {'username': self.username,
			   'ver': '1',
			   'lineendings': '0x0A',
			   "selecttype": "lastn",
			   "itemid": -1,
			   "howmany": 1}
		request.update(self.get_auth())
                result = self.server.LJ.XMLRPC.getevents(request)

                return result['events'][0]

        def del_event(self, itemid):
		request = {'username': self.username,
			   'ver': '1',
			   "itemid": itemid}
		request.update(self.get_auth())
                return self.server.LJ.XMLRPC.editevent(request)


        # post is Post or dict with subj, text and tags
        def post(self, post, eventtime=None, journal=None):
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
		if journal:
			request.update({'usejournal': journal})
		request.update(self.get_auth())
                return self.server.LJ.XMLRPC.postevent(request)

        # post is Post or dict {subj, tags, text}
        def edit(self, itemid, eventtime, post):
                moment = time.strptime(eventtime, LJ_TIME_FORMAT)

		if journal is None:
			jounral = self.username

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
