# Parking Sensor

### @explicitHints true

## {Introduction @showdialog}

A **sonar** sensor measures distance with sound. One of its round "eyes" sends
out a click that is too high for people to hear, and the other listens for the
echo. The longer the echo takes to come back, the farther away the object is.

In this tutorial you will build a parking sensor like the ones in cars.

## {Wire it up @showdialog}

Unplug the micro:bit first. The sonar has four pins. Use alligator clips to
connect them to the big pads on the micro:bit:

* **VCC** goes to **3V**
* **TRIG** goes to **P1**
* **ECHO** goes to **P0**
* **GND** goes to **GND**

Plug the micro:bit back in when the clips are on.

## {Show the distance}

From ``||sensorKit:Sensor Kit||``, drag ``||sensorKit:sonar distance (cm)||``
into ``||led:plot bar graph of 0 up to 0||`` inside ``||basic:forever||``. Put
**100** in the second space.

```blocks
basic.forever(function () {
    led.plotBarGraph(sensorKit.sonarDistance(), 100)
})
```

## {Try it}

Click **Download** and copy the program to your micro:bit.

Point the sonar at a wall and move your hand towards it. The closer your hand
gets, the fewer LEDs light up. A full screen means about 1 m or more.

If the screen goes blank, the sonar cannot see anything. It reads **0** when
nothing is in range.

## {Build the parking sensor}

Make a variable called **distance** and set it to the
``||sensorKit:sonar distance (cm)||`` at the start of ``||basic:forever||``.

Then use an ``||logic:if then else||`` block:

* If **distance** is more than **0** and less than **10**, show the
  ``||basic:X icon||``. Stop!
* Otherwise, ``||led:plot bar graph||`` of **distance** up to **100**.

```blocks
let distance = 0
basic.forever(function () {
    distance = sensorKit.sonarDistance()
    if (distance > 0 && distance < 10) {
        basic.showIcon(IconNames.No)
    } else {
        led.plotBarGraph(distance, 100)
    }
})
```

## {Test your parking sensor}

Download your program. Slowly move a book towards the sonar. The bar graph
should shrink, then switch to an **X** when the book is closer than 10 cm.

## {Challenge @showdialog}

Make it your own:

* Add a middle warning, such as a small square when the distance is between
  10 and 30 cm.
* Build a visitor counter with ``||sensorKit:on object closer than 10 cm||``.
  It runs once each time something comes closer than the distance you choose,
  so it can add one each time someone walks past.
* Measure things around the room in centimetres and check them with a ruler.
