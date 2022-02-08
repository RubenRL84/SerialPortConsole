from numpy import byte


def main():
    
    number2 = byte("4113")
    number2 = int.from_bytes(b'\xfc\x00', byteorder='big', signed=True) 
    print(type(number2))


if __name__ == "__main__":
    main()