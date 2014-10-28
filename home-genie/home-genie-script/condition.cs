// Remember to Change 'SensorName' to the correct name of your sensor
var mySensor = Modules.WithName("motion_sensor").Get();

// Debug code
// Program.Notify("Debug", mySensor.Parameter("Sensor.Generic").DecimalValue.ToString());

// Returns 'True' if the value of the sensor is 38 or higher
return (mySensor.WasFound && mySensor.Parameter("Sensor.Generic").DecimalValue >= 1);
