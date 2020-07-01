import serial
import time
import math

LJUST_VAL = 10


def convert_pm25_to_aqi(conc):
    conc_lo, conc_hi, aqi_lo, aqi_hi = get_pm25_breakpoints(conc)
    return get_aqi(conc, conc_lo, conc_hi, aqi_lo, aqi_hi)


def get_pm25_breakpoints(conc):
    truncated_conc = float(format(conc, '.1f'))
    if truncated_conc < 0:
        raise ValueError("Concentration cannot be below zero!")
    elif truncated_conc <= 12:
        return (0, 12, 0, 50)
    elif truncated_conc <= 35.4:
        return (12.1, 35.4, 51, 100)
    elif truncated_conc <= 55.4:
        return (35.5, 55.4, 101, 150)
    elif truncated_conc <= 150.4:
        return (55.5, 150.4, 151, 200)
    elif truncated_conc <= 250.4:
        return (150.5, 250.4, 201, 300)
    elif truncated_conc <= 500.4:
        return (250.5, 500.4, 301, 500)
    else:
        raise ValueError("Concentration too high to be calculated by AQI!")


def convert_pm10_to_aqi(conc):
    conc_lo, conc_hi, aqi_lo, aqi_hi = get_pm10_breakpoints(conc)
    return get_aqi(conc, conc_lo, conc_hi, aqi_lo, aqi_hi)


def get_pm10_breakpoints(conc):
    truncated_conc = math.floor(conc)
    if truncated_conc < 0:
        raise ValueError("Concentration cannot be below zero!")
    elif truncated_conc <= 54:
        return (0, 54, 0, 50)
    elif truncated_conc <= 154:
        return (55, 154, 51, 100)
    elif truncated_conc <= 254:
        return (155, 254, 101, 150)
    elif truncated_conc <= 354:
        return (255, 354, 151, 200)
    elif truncated_conc <= 424:
        return (355, 424, 201, 300)
    elif truncated_conc <= 604:
        return (425, 604, 301, 500)
    else:
        raise ValueError("Concentration too high to be calculated by AQI!")


def get_aqi(conc, conc_lo, conc_hi, aqi_lo, aqi_hi):
    raw = ((aqi_hi - aqi_lo) / (conc_hi - conc_lo)) * (conc - conc_lo) + aqi_lo
    return round(raw)


if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0')
    data = []

    for i in range(0, 10):
        raw = ser.read()
        data.append(raw)
    ser.close()

    pm25 = str(int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10)
    pm10 = str(int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10)

    aqi25 = str(convert_pm25_to_aqi(pm25))
    aqi10 = str(convert_pm10_to_aqi(pm10))

    print('pm2.5: '.ljust(LJUST_VAL) + pm25 + ' ug/m3')
    print('pm10: '.ljust(LJUST_VAL) + pm10 + ' ug/m3')

    print('aqi2.5: '.ljust(LJUST_VAL) + aqi25)
    print('aqi10: '.ljust(LJUST_VAL) + aqi10)
