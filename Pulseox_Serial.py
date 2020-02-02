import serial
import time
import csv

STATUS = {0:	'Success',
          1: 	'Not Ready',
         -1: 	'Object Detected',
         -2: 	'Excessive Sensor Device Motion',
         -3: 	'No object detected',
         -4:	'Pressing too hard',
         -5: 	'Object other than finger detected',
         -6: 	'Excessive finger motion',
         -7:    'Serial Error'}


class Reading:
    def __init__(self, status, heart_rate, oxygen, confidence, now):
        self._status = int(status)
        self._heart_rate = heart_rate
        self._oxygen = oxygen
        self._confidence = confidence
        self._now = now

    def status(self):
        return self._status

    def heart_rate(self):
        return int(self._heart_rate)

    def oxygen(self):
        return int(self._oxygen)

    def confidence(self):
        return int(self._confidence)

    def now(self):
        return time.mktime(self._now)

    def status_out(self):
        return f'{STATUS[self._status]}'

    def heart_rate_out(self):
        return f'heart rate = {self._heart_rate} bpm'

    def oxygen_out(self):
        return f'oxygen {self._oxygen}%'

    def confidence_out(self):
        return f'confidence= {self._confidence}'

    def now_out(self):
        return f'Time: {time.strftime("%H:%M:%S", self._now)}'

    def save_reading(self):
        if self.status() in range(-6, 0) or (self.status() == 0 and self.confidence() == 0):
            with open('error.csv', 'a', newline='') as csvfile:
                data_write = csv.writer(csvfile, delimiter=',')
                data_write.writerow([self.now(), self.status()])
        elif self.status() == 0:
            with open('data.csv', 'a', newline='') as csvfile:
                data_write = csv.writer(csvfile, delimiter=',')
                data_write.writerow([self.now(), self.heart_rate(), self.oxygen(), self.confidence()])


class PusleOx():
    def __init__(self):
        self.ser = serial.Serial(
                port='/dev/ttyACM0',
                baudrate=115200,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1
        )

    def get_reading(self):
        try:
            return Reading(*self.ser.readline().decode('utf-8').split(), time.localtime())
        except:
            return Reading(-7, 0, 0, 0, time.localtime())


def main(sensor):
    while True:
        time.sleep(1)
        reading = sensor.get_reading()
        print(f'{reading.now_out()}  {bool(reading.status())*reading.status_out()} {(not bool(reading.status()))*reading.heart_rate_out()} {(not bool(reading.status()))*reading.oxygen_out()} {(not bool(reading.status()))*reading.confidence_out()}')
        reading.save_reading()


if __name__ == "__main__":
    pulse_ox = PusleOx()
    main(pulse_ox)

