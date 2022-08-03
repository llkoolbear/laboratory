# ===============================================================================
#
# Name:       device.py
#
# Purpose:    A general device class
#
# Author:     Bear Bissen
#
# Created:    May 3, 2022
# Last Rev:   
# Edited by:
#
# License: MIT Open License
#
# ===============================================================================

from enum import Enum

class Device:

    class SettingLimit(Enum):
        MAX = "MAX"
        MIN = "MIN"

    class State(Enum):
        ON = "1"
        OFF = "0"

    def __init__(self):
        pass

    def enum_to_usage_str(self, enum):
        return f"{enum.__name__}.{{{str([m for m in enum.__members__])}".replace('[', '').replace(']', '').replace('\'', '') + '}'

    def parse_as(self, string, cast):
        try: 
            return cast(string)
        except ValueError:
            err_str = f'Failed to convert "{string}" to {cast}'
            raise ValueError(err_str)

    def check_enum(self, arg, type):
        if not isinstance(arg, type):
            raise TypeError(f'"{arg}" not a valid {type.__name__}! (usage: {self.enum_to_usage_str(type)})')

    def check_num(self, arg, units, min, max):

        if arg is self.SettingLimit.MIN:
            arg = min
        elif arg is self.SettingLimit.MAX:
            arg = max

        if not isinstance(arg, (int,float)):
            raise TypeError(f'"{arg}" not a valid number! (usage: {{int|float, {self.enum_to_usage_str(self.SettingLimit)}}})')

        if arg < min or arg > max:
            raise ValueError(f'"{arg}" out of range! (usage: {min}-{max} {units})')

    def check_int(self, arg, units, min, max):

        if not isinstance(arg, int):
            raise TypeError(f'"{arg}" not a valid int! (usage: int, {min}-{max} {units})')

        if arg < min or arg > max:
            raise ValueError(f'"{arg}" out of range! (usage: int, {min}-{max} {units})')

    def check_string(self, string):
        if not isinstance(string, str):
            raise TypeError(f'"{string}" not a valid String!')
