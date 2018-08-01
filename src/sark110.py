#---------------------------------------------------------
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
#---------------------------------------------------------

import pywinusb.hid as hid
import threading
import struct

#---------------------------------------------------------

rcv = [0xff] * 19
event = threading.Event()

#---------------------------------------------------------
def shortToBytes(n):
    """
    short to buffer array
    :param n:
    :return:
    """
    b = bytearray([0, 0])
    b[0] = n & 0xFF
    n >>= 8
    b[1] = n & 0xFF
    return b

def intToBytes(n):
    """
    int to buffer array
    :param n:
    :return:
    """
    b = bytearray([0, 0, 0, 0])
    b[0] = n & 0xFF
    n >>= 8
    b[1] = n & 0xFF
    n >>= 8
    b[2] = n & 0xFF
    n >>= 8
    b[3] = n & 0xFF
    return b

def rx_handler(data):
    """
    Handler called when a report is received
    :param data:
    :return:
    """
    global rcv
    rcv = data.copy()
    event.set()


def sark_open():
    """
    Opens the device
    :return: handler
    """
    target_vendor_id = 0x0483
    target_product_id = 0x5750
    filter = hid.HidDeviceFilter(vendor_id=target_vendor_id, product_id=target_product_id)
    device = filter.get_devices()[0]
    if not device:
        return
    else:
        device.open()
        device.set_raw_data_handler(rx_handler)
        return device


def sark_close(device):
    """
    Closes the device
    :param device:  handler
    :return:
    """
    device.close()


def sark_measure(device, freq, cal=True, samples=1):
    """
    Takes one measurement sample at the specified frequency
    :param device:  handler
    :param freq:    frequency in hertz; 0 to turn-off the generator
    :param cal:     True to get OSL calibrated data; False to get uncalibrated data
    :param samples: number of samples for averaging
    :return: rs, xs
    """
    report = device.find_output_reports()[0]
    snd = [0x0] * 19
    snd[1] = 2
    b = intToBytes(freq)
    snd[2] = b[0]
    snd[3] = b[1]
    snd[4] = b[2]
    snd[5] = b[3]
    if cal:
        snd[6] = 1
    else:
        snd[6] = 0
    snd[7] = samples
    event.clear()
    report.set_raw_data(snd)
    report.send()
    event.wait()
    if rcv[1] != 79:
        return 'Nan', 'Nan'
    b = bytearray([0, 0, 0, 0])
    b[0] = rcv[2]
    b[1] = rcv[3]
    b[2] = rcv[4]
    b[3] = rcv[5]
    rs = struct.unpack('f', b)
    b[0] = rcv[6]
    b[1] = rcv[7]
    b[2] = rcv[8]
    b[3] = rcv[9]
    xs = struct.unpack('f', b)
    return rs, xs


def sark_buzzer(device, freq=0, duration=0):
    """
    Sounds the sark110 buzzer.
    :param device:      handler
    :param freq:        frequency in hertz
    :param duration:    duration in ms
    :return:
    """
    report = device.find_output_reports()[0]
    snd = [0x0] * 19
    snd[1] = 20
    b = shortToBytes(freq)
    snd[2] = b[0]
    snd[3] = b[1]
    b = shortToBytes(duration)
    snd[4] = b[0]
    snd[5] = b[1]
    event.clear()
    report.set_raw_data(snd)
    report.send()
    event.wait()
    return rcv[1] == 79

def sark_reset(device):
    """
    :param device:      handler
    :return:
    """
    report = device.find_output_reports()[0]
    snd = [0x0] * 19
    snd[1] = 50
    event.clear()
    report.set_raw_data(snd)
    report.send()
    event.wait()
    return rcv[1] == 79

def sark_version(device):
    """
    Sends the sark110 get version command.
    :param device:  handler
    :return:        prot, ver
    """
    report = device.find_output_reports()[0]
    snd = [0x0] * 19
    snd[1] = 1
    event.clear()
    report.set_raw_data(snd)
    report.send()
    event.wait()
    if rcv[1] != 79:
        return 0, ''
    prot = (rcv[3] << 8) & 0xFF00
    prot += rcv[2] & 0xFF
    ver = [0x0] * 15
    ver[:] = rcv[4:]
    return prot, ver


def sark_measure_ext(device, freq, step, cal=True, samples=1):
    """
    Takes four measurement samples starting at the specified frequency and incremented at the specified step
    Uses half float, so a bit less precise
    :param device:  handler
    :param freq:    frequency in hertz; 0 to turn-off the generator
    :param step:    step in hertz
    :param cal:     True to get OSL calibrated data; False to get uncalibrated data
    :param samples: number of samples for averaging
    :return: rs, xs  four vals
    """
    report = device.find_output_reports()[0]
    snd = [0x0] * 19
    snd[1] = 12
    b = intToBytes(freq)
    snd[2] = b[0]
    snd[3] = b[1]
    snd[4] = b[2]
    snd[5] = b[3]
    b = intToBytes(step)
    snd[8] = b[0]
    snd[9] = b[1]
    snd[10] = b[2]
    snd[11] = b[3]
    if cal:
        snd[6] = 1
    else:
        snd[6] = 0
    snd[7] = samples
    event.clear()
    report.set_raw_data(snd)
    report.send()
    event.wait()
    if rcv[1] != 79:
        return 'Nan', 'Nan'
    rs = [0x0] * 4
    xs = [0x0] * 4

    rs[0] = half2Float(rcv[2], rcv[3])
    xs[0] = half2Float(rcv[4], rcv[5])
    rs[1] = half2Float(rcv[6], rcv[7])
    xs[1] = half2Float(rcv[8], rcv[9])
    rs[2] = half2Float(rcv[10], rcv[11])
    xs[2] = half2Float(rcv[12], rcv[13])
    rs[3] = half2Float(rcv[14], rcv[15])
    xs[3] = half2Float(rcv[16], rcv[17])

    return rs, xs

#---------------------------------------------------------
#half float decompress
def half2Float(byte1, byte2):
    hfs = (byte2 << 8) & 0xFF00
    hfs += byte1 & 0xFF
    temp = _half2Float(hfs)
    str = struct.pack('I', temp)
    return struct.unpack('f', str)[0]

def _half2Float(float16):
    s = int((float16 >> 15) & 0x00000001)   # sign
    e = int((float16 >> 10) & 0x0000001f)   # exponent
    f = int(float16 & 0x000003ff)           # fraction

    if e == 0:
        if f == 0:
            return int(s << 31)
        else:
            while not (f & 0x00000400):
                f = f << 1
                e -= 1
            e += 1
            f &= ~0x00000400
        # print(s,e,f)
    elif e == 31:
        if f == 0:
            return int((s << 31) | 0x7f800000)
        else:
            return int((s << 31) | 0x7f800000 | (f << 13))

    e = e + (127 - 15)
    f = f << 13
    return int((s << 31) | (e << 23) | f)

