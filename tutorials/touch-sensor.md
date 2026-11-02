# Touch Counter

### @explicitHints true

## {Introduction @showdialog}

A **touch sensor** notices when a finger is on its pad, a bit like the screen
on a phone. It tells the micro:bit "touched" or "not touched".

In this tutorial you will build a counter that adds one every time you tap the
sensor.

## {Wire it up @showdialog}

Unplug the micro:bit first. Then use alligator clips to connect the touch
sensor to the big pads on the micro:bit:

* **SIG** goes to **P0**
* **VCC** goes to **3V**
* **GND** goes to **GND**

Plug the micro:bit back in when the clips are on.

## {Show a heart}

From ``||sensorKit:Sensor Kit||``, drag out
``||sensorKit:on touch sensor at P0 touched||``. Put a
``||basic:show icon||`` block inside it and pick the heart.

```blocks
sensorKit.onTouched(DigitalPin.P0, function () {
    basic.showIcon(IconNames.Heart)
})
```

## {Try it}

Click **Download** and copy the program to your micro:bit. Tap the sensor pad.
A heart should appear.

If the heart appears when you **let go** instead of when you touch, your sensor
works the other way around. Put
``||sensorKit:set touch sensor to read low when touched||`` (under **more**) in
``||basic:on start||``.

## {Make a counter}

Make a variable called **count** in ``||variables:Variables||``.

In ``||basic:on start||``, ``||variables:set count to 0||``. In the touch
block, ``||variables:change count by 1||`` and then
``||basic:show number||`` **count**.

```blocks
let count = 0
sensorKit.onTouched(DigitalPin.P0, function () {
    count += 1
    basic.showNumber(count)
})
```

## {Reset button}

Add ``||input:on button A pressed||``. Inside it, set **count** back to **0**
and show it.

```blocks
let count = 0
sensorKit.onTouched(DigitalPin.P0, function () {
    count += 1
    basic.showNumber(count)
})
input.onButtonPressed(Button.A, function () {
    count = 0
    basic.showNumber(count)
})
```

## {Test your counter}

Download your program. Tap the sensor five times and check that the micro:bit
shows **5**. Press **A** to start again.

## {Challenge @showdialog}

Make it your own:

* How many taps can you do in 10 seconds? Use ``||input:running time (ms)||``
  to find out.
* Show a check mark icon when the count reaches 20.
* Use ``||sensorKit:touch sensor at P0 is touched||`` with an
  ``||logic:if||`` block to show a different picture only while a finger is on
  the pad.

```package
fwd-basic-sensor-kit=github:Forward-Education/pxt-fwd-basic-sensor-kit
```
