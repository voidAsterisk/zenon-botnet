import requests

class Reaction(object):
	def __init__(self, token, discord = "https://discordapp.com/api/v6/"):
		self.session = requests.session()
		self.session.proxies = {}
		self.session.proxies['http'] = 'socks5h://localhost:9050'
		self.session.proxies['https'] = 'socks5h://localhost:9050'
		self.token = token
		self.discord = discord
	
	def addReaction(self, chatid, msgid, reactionid, proxy):
		return self.session.put(self.discord  + "channels/" + str(chatid) + "/messages/" + str(msgid) + "/reactions/" + str(reactionid) + "/@me", proxies=proxy, headers={"Authorization":self.token}).text
		
	def removeReaction(self, chatid, msgid, reactionid, proxy):
		return self.session.delete(self.discord + "channels/" + str(chatid) + "/messages/" + str(msgid) + "/reactions/" + str(reactionid) + "/@me", proxies=proxy, headers={"Authorization":self.token}).text
		
	
	
