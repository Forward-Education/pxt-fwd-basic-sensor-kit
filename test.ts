// Exercises every block in the extension. Compiles as part of the test build.

// Light
basic.showNumber(sensorKit.lightLevel(AnalogPin.P0))

// Soil moisture
basic.showNumber(sensorKit.soilMoisture(AnalogPin.P0))

// Touch
sensorKit.setTouchLevel(SensorKitTouchLevel.High)
if (sensorKit.isTouched(DigitalPin.P0)) {
    basic.showIcon(IconNames.Yes)
}
sensorKit.onTouched(DigitalPin.P0, function () {
    basic.showIcon(IconNames.Heart)
})

// Sonar
sensorKit.setSonarPins(DigitalPin.P1, DigitalPin.P0)
basic.showNumber(sensorKit.sonarDistance())
sensorKit.onObjectCloser(10, function () {
    basic.showIcon(IconNames.Surprised)
})

// RGB LED
sensorKit.setRgbPins(AnalogPin.P0, AnalogPin.P1, AnalogPin.P2)
sensorKit.setRgbType(SensorKitRgbType.CommonCathode)
sensorKit.setRgbColor(0xff8000)
sensorKit.setRgb(0, 128, 255)
sensorKit.setRgbType(SensorKitRgbType.CommonAnode)
sensorKit.rgbOff()
