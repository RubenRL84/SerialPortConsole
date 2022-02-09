from tkinter import *
import threading
import sys
import serial
import serial.tools.list_ports
import serial as sr
#import numeric

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
    name_serialport = sr.Serial(serialPort,int(selectedPort))  
    if(frequencyChoosen =="30-60kHz" ):
        freq = 1
        d = (1).to_bytes(1,byteorder='big')
        name_serialport.write(d)
    else:
        freq = 2
        d_2 = (2).to_bytes(1,byteorder='big')
        name_serialport.write(d_2)

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



# Refresh Serial Port Button
refreshBtn = Button(root, text="Refresh Serial Port", command = getSerialPorts )
refreshBtn.config(pady=0.1)
refreshBtn.place(relx=0.65,rely=0.005)


# Connect to serial Port and run function
connectBtn = Button(root, text="Connect", command=lambda:threading.Thread(target=run).start() )
connectBtn.config(pady=0.1,width=6)
connectBtn.place(relx=0.85,rely=0.005)


closeBtn = Button(root, text="Close", fg='red', command=lambda:threading.Thread(target=close).start() )
closeBtn.config(pady=0.1,width=6)
closeBtn.place(relx=0.85,rely=0.05)



# Vertical (y) Scroll Bar
scroll = Scrollbar(root)
scroll.pack(side=RIGHT, fill=Y)

# Console Viewer
consoleBox = Text(root,height=30,yscrollcommand=scroll.set)
consoleBox.pack(side=BOTTOM,pady=0.1,fill=X)
#consoleBox.config(padx=0.2,pady=0.2)
#consoleBox.pack(side="bottom",fill=X)




root.mainloop()