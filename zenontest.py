import zenon
import time
import json
import random
import requests
import harmony
import os.path
import sys
import threading
import atexit

tokens = open("user_tokens",'r').read().split('\n')
del tokens[-1]
messages = open("message",'r').read().split('\n')
del messages[-1]
#chatid = "598705963372904488" # Moriya shrine
#chatid = "599849254718013442" # lord

global terminate
terminate = False
skip_test = False
spammode = "rndseq"
joinInterval = 0
postInterval = 1
targetInvite = "bgcF7sK"
targetserverid = ""
testInvite = "bgcF7sK"
targetChannels = [
	"608399012487495702",
]
message = "This server is being migratated due to owner under investigation: ```BDwKwDV```"
"""
joinInterval = 0
targetInvite = "sgFa5Dm"
targetGuild = "597425664496238602" # macks server
targetChannel = "597446133005942784"
"""
def exitfunc():
	terminate = True
	sys.exit()

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

def FormatMessage(msg):
	msg = msg.replace("\\n", "\n")
	return msg

def on_message():
	while True:
		
		message = client.get_message(chatid)
		if message == "!test":
			client.send_message(chatid, "sei grassa!")
def TestClients(clients):
	print("Starting test.")
	i = 1
	for client in clients:
		r = client.join_server("bgcF7sK") # Test server id
		if "200" in str(r):
			print("Bot " + str(i) + " online.")
		else:
			print("Bot " + str(i) + " offline.")
		client.leave_server("608399012487495700")
	print("Done.")
	
def SpamThreadRandomChannel(client, id):
	while not terminate:
		c = random.choice(targetChannels)
		r = client.send_message(c, FormatMessage(random.choice(messages)))
		if "\"code\": " in str(r) and "\"message\"" in str(r):
			print("Bot " + str(id) + " cannot post in " + c + ": \"" + (json.loads(r))["message"]+"\". Exited.")
			break
		else:
			print("Bot " + str(id) + " posted in " + c)
		time.sleep(postInterval)


def SpamSequentialChannels(client):
	while not terminate:
		for c in targetChannels:
			r = client.send_message(c, FormatMessage(random.choice(messages)))
			if "\"code\": " in str(r) and "\"message\"" in str(r):
				print("Bot " + str(id) + " cannot post in " + c + ": \"" + (json.loads(r))["message"]+"\". Exited.")
				break
			else:
				print("Bot " + str(id) + " posted in " + c)
			time.sleep(postInterval)
	
if __name__ == '__main__':	
	atexit.register(exitfunc)
	clients = []
	for t in tokens:
		clients.append(zenon.Client(t))
	""" 
		MAKE ALL BOTS JOIN TARGET SERVER
	"""
	# Obtain server ID from invite if not given
	if targetserverid == "":
		idbottoken = ""
		with open('invite_to_id_bot') as f:
			idbottoken = f.readline().strip()
		idbot = zenon.Client(idbottoken)
		r = idbot.join_server(targetInvite)
		if "200" not in str(r):
			print("ID bot could not join server to obtain ID. Please edit the invite_to_id or you might risk losing tokens. Or check the invite.")
			sys.exit()
		else:
			print("ID bot joined.")
			g = idbot.getGuilds()
			gjson = json.loads(g)
			targetserverid = gjson[0]["id"]
			print("Target ID: " + targetserverid)
	else:
		print("Target server ID set. No need to use ID bot.")	
	print("Clients joining server.")
	i = 1
	for client in clients:
		if not client.in_server(targetserverid):
			r = client.join_server_safe(targetInvite, targetserverid)
			if "200" in str(r):
				print("Bot " + str(i) + " joined " + targetInvite + ":" + targetserverid)
			elif "already a member" in str(r):
				print("Bot " + str(i) + " already in " + targetInvite + ":" + targetserverid)
			else:
				print("Bot " + str(i) + " cannot join " + targetInvite + ":" + targetserverid)
				client.online = False
			# Only sleep if not last
			if client != clients[-1]:
				time.sleep(joinInterval)
		else:
			print("Bot " + str(i) + " already in " + targetInvite + ":" + targetserverid)
		i += 1
	
	print("Joining complete.")
	
	if spammode == "rndseq":
		print("Spamming random channels one bot at a time")
	if spammode == "rndsim":
		print("Spamming a random channel all the bots at once.")
	i = 1
	if spammode == "rndsim":
		print("Launching threads. Mode: Random channels, simultaneously.")
		for c in clients:
			if not c.online:
				print("Skiped bot " + str(i))
				continue
			t = threading.Thread(target=SpamThreadRandomChannel, args=(c, i))
			t.start()
			print("Launched bot " + str(i))
			i += 1
	if spammode == "seq":
		print("Launching threads. Mode: one channel by one, simultaneously.")
		for c in clients:
			if not c.online:
				print("Skiped bot " + str(i))
				continue
			t = threading.Thread(target=SpamThreadRandomChannel, args=(c, i))
			t.start()
			print("Launched bot " + str(i))
			i += 1
	if spammode == "rndseq":
		while True:
			id = random.randint(0, len(clients)-1)
			c = clients[id]
			while c.online == False:
				id = random.randint(0, len(clients)-1)
				c = clients[id]
			
			ch = random.choice(targetChannels)
			r = c.send_message(ch, FormatMessage(random.choice(messages)))
			if "\"code\": " in str(r) and "\"message\"" in str(r):
				print("Bot " + str(id) + " cannot post in " + c + ": \"" + (json.loads(r))["message"]+"\". Market.")
				c.online = False
				
			else:
				print("Bot " + id + " posted in " + ch)
				time.sleep(postInterval)
	while True:
		continue
	"""
		SPAM MODES:
			rndsim	Random channels all bots simultaneously.
			seqsim  One channel at a time, all the bots simultaneously. 
			rndseq	Random channels one bot after another (random)
			seqseq  One channel after other one bot after other. XXX
			rndseq 	Random channels, one bot after another. XXX
			
			(None)	Do not spam.
	"""
	"""
		ALL THE BOTS ALREADY NOT IN THE SERVER JOINED
	"""
	#client.func_loop(on_message)
	#print(client.join_server("SwE4AFy"))
	#guilds = client.getGuilds("")
	#
	#while True:
	#	
	#	time.sleep(60)
	

