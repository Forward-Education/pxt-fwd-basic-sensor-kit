# Mood Light

### @explicitHints true

## {Introduction @showdialog}

An **RGB LED** is three tiny lights in one: **R**ed, **G**reen and **B**lue.
By mixing them at different brightness levels you can make almost any colour.

In this tutorial you will make a mood light that changes colour.

## {Wire it up @showdialog}

Unplug the micro:bit first. Then use alligator clips to connect the RGB LED
to the big pads on the micro:bit:

* **R** goes to **P0**
* **G** goes to **P1**
* **B** goes to **P2**
* the **common pin** (**-**) goes to **GND**

Plug the micro:bit back in when the clips are on.

## {Show a colour}

From ``||sensorKit:Sensor Kit||``, drag ``||sensorKit:set RGB LED to||`` into
``||basic:on start||``. Click the colour and pick red.

```blocks
sensorKit.setRgbColor(0xff0000)
```

## {Try it}

Click **Download** and copy the program to your micro:bit. The LED should
glow red.

If it glows light blue instead of red, your LED is the other type and its
common pin goes to **3V**. Move that clip from **GND** to **3V**. Put
``||sensorKit:set RGB LED common pin to 3V||`` at the start of
``||basic:on start||``.

## {Change colours}

Move your colour block into ``||basic:forever||``. Add a
``||basic:pause (ms) 1000||``, then two more colour blocks with pauses so the
LED goes red, green, blue.

```blocks
basic.forever(function () {
    sensorKit.setRgbColor(0xff0000)
    basic.pause(1000)
    sensorKit.setRgbColor(0x00ff00)
    basic.pause(1000)
    sensorKit.setRgbColor(0x0000ff)
    basic.pause(1000)
})
```

## {Mix your own}

``||sensorKit:set RGB LED to red green blue||`` lets you mix colours. Each one
goes from **0** (off) to **255** (full).

Add ``||input:on button A pressed||`` and use ``||math:pick random 0 to 255||``
for each colour. Every press makes a surprise colour.

```blocks
basic.forever(function () {
    sensorKit.setRgbColor(0xff0000)
    basic.pause(1000)
    sensorKit.setRgbColor(0x00ff00)
    basic.pause(1000)
    sensorKit.setRgbColor(0x0000ff)
    basic.pause(1000)
})
input.onButtonPressed(Button.A, function () {
    sensorKit.setRgb(randint(0, 255), randint(0, 255), randint(0, 255))
})
```

## {Test your mood light}

Download your program. Watch the colours change, then press **A** for a random
colour. It only lasts until the ``||basic:forever||`` loop sets the next colour.
Can you work out how to fix that?

## {Challenge @showdialog}

Make it your own:

* Use **red 255, green 0, blue 255**. What colour do you get? Try making yellow
  and orange.
* Build a traffic light that goes green, yellow, then red.
* Press **B** to ``||sensorKit:turn RGB LED off||``.

```package
fwd-basic-sensor-kit=github:Forward-Education/pxt-fwd-basic-sensor-kit
```
