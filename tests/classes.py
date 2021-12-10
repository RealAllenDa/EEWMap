"""
 EEWMap - Tests - Classes
 The classes for all tests, including:
    - Requests Response
        - Normal
        - Status Error
        - Text Empty
        - Error
    - Intensity Dictionary
        - Normal
        - Intensity Abnormal
        - Area Abnormal
    - Tsunami Dictionary
        - Normal
        - Grade Abnormal
        - Area Abnormal
"""


class _DemoResponse:
    """The base response model for requests."""
    status_code = 0
    text = ""


class DemoRespOK(_DemoResponse):
    """The normal response."""
    status_code = 200
    text = "TEST"


class DemoRespStatusError(_DemoResponse):
    """The response with http error code."""
    status_code = 404
    text = "TEST"


class DemoRespTextEmpty(_DemoResponse):
    """The response with empty text."""
    status_code = 200
    text = ""


class DemoRespError(_DemoResponse):
    """The abnormal response."""
    status_code = 404
    text = ""


class DemoNormIntensityJson:
    """The normal intensity JSON."""
    area_names = ["留萌地方南部"]
    area_intensities = {
        "留萌地方南部": {
            "name": "留萌地方南部",
            "intensity": "5+",
            "longitude": 123,
            "latitude": 123,
            "is_area": True
        }
    }
    intensity_color = "#FF7800"


class DemoIntAbnIntensityJson(DemoNormIntensityJson):
    """The intensity JSON with abnormal intensity."""
    area_names = ["石狩地方北部"]
    area_intensities = {
        "石狩地方北部": {
            "name": "石狩地方北部",
            "intensity": "TEST",
            "longitude": 123,
            "latitude": 123,
            "is_area": True
        }
    }
    intensity_color = "#666666"


class DemoAreaAbnIntensityJson(DemoNormIntensityJson):
    """The intensity JSON with abnormal area."""
    area_names = ["12345"]
    area_intensities = {
        "12345": {
            "name": "12345",
            "intensity": "5+",
            "longitude": 123,
            "latitude": 123,
            "is_area": True
        }
    }


class DemoNormTsunamiJson:
    """The normal tsunami JSON."""
    area_names = ["福岡県日本海沿岸"]
    area_grades = {
        "福岡県日本海沿岸": {
            "name": "福岡県日本海沿岸",
            "immediate": True,
            "grade": "MajorWarning"
        }
    }
    area_color = "#AA28AA"


class DemoAreaAbnTsunamiJson(DemoNormTsunamiJson):
    """The tsunami JSON with abnormal area."""
    area_names = ["TEST"]
    area_grades = {
        "TEST": {
            "name": "TEST",
            "immediate": True,
            "grade": "MajorWarning"
        }
    }


class DemoGradeAbnTsunamiJson(DemoNormTsunamiJson):
    """The tsunami JSON with abnormal grade."""
    area_names = ["オホーツク海沿岸"]
    area_grades = {
        "オホーツク海沿岸": {
            "name": "オホーツク海沿岸",
            "immediate": True,
            "grade": "Unknown"
        }
    }
