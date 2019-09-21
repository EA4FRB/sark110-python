# sark110-python
Python library and examples for the SARK-110 Antenna Analyzer series.

## About
This library includes the Python interface library for communicating with the SARK-110 via USB and includes basic examples.

## Pre-requisites
There are two variants:
- sark110.py uses pywinusb (only for Windows) https://github.com/rene-aguirre/pywinusb 
- sark110_hidapi.py uses cython-hidapi(multiplatform) https://github.com/gbishop/cython-hidapi

Some examples may require additional libraries

## Linux / Raspberry Pi
Use sark110_hidapi.py variant.

Install the following packages:
	$ sudo apt-get install python-dev cython libusb-1.0-0-dev libudev-dev libusb-1.0-0-dev
	$ sudo pip install --upgrade setuptools
	$ sudo pip install cython hidapi

First time, copy sark110.rules file to: /etc/udev/rules.d and run:

	sudo udevadm control --reload-rules && udevadm trigger

## License
Copyright (c) 2018-2019 Melchor Varela - EA4FRB

Licensed under the MIT License (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at [MIT License](https://opensource.org/licenses/MIT)
	
