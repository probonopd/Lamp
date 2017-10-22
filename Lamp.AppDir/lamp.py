#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket

def remap(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class Lamp:

    def __init__(self, host, port=8899):
        self.host = host
        self.port = port
        self.command = ""

    def __str__(self):
        return "Lamp %s" % self.host

    def set_value(self, name, value, in_min, in_max, out_min, out_max, checksum_add):
        remapped_value = int(round(remap(value, in_min, in_max, out_min, out_max), 0))
        remapped_value_hex = format(remapped_value, 'x')
        remapped_value_checksum = format(remapped_value + checksum_add, 'x')
        print("Setting %s to %i" % (name, remapped_value))
        if(name == "brightness"):
            command = "0833"
        elif(name == "temperature"):
            command = "0836"
        else:
            command = "0000"
        command_hex = "0x5500000002ff%s%s%saaaa" % (command, remapped_value_hex, remapped_value_checksum)
        # For whatever reason, bytes.fromhex fails if a hex number has no alphanumeric characters and no leading 0
        if(remapped_value < 16):
            remapped_value_hex = '0' + remapped_value_hex
        data = bytes.fromhex('5500000002ff') + bytes.fromhex(command) + bytes.fromhex(remapped_value_hex) + bytes.fromhex(remapped_value_checksum) + bytes.fromhex('aaaa')
        print([hex(i) for i in data])
        self.send(data);

    def send(self, command):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        s.send(command)
        s.close()

    def set_brightness(self, brightness):
        self.set_value("brightness", brightness, 0, 100, 0, 64, 60)

    def set_temperature(self, temperature):
        self.set_value("temperature", temperature, 0, 100, 0, 32, 63)

def main():
    l = Lamp("192.168.0.15")
    l.set_brightness(36)
    l.set_temperature(20)

if __name__ == "__main__":
    main()
