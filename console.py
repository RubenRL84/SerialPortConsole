from ast import Not
from hashlib import new
from tkinter import *
import threading
import sys
import serial
import serial.tools.list_ports
import serial as sr
import numpy as np
import matplotlib.pyplot as plt
import pygame
from time import sleep
from scipy.fft import fft, fftfreq
from scipy.signal import find_peaks
from numpy import cos, sin, pi, absolute, arange
from scipy.signal import kaiserord, lfilter, firwin, freqz
from pylab import figure, clf, plot, xlabel, ylabel, xlim, ylim, title, grid, axes, show
from numpy import convolve as np_convolve
from scipy import signal

global count
global live_numbers


def play():
    pygame.init()
    pygame.mixer.music.load("ping.wav")
    pygame.mixer.music.play(loops = 0)

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

    graph_numbers = np.array([])
    file.close()
    name_serialport.close()
    consoleBox.insert(END, "Connection Closed" +'\n')
    consoleBox.pack(side=BOTTOM,pady=0.1)

def start():
    global file
    global serialPort
    global name_serialport
    global selectedPort
    selectedPort = portClicked.get()
    frequencyChoosen = freqClicked.get()
    serialPort = clicked.get()

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
        return name_serialport 
    except ValueError:
        print(ValueError+ "Missing selecting something")

       

## Connect to selected port and frquency and show output on Text Window
def run():
    global consoleBox
    global graph_numbers
    global new_name_serialport
    global new_graph
    #count = 0
    first_list = False
    graph_numbers = np.array([])
    live_numbers = np.array([])
    new_graph = np.array([])
    new_name_serialport = start()

    global first_number
    global second_number

    first_number = 0
    second_number = 1

    while(True):
        if(len(graph_numbers) == 4096):
            new_name_serialport.close()
            new_name_serialport = sr.Serial(serialPort,int(selectedPort))
            graph_numbers = np.array([])
            live_numbers = np.array([])
            new_graph = np.array([])
            first_list = not first_list

        ADC_temp = new_name_serialport.read(2)
        ADC_temp = list(ADC_temp)
   
        # if((ADC_temp[0] >= ADC_temp[1]) and first_list == False):
        #     first_number = 0
        #     second_number = 1
        #     first_list = True
        # elif((ADC_temp[0] <= ADC_temp[1]) and first_list == False):
        #     first_number = 1
        #     second_number = 0
        #     first_list = True
        ADC = new_ADC_numbers(ADC_temp,first_number,second_number)
        if(ADC > 4095): 
            first_number = 1
            second_number = 0
            ADC = new_ADC_numbers(ADC_temp,first_number,second_number)
        elif(ADC <= 4095) and first_list == False:
            first_number = 0
            second_number = 1
            first_list = True
        
        graph_numbers = np.append(graph_numbers,ADC)
        live_numbers = np.append(live_numbers,ADC)
        new_graph = np.append(new_graph,ADC)
        if (live_numbers.size == 1024):

                        #Filtro FIR passa baixa
            #------------------------------------------------
            # Create a FIR filter and apply it to x.
            #------------------------------------------------
            #taps = np.array([-0.0071865,-0.019077,-0.0074447,0.0089641,-0.0028051,-0.0027272,0.0048902,-0.0039446,0.0013541,0.0013399,-0.0030411,0.0033026,-0.0022575,0.00044031,0.0014321,-0.0027164,0.0029824,-0.0021776,0.00057958,0.0012581,-0.0027057,0.0032394,-0.0026329,0.0010425,0.0010274,-0.0028611,0.0037785,-0.003383,0.0017262,0.00068386,-0.0030355,0.0044666,-0.0043844,0.0026915,0.00012838,-0.0031431,0.0052648,-0.0056413,0.0039911,-0.00073871,-0.0030758,0.0061169,-0.007197,0.0057389,-0.0020447,-0.0027422,0.0069819,-0.0090855,0.0080752,-0.0040037,-0.0019582,0.0078273,-0.01145,0.011273,-0.0069349,-0.00046311,0.0085931,-0.014561,0.015912,-0.011549,0.0022754,0.0092402,-0.019123,0.023464,-0.019713,0.0077424,0.0097362,-0.02752,0.039161,-0.03863,0.022286,0.010049,-0.054384,0.10337,-0.14779,0.17875,0.81014,0.17875,-0.14779,0.10337,-0.054384,0.010049,0.022286,-0.03863,0.039161,-0.02752,0.0097362,0.0077424,-0.019713,0.023464,-0.019123,0.0092402,0.0022754,-0.011549,0.015912,-0.014561,0.0085931,-0.00046311,-0.0069349,0.011273,-0.01145,0.0078273,-0.0019582,-0.0040037,0.0080752,-0.0090855,0.0069819,-0.0027422,-0.0020447,0.0057389,-0.007197,0.0061169,-0.0030758,-0.00073871,0.0039911,-0.0056413,0.0052648,-0.0031431,0.00012838,0.0026915,-0.0043844,0.0044666,-0.0030355,0.00068386,0.0017262,-0.003383,0.0037785,-0.0028611,0.0010274,0.0010425,-0.0026329,0.0032394,-0.0027057,0.0012581,0.00057958,-0.0021776,0.0029824,-0.0027164,0.0014321,0.00044031,-0.0022575,0.0033026,-0.0030411,0.0013399,0.0013541,-0.0039446,0.0048902,-0.0027272,-0.0028051,0.0089641,-0.0074447,-0.019077,-0.0071865])

            # Use firwin with a Kaiser window to create a lowpass FIR filter.
            #taps = firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))

            # Use lfilter to filter x with the FIR filter.
            #filtered_x = lfilter(taps, 1.0, live_numbers)

            N = live_numbers
            Frequency_Sampling = frequencyText.get(1.0,END)
            T = int(Frequency_Sampling)/2 # Frequency sample
            x = T * np.linspace(-1,1, N.size, endpoint=False)
            y = abs(fft(N))
            y = np.delete(y,0)
            x = np.delete(x,0)
            #print(y)
            for index, item in enumerate(x):
                #print(item)
                if(item > 72000.0 and item < 73500):
                    #print(y[index])
                    if(y[index] > 60000.0):
                        play()
                        #print(y[index])
            live_numbers = np.delete(live_numbers,np.s_[0::1024])
            
            #count += 1
            #threading.Thread(target=beep(live_numbers)).start()
            #live_numbers = np.array([])
        file.write(str(ADC)+'\n')
        consoleBox.insert(END,str(ADC)+'\n')
        consoleBox.pack(side=BOTTOM,pady=0.1)
            

    
        
        

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
portlist = ["4800","9600","19200","57600","115200","230400","576000","905000"]
portClicked = StringVar()
portClicked.set("Choose Baud Rate")
portFrequency = OptionMenu(root,portClicked,*portlist)
portFrequency.config(width=12,pady=0.1)
portFrequency.place(relx=0.26,rely=0.01)

