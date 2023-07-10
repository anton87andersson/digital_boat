// För att få fram hur många watt solpanelen laddar

var volt = msg.msgVolt;
var amp = msg.msgAmp;

// Beräkna effekten i Watt
var effekt = parseFloat((volt * amp).toFixed(2));

// Skapa ett meddelandeobjekt med effektvärdet
var effektMsg = { payload: effekt };

return effektMsg;
