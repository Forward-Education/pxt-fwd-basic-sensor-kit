# Thirsty Plant Alarm

### @explicitHints true

## {Introduction @showdialog}

A **soil moisture sensor** has two metal prongs. Wet soil lets electricity
flow between them more easily than dry soil, and your micro:bit can read the
difference as a number.

In this tutorial you will build an alarm that tells you when a plant needs
water.

## {Wire it up @showdialog}

Unplug the micro:bit first. Then use alligator clips to connect the soil
moisture sensor to the big pads on the micro:bit:

* **S** (signal) goes to **P0**
* **+** goes to **3V**
* **-** goes to **GND**

Plug the micro:bit back in when the clips are on.

Only the prongs go in the soil. Keep the micro:bit, the clips and the top of
the sensor dry.

## {Read the moisture}

From ``||sensorKit:Sensor Kit||``, drag ``||sensorKit:soil moisture (%) at P0||``
into ``||led:plot bar graph of 0 up to 0||`` inside ``||basic:forever||``. Put
**100** in the second space.

```blocks
basic.forever(function () {
    led.plotBarGraph(sensorKit.soilMoisture(AnalogPin.P0), 100)
})
```

## {Try it}

Click **Download** and copy the program to your micro:bit.

Moisture goes from **0** (dry) to **100** (wet). Hold the sensor in the air, then
push the prongs into damp soil or touch them to a wet paper towel. More LEDs
light up when it is wetter.

## {Build the alarm}

Replace the bar graph with an ``||logic:if then else||`` block. If the
``||sensorKit:soil moisture||`` is **less than 30**, show a
``||basic:sad face||``. Otherwise, show a ``||basic:happy face||``.

```blocks
basic.forever(function () {
    if (sensorKit.soilMoisture(AnalogPin.P0) < 30) {
        basic.showIcon(IconNames.Sad)
    } else {
        basic.showIcon(IconNames.Happy)
    }
})
```

## {Check the number}

Every soil is different, so it helps to see the exact number. Add an
``||input:on button A pressed||`` block that shows the
``||sensorKit:soil moisture||`` with ``||basic:show number||``.

```blocks
basic.forever(function () {
    if (sensorKit.soilMoisture(AnalogPin.P0) < 30) {
        basic.showIcon(IconNames.Sad)
    } else {
        basic.showIcon(IconNames.Happy)
    }
})
input.onButtonPressed(Button.A, function () {
    basic.showNumber(sensorKit.soilMoisture(AnalogPin.P0))
})
```

## {Test your alarm}

Download your program. Press **A** with the prongs in dry soil and again in
freshly watered soil. Pick a number between the two and use it in place of
**30**.

## {Challenge @showdialog}

Make it your own:

* Add a third face for soil that is too wet.
* Make the sad face flash so it is easier to notice.
* Test plants around your school. Which one is the thirstiest?
