/**
 * Forward Education micro:bit Sensor Starter Kit (FE-01-1202).
 *
 * Every module is powered from the micro:bit 3V pad with alligator clips and
 * connects to P0, P1 or P2. Pin defaults below match the kit wiring guide.
 */

enum SensorKitRgbType {
    //% block="GND (common cathode)"
    CommonCathode = 0,
    //% block="3V (common anode)"
    CommonAnode = 1
}

enum SensorKitTouchLevel {
    //% block="high"
    High = 1,
    //% block="low"
    Low = 0
}

//% block="Sensor Kit"
//% color=#5BA42D
//% icon="\uf2db"
//% weight=100
//% groups='["Light", "Soil moisture", "Touch", "Sonar", "RGB LED"]'
namespace sensorKit {
    const ANALOG_MAX = 1023
    const SONAR_TIMEOUT_US = 25000 // ~4.3 m range; pulseIn gives 0 = no echo
    const SONAR_MIN_GAP_MS = 60 // let old echoes die out between pings
    const TOUCH_POLL_MS = 20
    const SONAR_POLL_MS = 100

    function toPercent(raw: number): number {
        return Math.constrain(Math.idiv(raw * 100 + 511, ANALOG_MAX), 0, 100)
    }

    // shared poller for the event blocks; each watcher raises its own event value
    let eventsStarted = false
    let touchWatchers: TouchWatcher[] = []
    let sonarWatchers: SonarWatcher[] = []

    class TouchWatcher {
        last = false
        constructor(public pin: DigitalPin, public value: number) { }
    }

    class SonarWatcher {
        wasClose = false
        nextCheck = 0
        constructor(public cm: number, public value: number) { }
    }

    function startEvents(): void {
        if (eventsStarted) return
        eventsStarted = true
        control.inBackground(() => {
            while (true) {
                const now = control.millis()
                for (const w of touchWatchers) {
                    const touched = isTouched(w.pin)
                    if (touched && !w.last) control.raiseEvent(DAL.DEVICE_ID_NOTIFY, w.value)
                    w.last = touched
                }
                for (const w of sonarWatchers) {
                    if (now < w.nextCheck) continue
                    w.nextCheck = now + SONAR_POLL_MS
                    const d = sonarDistance()
                    const close = d > 0 && d < w.cm
                    if (close && !w.wasClose) control.raiseEvent(DAL.DEVICE_ID_NOTIFY, w.value)
                    w.wasClose = close
                }
                basic.pause(TOUCH_POLL_MS)
            }
        })
    }

    // ---------------- Light ----------------

    /**
     * Read the photoresistor module as a light level from 0 (dark) to 100 (bright).
     * Wiring: S to P0, middle pin to 3V, "-" to GND.
     * @param pin the pin the S wire is clipped to
     */
    //% group="Light"
    //% block="light level (\\%) at $pin"
    //% blockId=fwd_sensorkit_light
    //% pin.defl=AnalogPin.P0
    //% weight=100
    export function lightLevel(pin: AnalogPin = AnalogPin.P0): number {
        // the module pulls S towards GND as light increases, so flip it
        return 100 - toPercent(pins.analogReadPin(pin))
    }

    // ---------------- Soil moisture ----------------

    /**
     * Read the soil moisture sensor from 0 (dry) to 100 (wet).
     * Wiring: signal (S) to P0, + to 3V, - to GND.
     * @param pin the pin the signal wire is clipped to
     */
    //% group="Soil moisture"
    //% block="soil moisture (\\%) at $pin"
    //% blockId=fwd_sensorkit_moisture
    //% pin.defl=AnalogPin.P0
    //% weight=90
    export function soilMoisture(pin: AnalogPin = AnalogPin.P0): number {
        return toPercent(pins.analogReadPin(pin))
    }

    // ---------------- Touch ----------------

    let touchActive = SensorKitTouchLevel.High

    /**
     * Check if the touch sensor is being touched.
     * Wiring: signal (SIG) to P0, VCC to 3V, GND to GND.
     * @param pin the pin the signal wire is clipped to
     */
    //% group="Touch"
    //% block="touch sensor at $pin is touched"
    //% blockId=fwd_sensorkit_touched
    //% pin.defl=DigitalPin.P0
    //% weight=80
    export function isTouched(pin: DigitalPin = DigitalPin.P0): boolean {
        return pins.digitalReadPin(pin) == touchActive
    }

    /**
     * Run code once each time the touch sensor is touched.
     * @param pin the pin the signal wire is clipped to
     */
    //% group="Touch"
    //% block="on touch sensor at $pin touched"
    //% blockId=fwd_sensorkit_on_touched
    //% pin.defl=DigitalPin.P0
    //% weight=79
    export function onTouched(pin: DigitalPin, handler: () => void): void {
        const value = control.allocateNotifyEvent()
        touchWatchers.push(new TouchWatcher(pin, value))
        control.onEvent(DAL.DEVICE_ID_NOTIFY, value, handler)
        startEvents()
    }

    /**
     * Choose what the touch sensor output reads while it is touched.
     * The kit sensor reads high, so you only need this for a different module.
     * @param level the pin level while touched
     */
    //% group="Touch"
    //% block="set touch sensor to read $level when touched"
    //% blockId=fwd_sensorkit_touch_level
    //% advanced=true
    export function setTouchLevel(level: SensorKitTouchLevel): void {
        touchActive = level
    }

    // ---------------- Sonar ----------------

    let trigPin = DigitalPin.P1
    let echoPin = DigitalPin.P0
    let lastPing = -SONAR_MIN_GAP_MS

