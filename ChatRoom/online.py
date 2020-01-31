import math,os,os.path,datetime,time,jsonFunctions as jsl,json,requests
from tkinter import *
global userLvl
userLvl = 1
clear = lambda: os.system('cls')
keyCLS = "---CLS"
keyXIT = "---XIT"
keyREN = "---REN"
keyDEL = "---DEL"
os.system("@echo off")
msgLines=0 ##counts number of lines
msgLinesP=0 ##sets itself as msgLines and then compares when the program refreshs to check for new messages
msgCount=0
roomdata = requests.get('https://api.myjson.com/bins/1enq1y').json()

##bellsound & welcome prompt

def Beep():
	global BellSound
	print("                   PY CHAT                    ")
	print("================================================")
	print("      ======                 ================ ")
	print("      |V0.5|                 | Made by: MU  | ")
	print("      ======                 ================ ")
	print()
	print("========================                      ")
	print("|  Enable beep sound?  |                      ")
	print("========================                      ")
	print()
	print("================================================")
	userinput = input("Reply | Y/N ")
	if userinput is 'Y' or userinput is 'y': BellSound = True
	elif userinput is 'N' or userinput is 'n': BellSound = False
	try: 
		if BellSound is False:
			print('',end='')
	except:
		print("Invalid input")
		input()
		clear()
		Beep()
	userNickIn()
	
##input of usernick
def userNickIn():
	global userNick
	clear()
	if BellSound: print("Beep sound		: Enabled")
	else: print("Beep sound		: Disabled")
	print()
	userNick=input("Input your username: ")
	print()
	if len(userNick) > 12:
		print("Inputed username is too long")
		print("Max: 12")
		input()
		clear()
		userNickIn()
	else:
		chatRoomNameIn()
		
def chatRoomNameIn():
	global msgPath
	userLvl = 1
	clear()
	if BellSound: print("Beep sound		: Enabled")
	else: print("Beep sound		: Disabled")
	print()
	print("Your username		: "+userNick)
	print()
	print("Change username		changeusernick")
	print("list rooms		listrooms")
	print()
	ui = input("What room would you like to join? ")
	if ui == "listrooms":
		print()
		print("Rooms:")
		jsl.list_rooms(roomdata)
		input()
		chatRoomNameIn()
	elif jsl.checkroom(roomdata,ui):
		global roomname
		roomname=ui
		global roomkey
		roomkey = jsl.get_roomkey(roomdata,ui)
		screenMode()
	else:
		print("That is not a room.")
		
def screenMode():
	global mode
	clear()
	global roomname
	print("ChatRoom name : ")
	print()
	print(roomname)
	print()
	print("1. Join chatroom")
	print("2. View chatroom with auto-update")
	print("3. View full chatroom without auto-update")
	print()
	print("0. Back")
	print()
	ui = input("Choose what you would like to do: ")
	if ui == "1" or ui == "1.":
		mode = 1
		cmds()
	elif ui == "2" or ui == "2.": 
		mode = 2
		cmds()
	elif ui == "3" or ui == "3.": 
		mode = 3
		cmds()
	elif ui == "0" or ui == "0.": chatRoomNameIn()
	elif ui == 'test1': test()
	else:
		print("invalid input")
		input()
		screenMode()
	
def cmds():
	global mode
	clear()
	os.system("title Python Chatroom")
	print("Instructions")
	print()
	print("Action			Command")
	print()
	print("Refresh screen			[Enter nothing]")
	print("Exit chatroom			---XIT")
	if userLvl==2:
		print("Clear chatroom			---CLS")
		print("Rename chatroom			---REN")
		print("Delete chatroom			---DEL")
	input()
	if mode == 1:
		join()
	elif mode == 2:
		viewAuto()
	elif mode == 3:
		view()
def join():
	clear()
	global roomkey,msgLines,userinput,msgCount,msgLinesP
	try:
		data = requests.get('https://api.myjson.com/bins/'+roomkey).json()
	except:
		msgDisconnected()
	msgLines=data['msgcount']
	if msgLines is not msgLinesP:
		os.system('title Python Chatroom - ' + str(datetime.datetime.now()) + ' New Message')
		if BellSound is True: os.system('start /min sound.vbs')
	else: os.system('title Python Chatroom - ' + str(datetime.datetime.now()))
	msgLinesP = msgLines
	jsl.print_msgs(data)
	userinput=input("["+str(time.strftime('%H'))+":"+time.strftime('%M')+"] "+userNick+": ")
	msgProcess()
	
def viewAuto():
	clear()
	global roomkey
	try:
		r = requests.get('https://api.myjson.com/bins/'+roomkey).json()
		jsl.print_msgs(r)
	except:
		msgDisconnected()
	time.sleep(1)
	viewAuto()
	
def test():
	global roomkey
	r = requests.get('https://api.myjson.com/bins/'+roomkey).json()
	jsl.print_msgs(r)
	
def view():
	clear()
	global roomkey
	try:
		r = requests.get('https://api.myjson.com/bins/'+roomkey).json()
		jsl.print_msgs(r)
	except:
		msgDisconnected()
	input()
	view()
	
def msgDisconnected():
	clear()
	print("Looks like the room you were in is gone... maybe try checking your connection?")
	input()
	Beep()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
def msgProcess():
	global msgLines
	global userinput
	global msgCount
	try: 
		if userinput is "": join()
	except:
		msgBack()
	if userinput == '---XIT': exit()
	if userLvl is 2:
		if userinput == keyCLS: msgCls()
		elif userinput == keyREN: msgRen()
		elif userinput == keyDEL: msgDEL()
	##filtering for empty message
	msgFiltered=userinput
	try: 
		if msgFiltered is "": print("",end="")
	except: msgBack()
	##anti-spam
	msgTime = 0
	msgTime2 = time.strftime('%S')
	if int(msgTime2) - int(msgTime) < 1:
		if msgCount >= 2:
			print()
			print("Slow down, you're sending messages to fast")
			msgBack()
	else:
		msgTime=time.strftime('%S')
		msgCount=0
	msgCount+=1
	##writing to the file
	try:
		r = requests.get('https://api.myjson.com/bins/'+roomkey).json()
	except:
		msgDisconnected()
	part1 = "["+str(time.strftime('%H')+":"+time.strftime('%M'))+"] "+userNick
	dataOutput = {str(r['msgcount']+1):[part1,userinput]}
	r.update(dataOutput)
	r['msgcount'] = r['msgcount']+1
	write = requests.put('https://api.myjson.com/bins/'+roomkey,json=r)
	join()
	
def msgCls():
	exit()
def msgRen():
	exit()
def msgDEL():
	exit()
