RADIUS = 4

class Torpedo:
    """this class represents the torpedos in the game"""

    def __init__(self, location_x, speed_x, location_y, speed_y, direction):
        self.__location_x = location_x
        self.__speed_x = speed_x
        self.__location_y = location_y
        self.__speed_y = speed_y
        self.__direction = direction
        self.__radius = RADIUS
        self.__count = 0

    def radius(self):
        return self.__radius

    def x(self):
        return self.__location_x

    def y(self):
        return self.__location_y

    def speed_x(self):
        return self.__speed_x

    def speed_y(self):
        return self.__speed_y

    def direction(self):
        return self.__direction

    def update_location(self, x, y):
        self.__location_x = x
        self.__location_y = y

    def count(self):
        return self.__count

    def update_count(self):
        self.__count += 1