    /**
     * Measure the distance to an object in centimetres with the sonar module.
     * Returns 0 when nothing is in range (about 4 m).
     * Wiring: TRIG to P1, ECHO to P0, VCC to 3V, GND to GND.
     */
    //% group="Sonar"
    //% block="sonar distance (cm)"
    //% blockId=fwd_sensorkit_sonar
    //% weight=70
    export function sonarDistance(): number {
        // loop so a ping from another fiber during the pause still gets its gap
        while (control.millis() - lastPing < SONAR_MIN_GAP_MS)
            basic.pause(lastPing + SONAR_MIN_GAP_MS - control.millis())
        lastPing = control.millis()

        pins.digitalWritePin(trigPin, 0)
        control.waitMicros(2)
        pins.digitalWritePin(trigPin, 1)
        control.waitMicros(10)
        pins.digitalWritePin(trigPin, 0)
        const us = pins.pulseIn(echoPin, PulseValue.High, SONAR_TIMEOUT_US)
        return Math.idiv(us, 58)
    }

    /**
     * Run code once each time an object comes closer than a distance.
     * @param cm the distance in centimetres
     */
    //% group="Sonar"
    //% block="on object closer than $cm cm"
    //% blockId=fwd_sensorkit_on_closer
    //% cm.defl=10 cm.min=2 cm.max=400
    //% weight=69
    export function onObjectCloser(cm: number, handler: () => void): void {
        const value = control.allocateNotifyEvent()
        sonarWatchers.push(new SonarWatcher(cm, value))
        control.onEvent(DAL.DEVICE_ID_NOTIFY, value, handler)
        startEvents()
    }

    /**
     * Choose which pins the sonar module is clipped to.
     * @param trig the pin for TRIG
     * @param echo the pin for ECHO
     */
    //% group="Sonar"
    //% block="set sonar pins TRIG $trig ECHO $echo"
    //% blockId=fwd_sensorkit_sonar_pins
    //% trig.defl=DigitalPin.P1 echo.defl=DigitalPin.P0
    //% inlineInputMode=inline
    //% weight=68
    export function setSonarPins(trig: DigitalPin, echo: DigitalPin): void {
        trigPin = trig
        echoPin = echo
    }

    // ---------------- RGB LED ----------------

    let rgbType = SensorKitRgbType.CommonCathode
    let redPin = AnalogPin.P0
    let greenPin = AnalogPin.P1
    let bluePin = AnalogPin.P2
    let red = 0
    let green = 0
    let blue = 0

    function writeChannel(pin: AnalogPin, value: number): void {
        let duty = Math.idiv(Math.constrain(value, 0, 255) * ANALOG_MAX, 255)
        if (rgbType == SensorKitRgbType.CommonAnode) duty = ANALOG_MAX - duty
        pins.analogWritePin(pin, duty)
    }

    function showRgb(): void {
        writeChannel(redPin, red)
        writeChannel(greenPin, green)
        writeChannel(bluePin, blue)
    }

    /**
     * Set the RGB LED to a colour.
     * Wiring: R to P0, G to P1, B to P2, common pin to GND.
     * @param color the colour to show
     */
    //% group="RGB LED"
    //% block="set RGB LED to $color"
    //% blockId=fwd_sensorkit_rgb_color
    //% color.shadow="colorNumberPicker"
    //% weight=60
    export function setRgbColor(color: number): void {
        setRgb((color >> 16) & 0xff, (color >> 8) & 0xff, color & 0xff)
    }

    /**
     * Set the RGB LED by mixing red, green and blue (0 to 255 each).
     * @param r red brightness
     * @param g green brightness
     * @param b blue brightness
     */
    //% group="RGB LED"
    //% block="set RGB LED to red $r green $g blue $b"
    //% blockId=fwd_sensorkit_rgb_values
    //% r.min=0 r.max=255 r.defl=255
    //% g.min=0 g.max=255 g.defl=0
    //% b.min=0 b.max=255 b.defl=0
    //% inlineInputMode=inline
    //% weight=59
    export function setRgb(r: number, g: number, b: number): void {
        red = r
        green = g
        blue = b
        showRgb()
    }

    /**
     * Turn the RGB LED off.
     */
    //% group="RGB LED"
    //% block="turn RGB LED off"
    //% blockId=fwd_sensorkit_rgb_off
    //% weight=58
    export function rgbOff(): void {
        setRgb(0, 0, 0)
    }

    /**
     * Tell the extension where the RGB LED common pin is connected.
     * The kit board is common cathode, so its common pin goes to GND.
     * Choose 3V for a common anode board.
     * @param type where the common pin goes
     */
    //% group="RGB LED"
    //% block="set RGB LED common pin to $type"
    //% blockId=fwd_sensorkit_rgb_type
    //% weight=57
    export function setRgbType(type: SensorKitRgbType): void {
        rgbType = type
        showRgb()
    }

    /**
     * Choose which pins the RGB LED is clipped to.
     * @param r the pin for R
     * @param g the pin for G
     * @param b the pin for B
     */
    //% group="RGB LED"
    //% block="set RGB LED pins red $r green $g blue $b"
    //% blockId=fwd_sensorkit_rgb_pins
    //% r.defl=AnalogPin.P0 g.defl=AnalogPin.P1 b.defl=AnalogPin.P2
    //% inlineInputMode=inline
    //% weight=56
    export function setRgbPins(r: AnalogPin, g: AnalogPin, b: AnalogPin): void {
        redPin = r
        greenPin = g
        bluePin = b
        showRgb()
    }
}
