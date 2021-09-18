import math
SHIP_RADIUS = 1
LIVES = 3
DIRECTION_CHANGE = 7

class Ship:
    """this class represents the ship of the game"""
    def __init__(self, location_x, speed_x, location_y, speed_y, direction):
        self.__location_x = location_x
        self.__speed_x = speed_x
        self.__location_y = location_y
        self.__speed_y = speed_y
        self.__direction = direction
        self.__lives = LIVES

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

    def change_direction(self, movekey):
        """changes the direction of the ship by the movekey"""
        if movekey == "right":
            self.__direction -= DIRECTION_CHANGE
        elif movekey == "left":
            self.__direction += DIRECTION_CHANGE

    def accelerate(self):
        """changes the speed of the ship by the given formula"""
        new_speed_x = self.__speed_x + math.cos(math.radians(self.__direction))
        new_speed_y = self.__speed_y + math.sin(math.radians(self.__direction))
        self.__speed_x = new_speed_x
        self.__speed_y = new_speed_y

    def radius(self):
        return SHIP_RADIUS

    def lives(self):
        return self.__lives

    def remove_life(self):
        self.__lives -= 1