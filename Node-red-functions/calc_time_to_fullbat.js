// För att beräkna tid till fulladdat batteri, enbart teoretisk tid!!

// Anpassa värdena nedan enligt dina behov
const batterikapacitet = 80; 
const fullSpanning = 13.7;
var nuvarandeSpanning = msg.msgVoltBatt; 
var laddningsstrom = msg.msgAmp; 

// Beräkna laddningstiden
var tid = (batterikapacitet * (fullSpanning - nuvarandeSpanning)) / laddningsstrom;

// Skicka laddningstiden som utdata

if (tid >= 0) {
msg.payload = tid.toFixed(1) + " timmar";
}
else {
    msg.payload = "Fulladdat"
}


return msg;
