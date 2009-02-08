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
import urllib2
from xml.etree.ElementTree import ElementTree

USER_AGENT = 'lj.py (http://bitbucket.org/Davydov/ljpy)'

LJ_TIME_FORMAT = r"%Y-%m-%d %H:%M:%S"

class Server:
        def __init__(self, user, password, user_agent=USER_AGENT,
		     server='www.livejournal.com'):
                self.username = user
                self.hpassword = md5.md5(password).hexdigest()
		self.transport = xmlrpclib.Transport()
		self.user_agent = user_agent
		self.transport.user_agent = self.user_agent
		self.server_name = server
		self.server = xmlrpclib.ServerProxy(
			"http://%s/interface/xmlrpc:80" % self.server_name,
			self.transport)

        def get_challenge(self):
		logging.debug('requesting new challenge')
		result = self.server.LJ.XMLRPC.getchallenge()
		logging.debug('got challenge: %s' % str(result))
		return result

	def get_auth(self):
		challenge = self.get_challenge()
		try:
			auth = {'auth_method': 'challenge',
				'auth_challenge': challenge['challenge'],
				'auth_response': md5.md5(
					challenge['challenge'] +
					self.hpassword).hexdigest()}
		except KeyError, inst:
			raise UnexpectedReply('Server didn\'t returned %s.' %
					      inst.message)      
		logging.debug('auth: %s' % str(auth))

		return auth

	def get_session(self):
		# Should I store session in cache?
		request = {'username': self.username,
			   'ver': '1',
			   'expiration': 'short'}
		request.update(self.get_auth())
		logging.debug('sending sessiongenerate: %s' % str(request))
                result = self.server.LJ.XMLRPC.sessiongenerate(request)
		logging.debug('got result: %s' % str(result))
		try:
			return result['ljsession']
		except KeyError:
			raise UnexpectedReply(
				'Server didn\'t returned ljsession.')

        def get_last(self):
		request = {'username': self.username,
			   'ver': '1',
			   'lineendings': '0x0A',
			   "selecttype": "lastn",
			   "itemid": -1,
			   "howmany": 1}
		request.update(self.get_auth())
		logging.debug('sending getevents: %s' % str(request))
                result = self.server.LJ.XMLRPC.getevents(request)
		logging.debug('got result: %s' % str(result))
                return result['events'][0]

        def del_event(self, itemid):
		request = {'username': self.username,
			   'ver': '1',
			   "itemid": itemid}
		request.update(self.get_auth())
		logging.debug('sending editevent: %s' % str(request))
                result = self.server.LJ.XMLRPC.editevent(request)
		logging.debug('got result: %s' % str(result))
		return result

        # post is Post or dict with subj, text and tags
        def post(self, post, eventtime=None, journal=None,
		 raise_on_premod=False):
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
		logging.debug('sending postevent: %s' % str(request))
                result = self.server.LJ.XMLRPC.postevent(request)
		logging.debug('got result: %s' % str(result))
		try:
			result['itemid']
			result['url']
		except KeyError:
			if raise_on_premod:
				raise UnexpectedReply(
					'Didn\'t expected premoderated.')
			try:
				result['message']
			except KeyError:
				raise UnexpectedReply(
					'Server didn\'t returned message.')
		return result

        # post is Post or dict {subj, tags, text}
        def edit(self, itemid, eventtime, post, journal=None):
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
                if journal:
			request.update({'usejournal': journal})
		request.update(self.get_auth())
		logging.debug('sending editevent: %s' % str(request))
                result = self.server.LJ.XMLRPC.editevent(request)
		logging.debug('got result: %s' % str(result))
		return result

	def get_comments_meta(self, start_id=0, journal=None):
		session = self.get_session()
		headers = {'User-Agent': self.user_agent,
			   'Cookie': 'ljsession=' + session}
		url = 'http://%s/export_comments.bml'\
		    '?get=comment_meta&startid=%d' %\
		    (self.server_name, start_id)
		if journal:
			url += '&authas=%s' % journal
		logging.debug('sending get_comments: %s (%s)' % (
				url, str(headers)))
		request = urllib2.Request(url, None, headers)
		response =  urllib2.urlopen(request)
		result = {}
		tree = ElementTree()
		tree.parse(response)
		result['maxid'] = tree.findtext('maxid')
		comments = tree.find('comments')
		result['comments'] = {}
		for comment in comments.getiterator('comment'):
			attrib = comment.attrib.copy()
			id = int(attrib['id'])
			del attrib['id']
			try:
				attrib['posterid']=int(attrib['posterid'])
			except KeyError:
				pass
			result['comments'][id]=attrib
		usermaps = tree.find('usermaps')
		result['usermaps'] = {}
		for usermap in usermaps.getiterator('usermap'):
			id = int(usermap.attrib['id'])
			user = usermap.attrib['user']
			result['usermaps'][id]=user
		return result


class Post(dict):
	def __init__(self, subject, text, tags=''):
		self['subj'] = subject
		self['text'] = text
		self['tags'] = tags


class Error(Exception):
	"""Base class for exceptions."""
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)

class UnexpectedReply(Error):
	pass
