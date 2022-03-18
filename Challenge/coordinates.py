# Import serial package and other necessary packages
import serial
from time import sleep
import reverse_geocode

gpgga_info = "$GPGGA,"
ser = serial.Serial ("/dev/serial0")    # Open port with baud rate
GPGGA_buffer = 0
NMEA_buff = 0
lat_in_degrees = 0
long_in_degrees = 0

# Gets new updated GPS info
def GPS_Info():
    #Create variables to store values
    global NMEA_buff
    global lat_in_degrees
    global long_in_degrees
    nmea_time = []
    nmea_latitude = []
    nmea_longitude = []
    nmea_time = NMEA_buff[0]                    # Extract time from GPGGA string
    nmea_latitude = NMEA_buff[1]                # Extract latitude from GPGGA string
    nmea_latitude_dir = NMEA_buff[2]            # Extract the direction of latitude(N/S)
    nmea_longitude = NMEA_buff[3]               # Extract longitude from GPGGA string
    nmea_longitude_dir = NMEA_buff[4]           # Extract the direction of longitude(E/W)

    lat = float(nmea_latitude)                  #convert string into float for calculation
    longi = float(nmea_longitude)               #convert string into float for calculation

    # Get latitude in degree decimal format with direction
    lat_in_degrees = convert_to_degrees(lat) if nmea_latitude_dir == 'N' else (convert_to_degrees(-1 * lat))  
    # Get longitude in degree decimal format with direction
    long_in_degrees = convert_to_degrees(longi) if nmea_longitude_dir == 'E' else (convert_to_degrees(-1 * longi))

# Convert raw NMEA string into degree decimal format
def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.4f" %(position)
    return position

# Returns city from reverse geocode, provided with coordinates
def get_city(lat, long):
    coordinates = (lat, long)
    return reverse_geocode.get(coordinates)['city']

# Returns coordinates from GPS module
def locate():
    global NMEA_buff
    while True:
        received_data = (str)(ser.readline())                   # Read NMEA string received
        GPGGA_data_available = received_data.find(gpgga_info)   # Check for NMEA GPGGA string
        if (GPGGA_data_available>0):
            GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  # Store data coming after "$GPGGA," string
            NMEA_buff = (GPGGA_buffer.split(','))               # Store comma separated data in buffer
            GPS_Info()                                          # Get time, latitude, longitude

            return lat_in_degrees, long_in_degrees

if __name__ == '__main__':
    get_city(32.9345, -117.1327)