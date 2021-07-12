"""
 EEWMap - API - Tsunami
 The tsunami information from JMA XML, including:
    - Tsunami Expected Arrival Time Information
    - Tsunami Watch Information
 Note that tsunami watch information also contains tsunami expected arrival time information,
  so when tsunami watch information is refreshed, the expected arrival time information also refreshes.
 This module is responsible for:
    - Tsunami Detailed Arrival Time Information
        - Tsunami Areas
        - Tsunami Grade
        - Tsunami Expected Arrival Time
        - Tsunami Expected Height
    - Tsunami Watch Information
        - All the watch information
"""
from .get_jma_tsunami import get_jma_tsunami
