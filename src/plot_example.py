# ---------------------------------------------------------
"""
  This file is a part of the "SARK110 Antenna Vector Impedance Analyzer" software

  MIT License

  @author Copyright (c) 2018 Melchor Varela - EA4FRB

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
"""
# ---------------------------------------------------------
from sark110 import *
#import numpy as np
import math
import matplotlib.pyplot as plt

def z2vswr(r, x):
    gamma = math.sqrt((r - 50) ** 2 + x ** 2) / math.sqrt((r + 50) ** 2 + x ** 2)
    if gamma > 0.980197824:
        return 99.999
    swr = (1 + gamma) / (1 - gamma)
    return swr

if __name__ == '__main__':
    try:
        device = sark_open()
        if not device:
            print("device not connected")
        else:
            print("device connected")
            prot, ver = sark_version(device)
            print(prot, ver)
            sark_buzzer(device, 1000, 800)

            plt.style.use('seaborn-whitegrid')
            y = []
            x = []
            for freq in range(11000000, 16000000, 100000):  # setup loop over number of points
                rs, xs = sark_measure(device, freq)
                x.append(freq)
                y.append(z2vswr(rs[0], xs[0]))

            plt.plot(x, y)
            plt.title('SARK-110 Test')
            plt.xlabel('Freq MHz')
            plt.ylabel('SWR')
            plt.ylim(1., 10.)
            plt.show()

            print("done")
    finally:
        sark_close(device)
