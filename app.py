import serial
from tkinter import *

start=False
player=0

def startButton(event, start):
	if start==False:
		start =True
		strtText.set("PAUSE")
	else:
		start = False
		strtText.set("START")

def playerButton(event, player):
	if start:
		player = player^1
		plrText.set("PLAYER: "+str(player+1))


#construction for the 3x3 grid
xcoord=[10, 220, 430, 10, 220, 430, 10, 220, 430]
ycoord=[10, 10, 10, 220, 220, 220, 430, 430, 430]
root = Tk()
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
canvas = Canvas(root,width=640,height= 640)
blackBG= canvas.create_rectangle(0,0,640,640,fill="black")
for i in range(9):
    canvas.create_rectangle(xcoord[i],ycoord[i],xcoord[i]+200,ycoord[i]+200,fill="white")
canvas.pack(side=TOP)
#contruction ended here

win = False
ser = serial.Serial("/dev/cu.usbmodem1411",9600) #data from serial monitor
places = [[0]*9,[0]*9] # Array for places 9 by 9 
colourScheme = ["blue","red"] #colour scheme for notifying player 1 and 2 respectively
start = True
if start==True:
    while (True):
        StartButton.bind("<Button-1>",lambda event: startButton(event,start))
        PlayerButton.bind("<Button-1>",lambda event: playerButton(event,player))
        newData = str(ser.readline()) #reading arduino output as input
        newData = newData[2:-5]
        try:
            data = list(map(int,newData.split()))
            for i in range(9):
                if (places[player][i]==0 and places[player^1][i]==0): #checking if the block was previously unoccupied 
                    places[player][i] = data[i]
                    if data[i]==1:
                        canvas.create_rectangle(xcoord[i],ycoord[i],xcoord[i]+200,ycoord[i]+200,fill=colourScheme[player]) #colouring the block
                        player=player^1 #changing the player
        except:
            pass
        print(places[player])
        temp = player
        for player in range(2):
            if(places[player][4]==1):
                if((places[player][0]==1 and places[player][8]==1) or (places[player][1]==1 and places[player][7]==1) or (places[player][2]==1 and places[player][6]==1) or (places[player][3]==1 and places[player][5]==1)):
                    print("royal victory")
            elif((places[player][0]==1 and places[player][3]==1 and places[player][6]==1) or (places[player][0]==1 and places[player][1]==1 and places[player][2]==1)or(places[player][6]==1 and places[player][7]==1 and places[player][8]==1) or (places[player][2]==1 and places[player][5]==1 and places[player][8]==1)):
                print("royal victory")
        player = temp
        root.update()