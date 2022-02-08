from tkinter import *
import threading
import sys
import serial
import serial.tools.list_ports
import serial as sr

# UI Builder
root = Tk()
root.title("Acoustic Pinger Locator")
root.geometry("780x560")

# Refresh Serial Ports and show in Option Menu
def getSerialPorts():
    global drop
    lista= []
    ports = serial.tools.list_ports.comports()
    for port in ports:
        try:
            if port.manufacturer:
                lista.append(port.name)
            else:
                continue
               # lista.append("No Manufacturer Listed")
                print(port.device + ': No Manufacturer Listed')
        except AttributeError:
            print("\nThis utility requires that pyserial version 3.4 or greater is installed.")
            sys.exit(0)
    drop.destroy()
    clicked.set("Choose Serial Port")
    drop = OptionMenu(root,clicked, *lista,)
    drop.config(width=13,pady=0.1)
    drop.place(relx=0.01,rely=0.01)
    
## Connect to selected port and frquency and show output on Text Window
def run():
    global consoleBox
    global serialPort
    serialPort = clicked.get()
    selectedPort = portClicked.get()
    frequencyChoosen = freqClicked.get()
    if(frequencyChoosen =="30-60kHz" ):
        freq = 0
        #s_serial.write(freq)
    else:
        freq = 1
        #s.serial.write(freq)

    # {Function to run here}
    name_serialport = sr.Serial(serialPort,int(selectedPort))  
    consoleBox.insert(END, serialPort+ ' porta: '+ freqClicked.get()+'\n')
    consoleBox.pack(side=BOTTOM,pady=0.1)

# Drop Down Box 1
lista = ["Click Refresh"]
clicked = StringVar()
clicked.set("Choose Serial Port")
drop = OptionMenu(root,clicked, *lista,)
drop.config(width=13,pady=0.1)
drop.place(relx=0.01,rely=0.01)

# Drop Down Box 2
frequencyList = ["30-60kHz", "60-90kHz"]
freqClicked = StringVar()
freqClicked.set("Choose Frequency")
dropFrequency = OptionMenu(root,freqClicked,*frequencyList)
dropFrequency.config(width=11,pady=0.1)
dropFrequency.place(relx=0.35,rely=0.01)

# Drop Down Box 3
portlist = ["4800","9600","19200","57600","115200"]
portClicked = StringVar()
portClicked.set("Choose Baud Rate")
portFrequency = OptionMenu(root,portClicked,*portlist)
portFrequency.config(width=12,pady=0.1)
portFrequency.place(relx=0.23,rely=0.01)



# Refresh Serial Port Button
refreshBtn = Button(root, text="Refresh Serial Port", command = getSerialPorts )
refreshBtn.config(pady=0.1)
refreshBtn.place(relx=0.75,rely=0.01)

# Connect to serial Port and run function
connectBtn = Button(root, text="Connect", command=lambda:threading.Thread(target=run).start() )
connectBtn.config(pady=0.1)
connectBtn.place(relx=0.60,rely=0.01)

# Vertical (y) Scroll Bar
scroll = Scrollbar(root)
scroll.pack(side=RIGHT, fill=Y)

# Console Viewer
consoleBox = Text(root,width=90,height=35,yscrollcommand=scroll.set)
consoleBox.pack(side=BOTTOM,pady=0.1)




root.mainloop()