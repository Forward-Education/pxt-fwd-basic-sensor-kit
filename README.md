# fwd-basic-sensor-kit

MakeCode extension for the Forward Education **micro:bit Sensor Starter Kit**
(SKU FE-01-1202). It adds a **Sensor Kit** drawer with simple blocks for every
module in the kit: a light sensor, a soil moisture sensor, a touch sensor, a
sonar distance sensor and an RGB LED.

Developed and maintained by [Forward Education](https://forwardedu.com).

## Use as Extension

This repository can be added as an **extension** in MakeCode.

- open [https://makecode.microbit.org/](https://makecode.microbit.org/)
- click on **New Project**
- click on **Extensions** under the gearwheel menu
- search for **https://github.com/Forward-Education/pxt-fwd-basic-sensor-kit** and import

## How to connect the modules

There is no breakout board. Each module clips straight onto the micro:bit's
large pads with the alligator clips from the kit. Power always comes from the
**3V** pad and every module shares the **GND** pad.

Connect **one module at a time**. The pins below are the defaults the blocks
use. If you clip a wire to a different pad, change the pin in the block to
match.

### Light sensor (photoresistor)

| Module pin | micro:bit pad |
|---|---|
| S | P0 |
| middle pin (no label) | 3V |
| - | GND |

```blocks
basic.forever(function () {
    basic.showNumber(sensorKit.lightLevel(AnalogPin.P0))
})
```

The light level goes from 0 (dark) to 100 (bright).

### Soil moisture sensor

| Module pin | micro:bit pad |
|---|---|
| signal (S) | P0 |
| power (+) | 3V |
| ground (-) | GND |

```blocks
basic.forever(function () {
    if (sensorKit.soilMoisture(AnalogPin.P0) < 30) {
        basic.showIcon(IconNames.Sad)
    } else {
        basic.showIcon(IconNames.Happy)
    }
})
```

Moisture goes from 0 (dry) to 100 (wet). Push the two prongs into the soil, but
keep the electronics on top dry.

### Touch sensor

| Module pin | micro:bit pad |
|---|---|
| signal (SIG) | P0 |
| power (VCC) | 3V |
| ground (GND) | GND |

```blocks
sensorKit.onTouched(DigitalPin.P0, function () {
    basic.showIcon(IconNames.Heart)
})
```

Use **touch sensor is touched** inside an `if` block, or **on touch sensor
touched** to run code each time a finger taps the pad.

### Sonar (ultrasonic distance sensor)

| Module pin | micro:bit pad |
|---|---|
| TRIG | P1 |
| ECHO | P0 |
| VCC | 3V |
| GND | GND |

```blocks
basic.forever(function () {
    basic.showNumber(sensorKit.sonarDistance())
})
sensorKit.onObjectCloser(10, function () {
    basic.showIcon(IconNames.Surprised)
})
```

Distance is in centimetres. The sonar reaches about 4 m. When nothing is in
range, the distance is **0**, so check for that before comparing:

```blocks
basic.forever(function () {
    let d = sensorKit.sonarDistance()
    if (d > 0 && d < 20) {
        basic.showIcon(IconNames.No)
    } else {
        basic.clearScreen()
    }
})
```

If you clip TRIG and ECHO to other pads, add **set sonar pins** at the start of
your program.

### RGB LED

| Module pin | micro:bit pad |
|---|---|
| R | P0 |
| G | P1 |
| B | P2 |
| common pin (-) | GND |

```blocks
sensorKit.setRgbColor(0xff0000)
basic.pause(1000)
sensorKit.setRgb(0, 128, 255)
basic.pause(1000)
sensorKit.rgbOff()
```

Mix your own colour by giving red, green and blue a value from 0 to 255.

The kit LED is **common cathode**, so its common pin goes to GND. Some other
RGB LED boards are **common anode**, with the common pin going to 3V. For
those, add **set RGB LED common pin to 3V** at the start of your program, or
the colours will come out backwards.

## Blocks

| Group | Block |
|---|---|
| Light | `light level (%) at P0` |
| Soil moisture | `soil moisture (%) at P0` |
| Touch | `touch sensor at P0 is touched`, `on touch sensor at P0 touched` |
| Sonar | `sonar distance (cm)`, `on object closer than 10 cm`, `set sonar pins TRIG P1 ECHO P0` |
| RGB LED | `set RGB LED to (colour)`, `set RGB LED to red green blue`, `turn RGB LED off`, `set RGB LED common pin to GND/3V`, `set RGB LED pins` |
| more... | `set touch sensor to read high/low when touched` (only for touch modules that read low when touched) |

## Supported targets

- for PXT/microbit

## License

MIT

#### Metadata (used for search, rendering)

- for PXT/microbit

<script src="https://makecode.com/gh-pages-embed.js"></script><script>makeCodeRender("{{ site.makecode.home_url }}", "{{ site.github.owner_name }}/{{ site.github.repository_name }}");</script>
