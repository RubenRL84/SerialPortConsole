from numpy import byte
%matplotlib inline
import matplotlib.pyplot as plt

import numpy as np

def main():
    
    number2 = int("1000000010000",2)
    if (number2 > byte(4096)):
        number2 = ~byte(number2)
        number2 += byte(number2+1)
        number2 = byte(number2 >> 1)

fig = plt.figure()
ax = plt.axes()

x = np.linspace(0, 10, 1000)
ax.plot(2, -2);

if __name__ == "__main__":
    main()