def clearConsole():
    #graph_numbers = np.array([])
    #live_numbers = np.array([])
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

# Frequency Label
frequencyLabel =Label(root, text="Frequency sample: ")
frequencyLabel.config(width=16,pady=0.1)
frequencyLabel.place(relx=0.01,rely=0.063)

frequencyText = Text(root,width=8,height=1.4)
frequencyText.place(relx=0.185,rely=0.065)

# Graphic Section
def graph():

    #Filtro FIR passa baixa
    #------------------------------------------------
    # Create a FIR filter and apply it to x.
    #------------------------------------------------
    #taps = np.array([2.9368e-07,-1.3226e-21,3.8254e-07,-1.428e-06,2.5242e-06,-2.6511e-06,9.1298e-07,2.8116e-06,-7.4522e-06,1.088e-05,-1.069e-05,5.392e-06,4.4853e-06,-1.6001e-05,2.449e-05,-2.5276e-05,1.5846e-05,2.4707e-06,-2.4182e-05,4.1125e-05,-4.5446e-05,3.3007e-05,-5.7927e-06,-2.7904e-05,5.5943e-05,-6.6766e-05,5.4162e-05,-2.04e-05,-2.3793e-05,6.2719e-05,-8.1533e-05,7.2184e-05,-3.6988e-05,-1.1794e-05,5.6455e-05,-8.0727e-05,7.626e-05,-4.5948e-05,2.5891e-06,3.6638e-05,-5.7526e-05,5.4784e-05,-3.386e-05,7.7461e-06,9.7975e-06,-1.1391e-05,-8.8976e-18,1.2493e-05,-1.1786e-05,-1.0221e-05,4.9011e-05,-8.6996e-05,0.00010023,-7.006e-05,-5.4346e-06,0.00010589,-0.00019302,0.00022447,-0.00017251,3.9619e-05,0.00013666,-0.00029346,0.00036491,-0.00030918,0.00012927,0.00012223,-0.00035811,0.00048749,-0.00045145,0.00024908,5.7248e-05,-0.0003615,0.00055219,-0.00055499,0.00036289,-4.1285e-05,-0.00029526,0.00052597,-0.00057007,0.00041744,-0.0001314,-0.00017776,0.00039752,-0.0004576,0.00035549,-0.00015261,-5.6589e-05,0.0001884,-0.00020659,0.0001353,-4.2208e-05,1.0267e-19,-4.4921e-05,0.00015326,-0.00024905,0.00024173,-7.7282e-05,-0.00022184,0.00055006,-0.00075372,0.00069704,-0.00033184,-0.00026117,0.0008835,-0.0012849,0.0012626,-0.0007549,-0.00011244,0.001053,-0.001716,0.0018195,-0.0012696,0.00021433,0.00099425,-0.0019217,0.0022133,-0.0017345,0.00063169,0.000713,-0.0018205,0.0022942,-0.0019705,0.00098034,0.0003037,-0.0014135,0.0019664,-0.0018085,0.0010615,-5.8304e-05,-0.0008047,0.001233,-0.0011466,0.00069232,-0.00015481,-0.00019149,0.00021783,8.3284e-17,-0.00022906,0.00021173,0.00017999,-0.00084645,0.0014741,-0.0016671,0.0011443,8.7196e-05,-0.0016698,0.0029924,-0.0034228,0.0025883,-0.00058512,-0.0019875,0.0042041,-0.0051517,0.0043031,-0.0017743,-0.0016551,0.004786,-0.0064325,0.0058835,-0.0032073,-0.00072862,0.0045494,-0.0068739,0.0068364,-0.004425,0.00049853,0.0035321,-0.006236,0.0067011,-0.004867,0.0015201,0.0020415,-0.0045339,0.0051854,-0.0040041,0.0017093,0.00063059,-0.0020896,0.0022819,-0.001489,0.00046305,0,0.00049052,-0.001671,0.002713,-0.0026325,0.00084193,0.0024192,-0.0060089,0.008254,-0.0076577,0.0036603,0.0028948,-0.0098489,0.014419,-0.014278,0.0086116,0.0012954,-0.012266,0.020236,-0.021753,0.015411,-0.0026456,-0.012502,0.024661,-0.029049,0.023333,-0.0087319,-0.010155,0.026799,-0.035026,0.031322,-0.016296,-0.005306,0.02611,-0.038673,0.03818,-0.024298,0.001465,0.022547,-0.039325,0.042811,-0.031522,0.0091677,0.016591,-0.036815,0.044447,-0.036815,0.016591,0.0091677,-0.031522,0.042811,-0.039325,0.022547,0.001465,-0.024298,0.03818,-0.038673,0.02611,-0.005306,-0.016296,0.031322,-0.035026,0.026799,-0.010155,-0.0087319,0.023333,-0.029049,0.024661,-0.012502,-0.0026456,0.015411,-0.021753,0.020236,-0.012266,0.0012954,0.0086116,-0.014278,0.014419,-0.0098489,0.0028948,0.0036603,-0.0076577,0.008254,-0.0060089,0.0024192,0.00084193,-0.0026325,0.002713,-0.001671,0.00049052,0,0.00046305,-0.001489,0.0022819,-0.0020896,0.00063059,0.0017093,-0.0040041,0.0051854,-0.0045339,0.0020415,0.0015201,-0.004867,0.0067011,-0.006236,0.0035321,0.00049853,-0.004425,0.0068364,-0.0068739,0.0045494,-0.00072862,-0.0032073,0.0058835,-0.0064325,0.004786,-0.0016551,-0.0017743,0.0043031,-0.0051517,0.0042041,-0.0019875,-0.00058512,0.0025883,-0.0034228,0.0029924,-0.0016698,8.7196e-05,0.0011443,-0.0016671,0.0014741,-0.00084645,0.00017999,0.00021173,-0.00022906,8.3284e-17,0.00021783,-0.00019149,-0.00015481,0.00069232,-0.0011466,0.001233,-0.0008047,-5.8304e-05,0.0010615,-0.0018085,0.0019664,-0.0014135,0.0003037,0.00098034,-0.0019705,0.0022942,-0.0018205,0.000713,0.00063169,-0.0017345,0.0022133,-0.0019217,0.00099425,0.00021433,-0.0012696,0.0018195,-0.001716,0.001053,-0.00011244,-0.0007549,0.0012626,-0.0012849,0.0008835,-0.00026117,-0.00033184,0.00069704,-0.00075372,0.00055006,-0.00022184,-7.7282e-05,0.00024173,-0.00024905,0.00015326,-4.4921e-05,1.0267e-19,-4.2208e-05,0.0001353,-0.00020659,0.0001884,-5.6589e-05,-0.00015261,0.00035549,-0.0004576,0.00039752,-0.00017776,-0.0001314,0.00041744,-0.00057007,0.00052597,-0.00029526,-4.1285e-05,0.00036289,-0.00055499,0.00055219,-0.0003615,5.7248e-05,0.00024908,-0.00045145,0.00048749,-0.00035811,0.00012223,0.00012927,-0.00030918,0.00036491,-0.00029346,0.00013666,3.9619e-05,-0.00017251,0.00022447,-0.00019302,0.00010589,-5.4346e-06,-7.006e-05,0.00010023,-8.6996e-05,4.9011e-05,-1.0221e-05,-1.1786e-05,1.2493e-05,-8.8976e-18,-1.1391e-05,9.7975e-06,7.7461e-06,-3.386e-05,5.4784e-05,-5.7526e-05,3.6638e-05,2.5891e-06,-4.5948e-05,7.626e-05,-8.0727e-05,5.6455e-05,-1.1794e-05,-3.6988e-05,7.2184e-05,-8.1533e-05,6.2719e-05,-2.3793e-05,-2.04e-05,5.4162e-05,-6.6766e-05,5.5943e-05,-2.7904e-05,-5.7927e-06,3.3007e-05,-4.5446e-05,4.1125e-05,-2.4182e-05,2.4707e-06,1.5846e-05,-2.5276e-05,2.449e-05,-1.6001e-05,4.4853e-06,5.392e-06,-1.069e-05,1.088e-05,-7.4522e-06,2.8116e-06,9.1298e-07,-2.6511e-06,2.5242e-06,-1.428e-06,3.8254e-07,-1.3226e-21,2.9368e-07])
    #f = 74000
   # numtaps = 200
    # Use firwin with a Kaiser window to create a lowpass FIR filter.
    #taps = firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
    #taps = signal.firwin(numtaps, f)
    # Use lfilter to filter x with the FIR filter.
    #filtered_x = lfilter(taps, 1.0, graph_numbers)

    #filtered_x = np.array([np_convolve(xi, taps, mode='valid') for xi in graph_numbers])

    Frequency_Sampling = frequencyText.get(1.0,END)
    #N = filtered_x # Samples
    N = new_graph
    T = int(Frequency_Sampling)/2 # Frequency sample

    yf = abs(fft(N))
    yf = np.delete(yf,0)
    #x = np.delete(x,0)

    x = T * np.linspace(-1,1, yf.size, endpoint=False)
   
    
    
    
    #del yf[0]
    #del x[0]

    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True
    np.random.seed(0)


    #s  = graph_numbers
    #t = np.arange(0, s.size, dt)
    fig, axs = plt.subplots()
    axs.set_title("Signal")
    axs.plot(x, yf, color='C0')
    axs.set_xlabel("Frequencia")
    axs.set_ylabel("Amplitude")
    #axs.ticklabel_format(axis='y', scilimits=[0, 8])
    axs.ticklabel_format(axis='x', scilimits=[0, 5])
    #plt.switch_backend('agg')
    #plt.show()
    plt.savefig("Teste")
    plt.clf()

# Graphic Button
graphBtn = Button(root, text="Create Graphic", command=graph)
graphBtn.config(width=12,pady=0.1)
graphBtn.place(relx=0.46,rely=0.06)

getSerialPorts()


def beep(graph_numbers):

    
    N = graph_numbers
    Frequency_Sampling = frequencyText.get(1.0,END)
    T = int(Frequency_Sampling)/2 # Frequency sample
    x = T * np.linspace(-1,1, N.size, endpoint=False)
    y = fft(N)

    for index, item in enumerate(x):
        if(item > 72000 and item < 74000):
            if(y[index] > 70000):
                play()
                
                #live_numbers = np.empty()
                #print(count)
    


    
# Starts UI
root.mainloop()