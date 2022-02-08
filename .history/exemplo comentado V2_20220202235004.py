
def main():

    dataArray = []
    logFile = open("Lidar_BrunoFrancisco2","r")
    fileData = logFile.readlines() # cria lista A com dados do ficheiro
    
    for i in fileData:
        dataArray.append(float(i.split()[0])) # guarda primeiro valor do ficheiro no array
    logFile.close()

    dataToAdd2 =open("Lidar_BrunoFrancisco2","r")
    for i in dataToAdd2:
        content2 = dataToAdd2.read()
    content_list2 = content2.split("\n") # cria lista B com dados do ficheiro para usar para futuramente criar ficheiro final

    attemptFile = open("odo2.txt","r")
    fileData2 = attemptFile.readlines()
    attemptArray = []
    attempFullInfo = []

    for i in fileData2:
       if not i.strip(): 
           continue # como ficheiro tem linhas em branco, nesses casos vai ignorar essas linhas
       if i:
            attemptArray.append(float(i.split()[0])) # guarda primeiro valor do ficheiro no array
            attempFullInfo.append(i.strip("\n")) # cria segunda lista com todos os dados do ficheiro

    theRealData = []

    for i in dataArray:
        index = 0
        ValueBigger = float(i) # numero para comparacao
        for x in attemptArray:
            a = float(i) - float(x) # lista C - lista D com intenção de ter o numero mais perto de zero
            if( a < ValueBigger and a > 00.00): # compara o Valor da variavel a, caso seja menos que nr de comparação mas positivo
                ValueBigger = a # substitui para valor mais baixo
                number = index # guarda o indice da lista C
            index +=1
# usa o indice guardado, para ir buscar a lista B e adiciona a info pretendida do valor que está no mesmo indice da lista A
        theRealData.append(str(attempFullInfo[number]+" ")) 

# faz concatenação de 2 listas numa so, para criar o ficheiro final
    list3 = [i + j for i, j in zip( theRealData,content_list2)] 
    textfile = open("a_file.txt", "w")
    for index,value in enumerate(list3):
        textfile.write(value + "\n")
    textfile.close()
    


if __name__ == "__main__":
    main()