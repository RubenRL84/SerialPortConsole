from tkinter import *
import threading
import sys
import serial
import serial.tools.list_ports

# UI Builder
root = Tk()
root.title("Acoustic Pinger Locator")
root.geometry("580x360")

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
                lista.append("No Manufacturer Listed")
                print(port.device + ': No Manufacturer Listed')
        except AttributeError:
            print("\nThis utility requires that pyserial version 3.4 or greater is installed.")
            sys.exit(0)
    drop.destroy()
    clicked.set("Choose Serial Port")
    drop = OptionMenu(root,clicked, *lista,)
    drop.config(width=11,pady=0.1)
    drop.place(relx=0.01,rely=0.01)
    
## Connect to selected port and frquency and show output on Text Window
def run():
    global consoleBox
    # Codigo run aqui
    serialPort = clicked.get()
    frequencyChoosen = freqClicked.get()
   

    consoleBox.insert(END, clicked.get()+'\n')
    consoleBox.pack(side=BOTTOM,pady=0.1)

# Drop Down Box 1
lista = ["Click Refresh"]
clicked = StringVar()
clicked.set("Choose Serial Port")
drop = OptionMenu(root,clicked, *lista,)
drop.config(width=11,pady=0.1)
drop.place(relx=0.01,rely=0.01)

# Drop Down Box 2
frequencyList = ["30-60kHz", "60-90kHz"]
freqClicked = StringVar()
freqClicked.set("Choose Frequency")
dropFrequency = OptionMenu(root,freqClicked,*frequencyList)
dropFrequency.config(width=11,pady=0.1)
dropFrequency.place(relx=0.45,rely=0.01)

# Refresh Serial Port Button
refreshBtn = Button(root, text="Refresh Serial Port", command = getSerialPorts )
refreshBtn.place(relx=0.7)

# Connect to serial Port and run function
connectBtn = Button(root, text="Connect", command=lambda:threading.Thread(target=run).start() )
connectBtn.place(relx=0.28)

# Vertical (y) Scroll Bar
scroll = Scrollbar(root)
scroll.pack(side=RIGHT, fill=Y)

# Console Viewer
consoleBox = Text(root,width=80,height=25,yscrollcommand=scroll.set)
consoleBox.pack(side=BOTTOM,pady=0.1)

root.mainloop()