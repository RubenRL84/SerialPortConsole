from tkinter import *
import threading
import sys
import serial
import serial.tools.list_ports
import serial as sr
import numpy as np
import matplotlib.pyplot as plt
from time import sleep

# UI Builder
root = Tk()
root.title("Acoustic Pinger Locator")
root.geometry("780x500")
root.minsize("780","500")

# Frame for Text Window
frame = Frame(root)
frame.config(padx=0.1)
frame.pack(side=BOTTOM,fill=X)

def new_ADC_numbers (list_array,first_number,second_number):# função para tratar novos valores lidos
    number_low = list_array[first_number] # guarda os valores de menos significativos da leitura
    number_high = list_array[second_number] # guarda os valores de mais significativos da leitura
    number = ((number_high << 8) | number_low)   # concatena os valores numa só variavel 
    return number

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

# Close connection of serial port
def close():

    file.close()
    name_serialport.close()
    consoleBox.insert(END, "Connection Closed" +'\n')
    consoleBox.pack(side=BOTTOM,pady=0.1)

## Connect to selected port and frquency and show output on Text Window
def run():
    global consoleBox
    global serialPort
    global name_serialport
    global graph_numbers
    global file
    first_list = False
    graph_numbers = np.array([])
    serialPort = clicked.get()
    selectedPort = portClicked.get()
    frequencyChoosen = freqClicked.get()
    file = open("Log.txt", "w+")

    try:
        name_serialport = sr.Serial(serialPort,int(selectedPort))
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
        name_serialport = sr.Serial(serialPort,int(selectedPort))
        consoleBox.insert("1.0", serialPort+ ' porta: '+ freqClicked.get()+'\n')
        consoleBox.pack(side=BOTTOM,pady=0.1)
        
        while(True):
            ADC_temp = name_serialport.read(2)
            ADC_temp = list(ADC_temp)
            if((ADC_temp[0] >= ADC_temp[1]) and first_list == False):
                first_number = 0
                second_number = 1
                first_list = True
            elif((ADC_temp[0] < ADC_temp[1]) and first_list == False):
                first_number = 1
                second_number = 0
                first_list = True

            ADC = new_ADC_numbers(ADC_temp,first_number,second_number)
            graph_numbers = np.append(graph_numbers,ADC)
            file.write(str(ADC)+'\n')
            consoleBox.insert(END,str(ADC)+'\n')
            consoleBox.pack(side=BOTTOM,pady=0.1)
            

    except ValueError:
        print(ValueError+ "Missing selecting something")
        
        

# Drop Down Box of Serial Ports
lista = ["Click Refresh"]
clicked = StringVar()
clicked.set("Choose Serial Port")
drop = OptionMenu(root,clicked, *lista)
drop.config(width=16,pady=0.1)
drop.place(relx=0.01,rely=0.01)

# Drop Down Box of Frequencys
frequencyList = ["30-60kHz", "60-90kHz"]
freqClicked = StringVar()
freqClicked.set("Choose Frequency")
dropFrequency = OptionMenu(root,freqClicked,*frequencyList)
dropFrequency.config(width=11,pady=0.1)
dropFrequency.place(relx=0.46,rely=0.01)

# Drop Down Box of Baud Rate
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
refreshBtn.config(pady=0.1,width=13)
refreshBtn.place(relx=0.65,rely=0.005)

# Clear Console Button
refreshBtn = Button(root, text="Clear Console", command = clearConsole)
refreshBtn.config(pady=0.1,width=13)
refreshBtn.place(relx=0.65,rely=0.06)

# Connect to serial Port and run function
connectBtn = Button(root, text="Connect", command=lambda:threading.Thread(target=run).start() )
connectBtn.config(pady=0.1,width=6)
connectBtn.place(relx=0.88,rely=0.005)

# Close Button
closeBtn = Button(root, text="Close", fg='red', command=lambda:threading.Thread(target=close).start() )
closeBtn.config(pady=0.1,width=6)
closeBtn.place(relx=0.88,rely=0.06)

# Vertical (y) Scroll Bar
scroll = Scrollbar(frame)
scroll.pack(side=RIGHT, fill=Y)

# Console Label
consoleLabel =Label(frame,bg="white",fg="black", text="Console")
consoleLabel.pack(fill=X)

# Console Viewer
consoleBox = Text(frame,height=30,yscrollcommand=scroll.set)
consoleBox.pack(pady=0.2,fill=X)

# Graphic Section
def graph():
    #close()
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True
    np.random.seed(0)

    dt = 512 # sampling interval
    Fs = 1 / dt # sampling frequency
    s  = graph_numbers
    t = np.arange(0, s.size, dt)
    fig, axs = plt.subplots()
    axs.set_title("Signal")
    axs.plot(t, s, color='C0')
    axs.set_xlabel("Time")
    axs.set_ylabel("Amplitude")
    #plt.switch_backend('agg')
    #plt.show()
    plt.savefig("Teste")
    plt.clf()

# Graphic Button
graphBtn = Button(root, text="Create Graphic", command=graph)
graphBtn.config(width=12,pady=0.1)
graphBtn.place(relx=0.46,rely=0.06)

getSerialPorts()


# Starts UI
root.mainloop()