#!/usr/bin/env python3

from sark110 import *
from skrf import Network

def z2gamma(rs, xs):
    z = complex(rs, xs)
    z0 = 50 + 0j
    return (z - z0) / (z + z0)

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

            y = []
            x = []
            for freq in range(11000000, 16000000, 100000):  # setup loop over number of points
                rs, xs = sark_measure(device, freq)
                x.append(freq)
                y.append(z2gamma(rs[0], xs[0]))

            ring_slot = Network(frequency=x, s=y, z0=50)
            ring_slot.plot_s_smith()

            print("done")
   finally:
        sark_close(device)
