from rest_framework.exceptions import APIException


class ScheduleVisitStatusException(APIException):
    status_code = 400
    default_code = "status_invalid"
