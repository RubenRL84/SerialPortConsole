from numpy import byte


def main():
    number = -17
    number2 = byte(number ).astype('uint16')
    print(type(number2))




if __name__ == "__main__":
    main()