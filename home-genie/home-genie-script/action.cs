var mySensorValue = Modules.WithName("motion_sensor").Get().Parameter("Sensor.Generic").DecimalValue.ToString();

Net.SendMessage("risethink@nebrios.com", "", "hg_motion := " + mySensorValue);
