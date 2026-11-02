# Night Light

### @explicitHints true

## {Introduction @showdialog}

A **light sensor** (photoresistor) changes how much electricity it lets through
when light shines on it. Your micro:bit can read that change as a number.

In this tutorial you will measure light and build a night light that turns on
when the room gets dark.

## {Wire it up @showdialog}

Unplug the micro:bit first. Then use alligator clips to connect the light
sensor to the big pads on the micro:bit:

* **S** goes to **P0**
* the **middle pin** (no label) goes to **3V**
* **-** goes to **GND**

Plug the micro:bit back in when the clips are on.

## {Read the light level}

From ``||sensorKit:Sensor Kit||``, drag ``||sensorKit:light level (%) at P0||``
into a ``||basic:show number||`` block inside ``||basic:forever||``.

```blocks
basic.forever(function () {
    basic.showNumber(sensorKit.lightLevel(AnalogPin.P0))
})
```

## {Try it}

Click **Download** and copy the program to your micro:bit.

The number goes from **0** (dark) to **100** (bright). Cover the sensor with
your hand, then shine a light on it, and watch the number change.

## {Make it easier to read}

Scrolling numbers are hard to read. Swap ``||basic:show number||`` for
``||led:plot bar graph of 0 up to 0||`` from ``||led:Led||``. Put the light
level in the first space and **100** in the second.

More LEDs light up when there is more light.

```blocks
basic.forever(function () {
    led.plotBarGraph(sensorKit.lightLevel(AnalogPin.P0), 100)
})
```

## {Build the night light}

Now make the micro:bit light up when it gets dark.

Replace the bar graph with an ``||logic:if then else||`` block. Check if the
``||sensorKit:light level||`` is **less than 30**. If it is, use
``||basic:show leds||`` to turn on every LED. Otherwise,
``||basic:clear screen||``.

```blocks
basic.forever(function () {
    if (sensorKit.lightLevel(AnalogPin.P0) < 30) {
        basic.showLeds(`
            # # # # #
            # # # # #
            # # # # #
            # # # # #
            # # # # #
            `)
    } else {
        basic.clearScreen()
    }
})
```

## {Test your night light}

Download your program again. Cover the sensor with your hand. The night light
should switch on, then switch off when you take your hand away.

If it switches on too easily or not at all, change **30** to a different number.

## {Challenge @showdialog}

Make it your own:

* Show the sleepy face when it is dark and the happy face when it is bright.
* Press **A** to see the exact light level as a number.
* Test different spots in your classroom. Which is the brightest?
