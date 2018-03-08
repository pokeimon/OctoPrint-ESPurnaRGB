# OctoPrint-ESPurnaRGB
OctoPrint plugin for controlling ESPurna RGB LED device via REST API using M150 GCODE

        M150: Set Status LED Color - Use R-U-B for R-G-B
        M150 R255       ; Turn LED red
        M150 R255 U127  ; Turn LED orange
        M150            ; Turn LED off
        M150 R U B      ; Turn LED white

[![donate](https://img.shields.io/badge/donate-PayPal-blue.svg)](https://paypal.me/pokeimon/5)

---

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/pokeimon/OctoPrint-ESPurnaRGB/archive/master.zip

## Configuration

You will need to enable REST API for the ESPurna device.

In OctoPrint you will type in the device url such as **http://192.168.123** and the API key in the settings page.

This should work with _almost_ any device flashed with [ESPurna](https://github.com/xoseperez/espurna)

## Tested Devices

I have currently only tested the Magic Home LED Controller flashed with [ESPurna](https://github.com/xoseperez/espurna)