from numpy import byte


def main():
    
    number2 = int("1000000010000",2)
    if (number2 > byte(4096)):
        number2 = ~byte(number2)
        number2 += byte(number2+1)
        number2 = byte(number2 >> 1)


        
   # number2 = int.from_bytes(b'number2', byteorder='little') 

    print(number2)


if __name__ == "__main__":
    main()