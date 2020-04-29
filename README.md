# sark110-python
Python class and examples for interfacing with the SARK-110 Antenna Analyzer series.

## About
The Sark110 class in sark110.py provides an interface for communicating with the SARK-110 via USB and basic examples.

## Pre-requisites
- pywinusb for Windows; https://github.com/rene-aguirre/pywinusb
- cython-hidapi for Linux; https://github.com/gbishop/cython-hidapi

Some examples may require additional libraries

## Linux / Raspberry Pi

Install the following packages:
- $ sudo apt-get install python-dev cython libusb-1.0-0-dev libudev-dev libusb-1.0-0-dev
- $ sudo pip install --upgrade setuptools
- $ sudo pip install cython hidapi

First time, copy sark110.rules file to: /etc/udev/rules.d and run:

	sudo udevadm control --reload-rules && udevadm trigger

## Usage tips
Ensure that the analyzer is connected to the computer using the USB cable and configured in Computer Control mode (commands are not processed in the other modes).

Check the examples, e.g. basic_example.py, as a quick guide to use Sark110 class. 

## License
Copyright (c) 2018-2020 Melchor Varela - EA4FRB

Licensed under the MIT License (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at [MIT License](https://opensource.org/licenses/MIT)
	
