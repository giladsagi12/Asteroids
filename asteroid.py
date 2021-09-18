class Asteroid:
    """this class represents the asteroids in the game"""
    def __init__(self, location_x, speed_x, location_y, speed_y, size):
        self.__location_x = location_x
        self.__speed_x = speed_x
        self.__location_y = location_y
        self.__speed_y = speed_y
        self.__size = size
        self.__direction = 0
        self.__destroyed = False

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

    def size(self):
        return self.__size

    def change_size(self):
        self.__size -= 1

    def update_location(self, x, y):
        self.__location_x = x
        self.__location_y = y

    def radius(self):
        return self.__size * 10 - 5

    def has_intersection(self, obj):
        """
        :param obj: the ship or a torpedo
        :returns: True if there was an intersection
         between the asteroid and the object according to the the given formula,
         False otherwise."""
        distance = ((obj.x() - self.__location_x)**2 + (obj.y() - self.__location_y)**2)**0.5
        if distance <= self.radius() + obj.radius():
            return True
        return False

    def change_speed_after_collision(self, torpedo):
        """changes the speed of the asteroid if collided with
         a torpedo by the given formula."""
        speed_x = (torpedo.speed_x() + self.__speed_x)/((self.__speed_x**2 + self.__speed_y**2)**0.5)
        speed_y = (torpedo.speed_y() + self.__speed_y)/((self.__speed_x**2 + self.__speed_y**2)**0.5)
        self.__speed_x, self.__speed_y = speed_x, speed_y

    def change_speed_sign(self):
        self.__speed_x *= -1
        self.__speed_y *= -1

    def change_status(self):
        self.__destroyed = True

    def destroyed(self):
        return self.__destroyed