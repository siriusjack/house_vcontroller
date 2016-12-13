import re
from ._light import Light


class House():
    def __init__(self):
        self.__lights = [Light(i + 1) for i in range(3)]

    def turn_lights_on(self):
        for light in self.__lights:
            light.turn_on()

    def turn_lights_off(self):
        for light in self.__lights:
            light.turn_off()

    def listen(self, msg):
        if re.search(r'ぼっとらいとおん', msg):
            self.turn_lights_on()
        if re.search(r'ぼっとらいとおふ', msg):
            self.turn_lights_off()
