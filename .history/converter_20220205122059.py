from numpy import byte


def main():
    
    number2 = byte("111111111").astype("uint16")
   # number2 = int.from_bytes(b'number2', byteorder='little') 
    print(number2)


if __name__ == "__main__":
    main()