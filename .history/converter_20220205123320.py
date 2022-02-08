from numpy import byte


def main():
    
    number2 = int("111111111111",2)
    number2 += 17
    if (number2 >> 4096):
        number2 = int.to_bytes(number2)
        #number2 += 1
   # number2 = int.from_bytes(b'number2', byteorder='little') 

    print(number2)


if __name__ == "__main__":
    main()