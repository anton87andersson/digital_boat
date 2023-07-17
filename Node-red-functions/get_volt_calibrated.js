var get_volt_Batt = msg.msgVoltBatt;
// Messure and add the diffrent in voltage
var diff = 0.5;
var cal_batt = get_volt_Batt - diff;
msg.payload = cal_batt.toFixed(1);
return msg;