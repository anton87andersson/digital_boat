// För att beräkna hur många procent batteriet har kvar.

var totalKapacitet = 80; // Total kapacitet i Ah
var fulladdadSpanning = 13.7; // Spänning vid fulladdning i volt
var kvarvarandeSpanning = msg.payload; // Aktuell kvarvarande spänning i volt
var diff = 0.5;
var kvarvarandeKapacitet = (kvarvarandeSpanning / fulladdadSpanning) * totalKapacitet;
var procentKvar = (kvarvarandeKapacitet / totalKapacitet) * 100;

msg.payload = procentKvar.toFixed(1); // Avrunda till två decimaler
return msg;
