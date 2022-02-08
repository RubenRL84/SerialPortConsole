import math
def main():
    my_file = open("odometria_first.txt", "r")
    content = my_file.read()
    content_list = content.split("\n")
    my_file.close()
    #print(content_list)

    my_file2 = open("logteste_first_clean.txt", "r")
    content2 = " "+my_file2.read()
    content_list2 = content2.split("\n")
    my_file2.close()
   # print(content_list2)
    list3 = [i + j for i, j in zip(content_list, content_list2)]
    textfile = open("a_file.txt", "w")
    for index,value in enumerate(list3):
        textfile.write(value + "\n")
    textfile.close()

def second():
    logFile = open("log_Vitor_Rui_clean.txt","r")

    fileData = logFile.readlines()
    dataArray = []
    print(len(fileData))
    for i in fileData:
        dataArray.append(float(i.split()[0]))
    logFile.close()

    dataToAdd2 =open("log_Vitor_Rui_clean.txt","r")
    content2 = " "+dataToAdd2.read()
    content_list2 = content2.split("\n")

    attemptFile = open("first_attempt.txt","r")
    fileData2 = attemptFile.readlines()
    attemptArray = []
    attempFullInfo = []
    for i in fileData2:
       if not i.strip():
           continue
       if i:
            attemptArray.append(float(i.split()[0]))
            attempFullInfo.append(i.strip("\n"))

    theRealData = []

    ValueBigger = 9999999999.9999

    for i in dataArray:
        index = 0
        
        for x in attemptArray:
            a = float(i) - float(x)
            if( a < ValueBigger and a > 00.00):
                ValueBigger = a
               # print(ValueBigger) 
                number = index
            index +=1

        theRealData.append(str(attempFullInfo[number]))

    list3 = [i + j for i, j in zip( theRealData,content_list2)]
    textfile = open("a_file.txt", "w")
    for index,value in enumerate(list3):
        textfile.write(value)
    textfile.close()

    print(len(list3))


if __name__ == "__main__":
    second()