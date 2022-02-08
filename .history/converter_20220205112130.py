from numpy import byte


def main():
    number = -17
    number2 = byte(number & 0xFFF)
    print(type(number2))




if __name__ == "__main__":
    main()