from project.messaging import DetectionMessage, GpsMessage


class ChangeMessage():
    def __init__(self):
        self.workload_change = None
        self.level_change = None
        self.update_azimuth = None
        self.update_container_number = None
        self.message = None

    def set_workload_change(self, workload_change):
        pass


class SubsystemsUpdateCodes():
    def __init__(self):
        self.codes = ChangeCodes()
        self._message = {'workload': None,
                         'level': None,
                         'azimuth': None,
                         'container_number': None}

    @property
    def message(self):
        for key in self._message.keys():
            assert self._message[key] in [
                self.codes.NO_CHANGE, self.codes.CHANGED], f"{key} change must be of type ChangeCodes"

        return self._message

    @message.setter
    def workload_change(self, value):
        self._message['workload'] = value

    @message.setter
    def level_change(self, value):
        self._message['level'] = value

    @message.setter
    def azimuth_changed(self, value):
        self._message['azimuth'] = value

    @message.setter
    def container_number_changed(self, value):
        self._message['container_number'] = value


class ChangeCodes:
    NO_CHANGE = 0
    CHANGED = 1
    ERROR = 2


class Fork():
    def __init__(self):
        self.change_codes = ChangeCodes()
        self.update_codes = SubsystemsUpdateCodes()
        pass

    def update_subsystems(self, det_message: DetectionMessage, gps_message: GpsMessage):
        assert type(
            det_message) is DetectionMessage, "det_message must be of type DetectionMessage"
        assert type(
            gps_message) is GpsMessage, "gps_message must be of type GpsMessage"

        self.update_codes.workload_change = self.update_workload(det_message)
        self.update_codes.level_change = self.update_level(
            det_message, gps_message)
        self.update_codes.azimuth_changed = self.update_azimuth(
            det_message, gps_message)
        self.update_codes.container_number_changed = self.update_container_number(
            det_message)

        return self.update_codes.message

    def update_workload(self, det_message: DetectionMessage):
        return self.change_codes.NO_CHANGE

    def update_azimuth(self, det_message: DetectionMessage, gps_message: GpsMessage):
        return self.change_codes.NO_CHANGE

    def update_level(self, det_message: DetectionMessage, gps_message: GpsMessage):
        return self.change_codes.NO_CHANGE

    def update_container_number(self, det_message: DetectionMessage):
        return self.change_codes.NO_CHANGE

    def make_action(self, subsystems_change):
        
        pass

    def make_step_report(self, action_report, subsystems_change):
        pass

    def make_step(self, det_message: DetectionMessage, gps_message: GpsMessage):

        assert type(
            det_message) is DetectionMessage, "det_message must be of type DetectionMessage"
        assert type(
            gps_message) is GpsMessage, "gps_message must be of type GpsMessage"

        subsystems_change = self.update_subsystems(det_message, gps_message)
        action_report = self.make_action(subsystems_change)

        step_result = self.make_step_report(action_report, subsystems_change)
        return step_result
