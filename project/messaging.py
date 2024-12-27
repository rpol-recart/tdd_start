import numbers


class DetectionMessage():
    def __init__(self):
        pass

    def read(self, message):
        pass


class GpsMessage():
    GPS_ON = 1
    GPS_OFF = 0

    def __init__(self, log_on=False):

        self.log_on = log_on
        self.gps1 = self.GPS_ON
        self.gps2 = self.GPS_ON
        self.gps1_alt = self.GPS_ON
        self.gps2_alt = self.GPS_ON
        self._lat1 = None
        self._long1 = None
        self._alt1 = None
        self._lat2 = None
        self._long2 = None
        self._alt2 = None
        self._utime = None
        self.parcing_errors = []
        self.keys_to_check = ['lat1', 'long1',
                              'alt1', 'lat2', 'long2', 'alt2', 'utime']
        self.parcing_steps = {'lat1': self.lat1,
                              'lat2': self.lat2,
                              'long1': self.long1,
                              'long2': self.long2,
                              'alt1': self.alt1,
                              'alt2': self.alt2,
                              'utime': self.utime}

    def check_value(self, name, value, good_values):
        if (type(value) is float):
            print('is_float')
            # check Krasnoyarsk diapazon
            if int(value) in range(*good_values):
                return True
            else:
                self.parcing_errors.append(
                    f'{name} value {value} is not in Krasnoyarsk, will be set None')
        else:
            self.parcing_errors.append(
                f'{name} value type {type(value)} is not float, will be set None')
        return False

    @property
    def lat1(self):
        return self._lat1

    @lat1.setter
    def lat1(self, value):
        if self.check_value('lat1', value, [55, 58]):
            self._lat1 = value
        else:
            self._lat1 = None

    @property
    def lat2(self):
        return self._lat2

    @lat2.setter
    def lat2(self, value):
        if self.check_value('lat2', value, [55, 58]):
            self._lat2 = value
        else:
            self._lat2 = None

    @property
    def long1(self):
        return self._long1

    @long1.setter
    def long1(self, value):
        if self.check_value('long1', value, [92, 94]):
            self._long1 = value
        else:
            self._long1 = None

    @property
    def long2(self):
        return self._long2

    @long2.setter
    def long2(self, value):
        if self.check_value('long2', value, [92, 94]):
            self._long2 = value
        else:
            self._long2 = None

    @property
    def alt1(self):
        return self._alt1

    @alt1.setter
    def alt1(self, value):
        if self.check_value('alt1', value, [100, 250]):
            self._alt1 = value
        else:
            self._alt1 = None

    @property
    def alt2(self):
        return self._alt2

    @alt2.setter
    def alt2(self, value):
        if self.check_value('alt2', value, [100, 250]):
            self._alt2 = value
        else:
            self._alt2 = None

    @property
    def utime(self):
        return self._utime

    @utime.setter
    def utime(self, value):
        if isinstance(value, numbers.Number):
            if value > 1716181200:  # May 2024
                self._utime = value
            else:
                self.parcing_errors.append(
                    f'utime value {value} must be greater 1716181200 - May 2024, will be set None')
        else:
            self.parcing_errors.append(
                f'utime value type {type(value)} is not number, will be set None')

    def read(self, message):
        if type(message) is dict:
            if all(key in message for key in self.keys_to_check):
                for key in self.keys_to_check:
                    print(key, message[key])
                    setattr(self, key, message[key])
            else:
                self.parcing_errors.append(
                    f'message keys {list(message.keys())} not equal {self.keys_to_check}')

        if any(var is None for var in (self.lat1, self.long1)):
            self.gps1 = self.GPS_OFF
        if any(var is None for var in (self.lat2, self.long2)):
            self.gps2 = self.GPS_OFF
        if self.alt1 is None:
            self.gps1_alt = self.GPS_OFF
        if self.alt2 is None:
            self.gps2_alt = self.GPS_OFF
        if self.utime is None:
            self.gps1 = self.gps2 = self.GPS_OFF


class MessageParcer():
    def __init__(self) -> None:
        pass

    def read_message(self, message: dict):
        return DetectionMessage()
