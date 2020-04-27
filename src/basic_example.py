#---------------------------------------------------------
"""
  This file is a part of the "SARK110 Antenna Vector Impedance Analyzer" software
 
  MIT License
 
  @author Copyright (c) 2018-2019 Melchor Varela - EA4FRB
 
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
#---------------------------------------------------------
import os
if os.name == 'nt':
    from sark110 import *
elif os.name == 'posix':
    from sark110_hidapi import *
else:
    raise ImportError("Error: no implementation for your platform ('{}') available".format(os.name))
	
from sys import argv

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
            for freq in range(int(start), int(stop), int(step)):  # setup loop over number of points
                rs, xs = sark_measure(device, freq)
                print(rs, xs)
            print("done")
    finally:
        sark_close(device)
    exit(1)