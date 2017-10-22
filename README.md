# Lamp

Control Lead Energy Flexible White LED panel. Set brightness and color temperature.

## Compatible hardware

Tested with Lead Energy LED PANEL PDW. Seems to be built by OEM Sunricher. Sunricher has even put the app into the Play Store: https://play.google.com/store/apps/details?id=com.sunricher.leadenergy

## Usage

Simply use the GUI:

![screenshot](https://user-images.githubusercontent.com/2480569/31863842-a7980c74-b753-11e7-8fbf-abdff9407dd5.png)

Or use the Python API.

## Protocol


```
Packet: 0x5500000002ffXXXXYYZZaaaa

XXXX = Command
YY = Value
ZZ = Checksum

On/off:
XXXX = 0x0212
YY = On: 0xab  Off: 0xa9
ZZ = Checksum = YY + 0x15

Brightness:
XXXX = 0x0833 
YY = Brightness from entirely dark to bright in 64 steps (0x00..0x40)
ZZ = Checksum = YY + 0x3c

Color temperature:
XXXX = 0x0836 
YY = Color temperatore from cold to warm in 32 steps (0x00..0x20)
ZZ = Checksum = YY + 0x3f
```

Source: https://forum.fhem.de/index.php/topic,18958.msg381964.html#msg381964 (corrected version here)

We can send commands with `nc` like this:

```
echo -e '\x55\x00\x00\x00\x02\xff\x02\x12\xab\xC0\xaa\xaa' | nc 192.168.0.15 8899 # On
echo -e '\x55\x00\x00\x00\x02\xff\x02\x12\xa9\xBE\xaa\xaa' | nc 192.168.0.15 8899 # Off

echo -e '\x55\x00\x00\x00\x02\xff\x08\x33\x00\x3C\xaa\xaa' | nc 192.168.0.15 8899 # Entirely dark
echo -e '\x55\x00\x00\x00\x02\xff\x08\x33\x20\x5C\xaa\xaa' | nc 192.168.0.15 8899 # Half bright
echo -e '\x55\x00\x00\x00\x02\xff\x08\x33\x40\x7C\xaa\xaa' | nc 192.168.0.15 8899 # Entirely bright

echo -e '\x55\x00\x00\x00\x02\xff\x08\x36\x00\x3F\xaa\xaa' | nc 192.168.0.15 8899 # Cool
echo -e '\x55\x00\x00\x00\x02\xff\x08\x36\x10\x4F\xaa\xaa' | nc 192.168.0.15 8899 # Neutral
echo -e '\x55\x00\x00\x00\x02\xff\x08\x36\x20\x5F\xaa\xaa' | nc 192.168.0.15 8899 # Warm
```
