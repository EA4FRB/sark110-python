# ---------------------------------------------------------
"""
  This file is a part of the "SARK110 Antenna Vector Impedance Analyzer" software

  MIT License

  @author Copyright (c) 2020 Melchor Varela - EA4FRB

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
import math
import matplotlib.pyplot as plt
from sys import argv


def z2vswr(r, x):
    gamma = math.sqrt((r - 50) ** 2 + x ** 2) / math.sqrt((r + 50) ** 2 + x ** 2)
    if gamma > 0.980197824:
        return 99.999
    swr = (1 + gamma) / (1 - gamma)
    return swr


def z2mag(r, x):
    return (math.sqrt(r ** 2 + x ** 2))


def z2gamma(rs, xs, z0=50 + 0j):
    z = complex(rs, xs)
    return (z - z0) / (z + z0)


if __name__ == '__main__':
	if len(argv) != 4:
		print("please provide arguments in Hz: start stop, step")
		exit(-1)

	fr_start = argv[1]
	print("start: " + fr_start)
	fr_stop = argv[2]
	print("stop: " + fr_stop)
	fr_step = argv[3]
	print("step: " + fr_step)

	device = Sark110()
	device.open()
	device.connect()
	if not device.is_connected:
		print("Device not connected")
		exit(-2)
	else:
		print("Device connected")

	print(device.fw_protocol, device.fw_version)
	device.buzzer(1000, 800)

	plt.style.use('seaborn-whitegrid')
	y = []
	x = []
	rs = [0]
	xs = [0]
	for freq in range(int(fr_start), int(fr_stop), int(fr_step)):
		device.measure(freq, rs, xs)
		x.append(freq)
		y.append(z2vswr(rs[0][0], xs[0][0]))

	plt.plot(x, y)
	plt.title('SARK-110 Test')
	plt.xlabel('Freq MHz')
	plt.ylabel('SWR')
	plt.ylim(1., 10.)
	plt.show()

	print("done")
	device.close()
	exit(1)
