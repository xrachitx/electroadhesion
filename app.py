import serial
from tkinter import *

def startButton(event):
	global start
	print(start)
	if start==False:
		start =True
		strtText.set("PAUSE")
	else:
		start = False
		strtText.set("START")

def playerButton(event):
	global player
	if start:
		player = player^1
		plrText.set("PLAYER: "+str(player+1))


start = False # boolean to represent Start/Pause state
root = Tk()
player = 0 # denotes the player

#construction for the 3x3 grid
xcoord=[10, 220, 430, 10, 220, 430, 10, 220, 430]
ycoord=[10, 10, 10, 220, 220, 220, 430, 430, 430]
topFrame = Frame(root)
topFrame.pack()
buttonFrame = Frame(root)
buttonFrame.pack(fill = X,side = BOTTOM)
strtText = StringVar()
StartButton = Button(buttonFrame,textvariable=strtText,fg="black")
strtText.set("START")
plrText = StringVar()
PlayerButton = Button(buttonFrame,textvariable= plrText,fg="black")
plrText.set("PLAYER: "+str(player+1))
buttonFrame.columnconfigure(0, weight=1)
buttonFrame.columnconfigure(1, weight=1)
StartButton.grid(row=0,column=0,sticky= W+E)
PlayerButton.grid(row=0,column=1,sticky=W+E)
StartButton.bind("<Button-1>",lambda event: startButton(event))
PlayerButton.bind("<Button-1>",lambda event: playerButton(event))
canvas = Canvas(root,width=640,height= 640)
blackBG= canvas.create_rectangle(0,0,640,640,fill="black")
for i in range(9):
	canvas.create_rectangle(xcoord[i],ycoord[i],xcoord[i]+200,ycoord[i]+200,fill="white")
canvas.pack(side=TOP)
#contruction ended here


ser = serial.Serial("/dev/cu.usbmodem1411",9600) #data from serial monitor
places = [[0]*9,[0]*9] # Array for places 9 by 9 
colourScheme = ["blue","red"] #colour scheme for notifying player 1 and 2 respectively

if start:
	while (True):
		newData = str(ser.readline())
		newData = newData[2:-5]
		data = list(map(int,newData.split()))
		try:
			for i in range(9):
				if (places[player][i]==0 and places[player^1][i]==0):
					places[player][i] = data[i]
		except IndexError:
			pass
		for i in range(9):
			if places[player][i] == 1:
				canvas.create_rectangle(xcoord[i],ycoord[i],xcoord[i]+200,ycoord[i]+200,fill=colourScheme[player])

root.mainloop()