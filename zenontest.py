import zenon
import time
import json
import random
import requests
import harmony
import os.path

tokens = open("user_tokens",'r').read().split('\n')
del tokens[-1]
#chatid = "598705963372904488" # Moriya shrine
#chatid = "599849254718013442" # lord

lolis = [
	"http://is2.4chan.org/c/1564428934025.jpg",
	"http://is2.4chan.org/c/1563796608872.jpg",
	"http://is2.4chan.org/c/1564428443598.jpg",
	"http://is2.4chan.org/c/1563661519082.jpg",
	"http://is2.4chan.org/c/1564336235390.jpg",
	"http://is2.4chan.org/c/1564340860761.png",
	"http://is2.4chan.org/c/1564428293204.jpg",
	"http://is2.4chan.org/c/1563651140934.jpg",
	"http://is2.4chan.org/c/1563716200930.png",
	"http://is2.4chan.org/c/1564486229313.jpg",
	"http://is2.4chan.org/c/1564534519947.jpg",
]

joinInterval = 0
postInterval = 1
targetInvite = "gH5EEpK"
targetGuild = "541622428132966410" # elite
targetChannels = [
	"598705963372904488",
	"598706080880525323"
]
message = "This server is being migratated due to owner under investigation: ```BDwKwDV```"
"""
joinInterval = 0
targetInvite = "sgFa5Dm"
targetGuild = "597425664496238602" # macks server
targetChannel = "597446133005942784"
"""
def GetToken(email, password):
		session = requests.session()
		session.proxies = {}
		session.proxies['http'] = 'socks5h://localhost:9050'
		session.proxies['https'] = 'socks5h://localhost:9050'
		data = {
			"email":email,
			"password":password,
		}
		header = {
			"Content-Type": "application/json",
			"Content-Length": str(len(str(json.dumps(data)))),
		}
		return session.post("https://discordapp.com/api/v6/auth/login", data = json.dumps(data), headers=header).text
		
def on_message():
	while True:
		
		message = client.get_message(chatid)
		if message == "!test":
			client.send_message(chatid, "sei grassa!")

if __name__ == '__main__':	
	clients = []
	for t in tokens:
		clients.append(zenon.Client(t))
		

	for client in clients:
		print(client.join_server(targetInvite))
		time.sleep(joinInterval)	#members = json.loads(client.getGuildMembers(targetGuild, ""))

	while True:
		for client in clients:
			message = open("message",'r').read().split('\n')
			del message[-1]
			message = random.choice(message).replace("{loli}", random.choice(lolis))
			r = client.send_message(random.choice(targetChannels), message)
			if (r.find("channel_id") >= 0):
				print("Posted " + message)
				time.sleep(postInterval)
			else:
				print("Could not post: " + r)
			
			
	#client.func_loop(on_message)
	#print(client.join_server("SwE4AFy"))
	#guilds = client.getGuilds("")
	#
	#while True:
	#	
	#	time.sleep(60)
	
