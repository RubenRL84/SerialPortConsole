from numpy import byte


def main():
    
    number2 = byte("4113")
    number2 = int.from_bytes(b'\x00\x1F', byteorder='little') 
    print(number2)


if __name__ == "__main__":
    main()