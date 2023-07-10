// Funktion för att plocka ur värden från solpanelen för att lägga in i nodered.
// Koppla en serial in från arduino till denna och använd sedan meddelandena nedanför.

var dataStr = msg.payload;  // Strängen med värdena

// Dela upp strängen vid kolon och mellanslag
var values = dataStr.split(" : ");

// Extrahera Volt-värdet och ta bort eventuella vita mellanslag
var voltStr = values[0].trim();
var volt = parseFloat(voltStr);

// Extrahera Ampere-värdet och ta bort eventuella vita mellanslag
var ampereStr = values[2].trim();
var ampere = parseFloat(ampereStr);

var volt_battStr = values[1].trim();
var volt_batt = parseFloat(volt_battStr);

// Skapa separata meddelanden för Volt och Ampere
var voltMsg = { msgVolt: volt ,
                msgAmp: ampere,
                msgVoltBatt: volt_batt};
var ampereMsg = { msgAmp: ampere };

return voltMsg;
