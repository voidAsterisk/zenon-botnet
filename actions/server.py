import requests

class Server(object):
	def __init__(self, token, discord = "https://discordapp.com/api/v6/"):
		self.session = requests.session()
		self.session.proxies = {}
		self.session.proxies['http'] = 'socks5h://localhost:9050'
		self.session.proxies['https'] = 'socks5h://localhost:9050'
		self.discord = discord
		self.token = token
		
	def get_channels(self, serverid):
		return self.session.get(self.discord + "/guilds/"+serverid+"/channels", headers={"Authorization":self.token})
		
	def join_server(self, invite):
		return self.session.post(self.discord + "invite/" + invite, headers={"Authorization":self.token})
		
	def leave_server(self, serverid, proxy):
		return self.session.delete(self.discord + "users/@me/guilds/" + str(serverid), proxies=proxy, headers={"Authorization":self.token}).text

	def createServer(self, logo, name, region, proxy):
		return self.session.post(self.discord + "guilds", headers={"Authorization":self.token}, proxies=proxy, data={"icon":logo, "name":name, "region":region}).text
		
	def kick(self, chatid, userid, reason, proxy):
		return self.session.delete(self.discord + "guilds/" + str(chatid) + "/members/" + str(userid) + "?reason=" + reason, proxies=proxy, headers={"Authorization":self.token}).text
		
	def ban(self, chatid, userid, reason, proxy):
		return self.session.put(self.discord + "guilds/" + str(chatid) + "/bans/" + str(userid) + "?delete-message-days=0&reason=" + reason, proxies=proxy, headers={"Authorization":self.token}).text
		
	
		
