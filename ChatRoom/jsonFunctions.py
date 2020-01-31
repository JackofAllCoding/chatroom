import json
def print_msgs(data):
	msgLines=data['msgcount']
	linecounter=0
	dLength=0
	for items in data:
		dLength+=1
	counterH=msgLines-20
	counterB=20
	if counterH <= 0:
		counterH = 1
		counterB=msgLines
	print(data['date'])
	print(data['name'])
	print('+-=============================================-+')
	counterA=0
	for msg in data:
		if counterA  >= counterH:
			if counterA >= msgLines-1:
				break
			counterB=20
			counterB-=counterA
			print(data[str(data['msgcount']-counterB)][0],end='')
			print(": "+data[str(data['msgcount']-counterB)][1])
			linecounter+=1
		counterA+=1
	print(data[str(data['msgcount'])][0],end='')
	print(": "+data[str(data['msgcount'])][1])
def list_rooms(data):
	for room in data:
		print(room)
def get_roomkey(data,room):
	for rooms in data:
		if rooms == room:
			return data[rooms]
def checkroom(data,room):
	value = False
	for rooms in data:
		if rooms == room:
			value = True
			return value
	return value
