import requests

class Messages(object):
	def __init__(self, token, Discord = "https://discordapp.com/api/v6/"):
		self.token = token
		self.discord = Discord
		self.session = requests.session()
		self.session.proxies = {}
		self.session.proxies['http'] = 'socks5h://localhost:9050'
		self.session.proxies['https'] = 'socks5h://localhost:9050'
		
		
	def send_message(self, chatid, content): # it can also be use as a private message
		return self.session.post(self.discord + "channels/" + str(chatid) + "/messages#", data={"content":str(content)}, headers={"Authorization":self.token}).text
	
	def send_message_with_tts(self, chatid, content, proxy):
		return self.session.post(self.discord + "channels/" + str(chatid) + "/messages#", proxies=proxy, data={"content":str(content), "nonce":str(chatid), "tts":True}, headers={"Authorization":self.token}).text
		
	def typing_action(self, chatid, proxy):
		return self.session.post(self.discord + "channels/" + str(chatid) + "/typing", proxies=proxy, headers={"Authorization":self.token}).text
	
	def pinMessage(self, chatid, msgid, proxy):
		return self.session.post(self.discord + "channels/" + str(chatid) + "/pins/" + str(msgid), proxies=proxy, headers={"Authorization":self.token}).text
	
	def deleteMessage(self, chatid, messageid, proxy):
		return self.session.delete(self.discord + "channels/" + str(chatid) + "/messages/" + str(messageid), proxies=proxy, headers={"Authorization":self.token}).text
	
	def editMessage(self, chatid, messageid, text, proxy):
		return self.session.patch(self.discord + "channels/" + str(chatid) + "/messages/" + str(messageid), proxies=proxy, headers={"Authorization":self.token}, data={"content":text}).text
		
	def sendFile(self, chatid, file, content, proxy):
		return self.session.post(self.discord + "channels/" + str(chatid) + "/messages", proxies=proxy, headers={"Authorization":self.token, "content":str(content)}, files={"file":open(file, 'rb')}).text
		
	def get_message(self, chatid, proxy):
		res = self.session.get(self.discord + "channels/" + str(chatid) + "/messages?limit=1", proxies=proxy, headers={"Authorization":self.token}).text
		return res.split('"content": "')[1].split('"')[0]
	
	def get_author(self, chatid, proxy):
		res = self.session.get(self.discord + "channels/" + str(chatid) + "/messages?limit=1", proxies=proxy, headers={"Authorization":self.token}).text
		return res.split('"username": "')[1].split('"')[0]
	
	def get_author_id(self, chatid, proxy):
		res = self.sessionself.session.get(self.discord + "channels/" + str(chatid) + "/messages?limit=1", proxies=proxy, headers={"Authorization":self.token}).text
		return res.split('"id": "')[1].split('"')[0]
