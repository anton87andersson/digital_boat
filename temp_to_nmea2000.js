// För att skicka datan till NMEA2000 nätverk
// Kopplas till noden signalk-send-pathvalue
// Tänk på att tempraturen i NMEA-2000 nätverk är i kelvin!!

// Spara datan till Signalk som sedan transporterar det vidare till NMEA2000
var path = "propulsion.b20.coolantTemperature";

// Gör om till kelvin
var value = parseFloat(msg.payload)+273.15;

msg.topic = path;
msg.payload = value;

return msg;
