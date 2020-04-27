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
import os
if os.name == 'nt':
    from sark110 import *
elif os.name == 'posix':
    from sark110_hidapi import *
else:
    raise ImportError("Error: no implementation for your platform ('{}') available".format(os.name))

import math
import matplotlib.pyplot as plt
from sys import argv

def z2vswr(r, x):
    gamma = math.sqrt((r - 50) ** 2 + x ** 2) / math.sqrt((r + 50) ** 2 + x ** 2)
    if gamma > 0.980197824:
        return 99.999
    swr = (1 + gamma) / (1 - gamma)
    return swr

if __name__ == '__main__':
    if len(argv) != 4:
        print("please provide arguments in Hz: start stop, step")
        exit(-1)
    start = argv[1]
    print("start: " + start)
    stop = argv[2]
    print("stop: " + stop)
    step = argv[3]
    print("step: " + step)
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

            """
            Alternative implementation using command sampling four freqs (half float)
            
            for freq in range(11000000, 16000000, 4*100000):  # setup loop over number of points
                rs, xs = sark_measure_ext(device, freq, 100000)
                x.append(freq)
                y.append(z2vswr(rs[0], xs[0]))
                x.append(freq+(1*100000))
                y.append(z2vswr(rs[1], xs[1]))
                x.append(freq+(2*100000))
                y.append(z2vswr(rs[2], xs[2]))
                x.append(freq+(3*100000))
                y.append(z2vswr(rs[3], xs[3]))
            """

            plt.plot(x, y)
            plt.title('SARK-110 Test')
            plt.xlabel('Freq MHz')
            plt.ylabel('SWR')
            plt.ylim(1., 10.)
            plt.show()

            print("done")
    finally:
        sark_close(device)
    exit(1)