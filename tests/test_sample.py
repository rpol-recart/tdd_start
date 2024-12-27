import json
from project.messaging import MessageParcer
from project.messaging import DetectionMessage, GpsMessage
from project.core import Fork


def test_message_loader():
    pass


def test_read_message():
    mp = MessageParcer()
    with open('./tests/sample_messages/sample_message1.json', 'rb') as f:
        msg = json.load(f)
    message = mp.read_message(msg)
    assert type(message) is DetectionMessage


def test_update_subsystems_test1():
    '''
    Testing format message generated in fork.update_subsystems
    '''
    det = DetectionMessage()
    gps = GpsMessage()
    fork = Fork()
    subsystems_change = fork.update_subsystems(det, gps)
    assert type(subsystems_change) is dict and len(
        subsystems_change) == 4, 'subsystems_change must be a dict with 4 keys'
    for key in ['workload', 'level', 'azimuth', 'container_number']:
        assert key in subsystems_change.keys(
        ), f'{key} must be in subsystems_change message'


def test_gps_message1():
    '''
    Testing gps message
    '''
    messg = {
        "gps": {
            "lat1": 55.752220000000000000,
            "long1": 37.615560000000000000,
            "alt1": 150.000000000000000000,
            "lat2": 55.752220000000000000,
            "long2": 37.615560000000000000,
            "alt2": 150.000000000000000000,
            "utime": 1734670800
        }
    }
    gps = GpsMessage()
    gps.read(messg['gps'])
    assert len(gps.parcing_errors) == 2, 'parcing_errors must handle 2 errors'


def test_gps_message2():
    '''
    Testing gps message
    '''
    messg = {
        "gps": {
            "lat1": 55.752220000000000000,
            "long1": 92.615560000000000000,
            "alt1": 150.000000000000000000,
            "lat2": 55.752220000000000000,
            "long2": 93.615560000000000000,
            "alt2": 150.000000000000000000,
            "utime": -1
        }
    }
    gps = GpsMessage()
    gps.read(messg['gps'])
    assert len(
        gps.parcing_errors) == 1, 'parcing_errors must handle 1 errors utime not in diapazon'


def test_gps_message3():
    '''
    Testing gps message
    '''
    messg = {
        "gps": {
            "lat1": None,
            "long1": 92.615560000000000000,
            "alt1": -1,
            "lat2": -1,
            "long2": 93.615560000000000000,
            "alt2": None,
            "utime": -1
        }
    }
    gps = GpsMessage()
    gps.read(messg['gps'])
    assert len(
        gps.parcing_errors) == 5, 'parcing_errors must handle 1 errors utime not in diapazon'
    assert gps.utime is None, 'utime must be None'
    assert gps.lat1 is None, 'lat1 must be None'
    assert gps.lat2 is None, 'lat2 must be None'
    assert gps.long1 == 92.61556, 'long1 must be 92.61556'
    assert gps.alt1 is None, 'alt1 must be None'
    assert gps.alt2 is None, 'alt2 must be None'


def test_gps_message4():
    '''
    Testing gps message key names
    '''
    messg = {
        "gps": {
            "lat1": None,
            "long3": 92.615560000000000000,
            "alt1": -1,
            "lat2": -1,
            "long2": 93.615560000000000000,
            "alt2": None,
            "utime": -1
        }
    }
    gps = GpsMessage()
    gps.read(messg['gps'])
    assert len(
        gps.parcing_errors) == 1, '''parcing_errors must handle 1 errors 
                                    key not equal template 'lat1', 'long1',
                                    'alt1', 'lat2', 'long2', 'alt2', 'utime' 
                                    '''
    assert gps.utime is None, 'utime must be None'
    assert gps.lat1 is None, 'lat1 must be None'
    assert gps.lat2 is None, 'lat2 must be None'
    assert gps.long1 is None, 'long1 must be None'
    assert gps.alt1 is None, 'alt1 must be None'
    assert gps.alt2 is None, 'alt2 must be None'


def test_gps_message5():
    '''
    Testing gps message key names
    '''
    messg = {
        "gps": {
            "lat1": 55.752220000000000000,
            "long1": 92.615560000000000000,
            "alt1": 150.000000000000000000,
            "lat2": 55.752220000000000000,
            "long2": 93.615560000000000000,
            "alt2": 150.000000000000000000,
            "utime": -1
        }
    }
    gps = GpsMessage()
    gps.read(messg['gps'])
    assert gps.gps1 == gps.gps2 == gps.GPS_OFF, ' when utime incorrect gps1 and gps2 must be GPS_OFF'

    messg = {
        "gps": {
            "lat1": 55.752220000000000000,
            "long1": 92.615560000000000000,
            "alt1": 150.000000000000000000,
            "lat2": 37.752220000000000000,  # incorrect lat2
            "long2": 93.615560000000000000,
            "alt2": 150.000000000000000000,
            "utime": 1734670800
        }
    }
    gps = GpsMessage()
    gps.read(messg['gps'])  
    assert gps.gps1 == gps.GPS_ON
    assert gps.gps2 == gps.GPS_OFF, ' when lat2 incorrect  gps2 must be GPS_OFF'
