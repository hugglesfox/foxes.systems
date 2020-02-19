# Accessing the BBC micro:bit REPL on Gentoo
*February 9, 2019*

![](/static/images/microbit_repl.png)
Thanks to the [National Computer Science School](https://ncss.edu.au/) I'm
now the proud owner of a [BBC micro:bit](https://microbit.org/). The
micro:bit has the ability to provide a python REPL over USB serial but
when plugging it into my Gentoo machine, the micro:bit doesn't show up in
`/dev`. What gives?

Like most things, a kernel module is required to provide the drivers for
the USB serial interface. On first inspection you would think that
`CONFIG_USB_SERIAL_CONSOLE` is the correct module, but no. The micro:bit's
REPL is actually treated as a USB modem which requires `CONFIG_USB_ACM` to
be set.

#### Kernel

```
Device Drivers --->
  [*]  USB Support --->
    <*>  USB Modem (CDC ACM) support
```

Now that the module is enabled, [rebuild the
kernel](https://wiki.gentoo.org/wiki/Kernel/Rebuild) and reboot.


Once rebooted plug in the micro:bit and there should be a new device in `/dev`
called `/dev/ttyACM0` (or something similar). Now it's as simple as
connecting to your micro:bit REPL using your serial console client of choice!

```bash
picocom /dev/ttyACM0 -b 115200
```

[The micro:bit documentation as some more examples.](https://microbit-micropython.readthedocs.io/en/latest/devguide/repl.html)

Happy hacking.

H
