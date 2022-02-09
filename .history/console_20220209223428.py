from tkinter import *
import threading
import sys
from turtle import bgcolor
import serial
import serial.tools.list_ports
import serial as sr
#import numeric

# UI Builder
root = Tk()
root.title("Acoustic Pinger Locator")
root.geometry("780x560")

frame = Frame(root)
frame.pack(side=BOTTOM,fill=X)

# Refresh Serial Ports and show in Option Menu
def getSerialPorts():
    global drop
    lista= []
    ports = serial.tools.list_ports.comports()
    for port in ports:
        try:
            if port.manufacturer:
                lista.append(port.device)
            else:
                continue
               # lista.append("No Manufacturer Listed")
                print(port.device + ': No Manufacturer Listed')
        except AttributeError:
            print("\nThis utility requires that pyserial version 3.4 or greater is installed.")
            sys.exit(0)
    if len(lista) == 0:
        lista.append("No Device detected")
    drop.destroy()
    clicked.set("Choose Serial Port")
    drop = OptionMenu(root,clicked, *lista)
    drop.config(width=16,pady=0.1)
    drop.place(relx=0.01,rely=0.01)

def close():
    
    name_serialport.close()
    consoleBox.insert(END, "Connection Closed" +'\n')
    consoleBox.pack(side=BOTTOM,pady=0.1)

## Connect to selected port and frquency and show output on Text Window
def run():
    global consoleBox
    global serialPort
    global name_serialport
    serialPort = clicked.get()
    selectedPort = portClicked.get()
    frequencyChoosen = freqClicked.get()
    try:
        if serialPort == "Choose Serial Port":
            consoleBox.insert(END, "Need to choose Serial Port"+'\n')
            consoleBox.pack(side=BOTTOM,pady=0.1)
        if selectedPort == "Choose Baud Rate":
            consoleBox.insert(END, "Need to choose Baud Rate"+'\n')
            consoleBox.pack(side=BOTTOM,pady=0.1)
            
            name_serialport = sr.Serial(serialPort,int(selectedPort))
        if(frequencyChoosen == "Choose Frequency"):
            consoleBox.insert(END, "Need to choose frequency"+'\n')
            consoleBox.pack(side=BOTTOM,pady=0.1)

        if(frequencyChoosen =="30-60kHz" ):
            d = (1).to_bytes(1,byteorder='big')
            name_serialport.write(d)
        else:
            d_2 = (2).to_bytes(1,byteorder='big')
            name_serialport.write(d_2)
    except ValueError:
        print(ValueError)
        # {Function to run here}
        
        consoleBox.insert(END, serialPort+ ' porta: '+ freqClicked.get()+'\n')
        consoleBox.pack(side=BOTTOM,pady=0.1)

# Drop Down Box 1
lista = ["Click Refresh"]
clicked = StringVar()
clicked.set("Choose Serial Port")
drop = OptionMenu(root,clicked, *lista)
drop.config(width=16,pady=0.1)
drop.place(relx=0.01,rely=0.01)

# Drop Down Box 2
frequencyList = ["30-60kHz", "60-90kHz"]
freqClicked = StringVar()
freqClicked.set("Choose Frequency")
dropFrequency = OptionMenu(root,freqClicked,*frequencyList)
dropFrequency.config(width=11,pady=0.1)
dropFrequency.place(relx=0.46,rely=0.01)

# Drop Down Box 3
portlist = ["4800","9600","19200","57600","115200"]
portClicked = StringVar()
portClicked.set("Choose Baud Rate")
portFrequency = OptionMenu(root,portClicked,*portlist)
portFrequency.config(width=12,pady=0.1)
portFrequency.place(relx=0.26,rely=0.01)

def clearConsole():
    consoleBox.delete("1.0",END)

# Refresh Serial Port Button
refreshBtn = Button(root, text="Refresh Serial Port", command = getSerialPorts )
refreshBtn.config(pady=0.1)
refreshBtn.place(relx=0.65,rely=0.005)

# Clear Console Button
refreshBtn = Button(root, text="Clear Console", command = clearConsole)
refreshBtn.config(pady=0.1,width=12)
refreshBtn.place(relx=0.65,rely=0.05)


# Connect to serial Port and run function
connectBtn = Button(root, text="Connect", command=lambda:threading.Thread(target=run).start() )
connectBtn.config(pady=0.1,width=6)
connectBtn.place(relx=0.85,rely=0.005)

# Close Button
closeBtn = Button(root, text="Close", fg='red', command=lambda:threading.Thread(target=close).start() )
closeBtn.config(pady=0.1,width=6)
closeBtn.place(relx=0.85,rely=0.05)



# Vertical (y) Scroll Bar
scroll = Scrollbar(frame)
scroll.pack(side=RIGHT, fill=Y)

consoleLabel =Label(frame,bg="white",fg="black", text="Console")
consoleLabel.pack(fill=X)

# Console Viewer
consoleBox = Text(frame,height=30,yscrollcommand=scroll.set)
consoleBox.pack(pady=0.1,fill=X)
#consoleBox.config(padx=0.2,pady=0.2)
#consoleBox.pack(side="bottom",fill=X)




root.mainloop()