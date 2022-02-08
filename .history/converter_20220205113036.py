from numpy import byte


def main():
    
    number2 = byte("4113").astype("uint8")
    print(type(number2))


if __name__ == "__main__":
    main()