from screen import Screen
from ship import Ship
from torpedo import Torpedo
from asteroid import Asteroid
import sys
import random
import math

DEFAULT_ASTEROIDS_NUM = 5
ASTEROID_SIZE = 3
POINTS = {3: 20, 2: 50, 1: 100}


class GameRunner:
    """this class represents the game with all the objects included in it"""

    def __init__(self, asteroids_amount):
        self.__screen = Screen()
        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__asteroids_amount = asteroids_amount
        self.__asteroids = []
        self.__torpedos = []
        self.__score = 0
        self.__objects = []

        x = random.randint(self.__screen_min_x, self.__screen_max_x)
        y = random.randint(self.__screen_min_y, self.__screen_max_y)
        self.__ship = Ship(x, 0, y, 0, 0)

        self.add_asteroids()

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You should not to change this method!
        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        """
        runs a single turn of the game.
        """
        if self.check_end():
            self.__screen.end_game()
            sys.exit()

        self.draw_objects()
        self.move_objects()
        self.check_user_actions()
        self.check_collision()

    def move_objects(self):
        """adds all objects in the game to a list and updates
        their locations by the given formula."""

        self.__objects = []
        self.__objects += self.__asteroids
        self.__objects += self.__torpedos
        self.__objects.append(self.__ship)
        for obj in self.__objects:
            delta_x = self.__screen_max_x - self.__screen_min_x
            delta_y = self.__screen_max_y - self.__screen_min_y
            new_x = self.__screen_min_x + (obj.x() + obj.speed_x()
                                           - self.__screen_min_x) % delta_x
            new_y = self.__screen_min_y + (obj.y() + obj.speed_y()
                                           - self.__screen_min_y) % delta_y
            obj.update_location(new_x, new_y)

    def add_asteroids(self):
        """adds the number of asteroids asked in the __init__ function
         to the __init__ asteroids list, and register them in the screen"""

        for i in range(self.__asteroids_amount):
            collision = True
            while collision:
                x = random.randint(self.__screen_min_x, self.__screen_max_x)
                y = random.randint(self.__screen_min_y, self.__screen_max_y)
                speed_x = random.randint(1, 4) * random.choice([1, -1])
                speed_y = random.randint(1, 4) * random.choice([1, -1])
                asteroid = Asteroid(x, speed_x, y, speed_y, ASTEROID_SIZE)
                if not asteroid.has_intersection(self.__ship):
                    collision = False
            self.__asteroids.append(asteroid)
            self.__screen.register_asteroid(asteroid, ASTEROID_SIZE)

    def check_collision(self):
        """checks for collision between a torpedo and the ship or an asteroid.
        reduce the ship's life if collided with an asteroid, and destroys the asteroid.
        """
        for asteroid in self.__asteroids:
            if asteroid.has_intersection(self.__ship):
                self.__screen.show_message("collision", "ship collided with asteroid")
                self.__screen.remove_life()
                asteroid.change_status()
                self.__screen.unregister_asteroid(asteroid)
                self.__ship.remove_life()
            else:
                for torpedo in self.__torpedos:
                    if asteroid.has_intersection(torpedo):
                        self.torpedo_collision(asteroid, torpedo)
        self.remove_destroyed_asteroids()

    def torpedo_collision(self, asteroid, torpedo):
        """in case of collision between a torpedo and an asteroid, the function updates the
        score by the size of the asteroid, and removes the torpedo.
         if the asteroid size > 1 the asteroid splits to two asteroid with
         size smaller by 1. if asteroid size is 1, removes asteroid from screen. """

        self.__score += POINTS[asteroid.size()]
        self.__screen.set_score(self.__score)
        self.__screen.unregister_torpedo(torpedo)
        self.__torpedos.remove(torpedo)
        if asteroid.size() > 1:
            asteroid.change_size()
            asteroid.change_speed_after_collision(torpedo)
            new_asteroid = Asteroid(asteroid.x(), asteroid.speed_x(), asteroid.y(), asteroid.speed_y(), asteroid.size())
            new_asteroid.change_speed_sign()
            self.__asteroids.append(new_asteroid)
            self.__screen.unregister_asteroid(asteroid)
            self.__screen.register_asteroid(asteroid, asteroid.size())
            self.__screen.register_asteroid(new_asteroid, new_asteroid.size())
        else:
            asteroid.change_status()
            self.__screen.unregister_asteroid(asteroid)

    def check_user_actions(self):
        """checks what key was pressed by the user and
        calls the relevant function accordingly. limits the amount of torpedos to 10"""
        if self.__screen.is_left_pressed():
            self.__ship.change_direction("left")
        if self.__screen.is_right_pressed():
            self.__ship.change_direction("right")
        if self.__screen.is_up_pressed():
            self.__ship.accelerate()
        if self.__screen.is_space_pressed():
            if len(self.__torpedos) < 10:
                self.create_torpedo()

    def create_torpedo(self):
        """sets the speed of the torpedo by the formula which includes
         the speed of the ship. creates a new object of class
         Torpedo with that speed and with the ships location and direction"""
        torpedo_speed_x = self.__ship.speed_x() \
                          + 2 * math.cos(math.radians(self.__ship.direction()))
        torpedo_speed_y = self.__ship.speed_y() \
                          + 2 * math.sin(math.radians(self.__ship.direction()))
        torpedo = Torpedo(self.__ship.x(), torpedo_speed_x,
                          self.__ship.y(), torpedo_speed_y,
                          self.__ship.direction())
        self.__torpedos.append(torpedo)
        self.__screen.register_torpedo(torpedo)

    def check_end(self):
        """checks all possibilities of the game to be finished"""
        if self.__screen.should_end():
            self.__screen.show_message("Game Over", "The user quit.")
            return True
        elif self.__ship.lives() == 0:
            self.__screen.show_message("Game Over", "Ship destroyed")
            return True
        elif not self.__asteroids:
            self.__screen.show_message("You won!", "All asteroids destroyed.")
            return True
        return False

    def draw_objects(self):
        # draw ship:
        self.__screen.draw_ship(self.__ship.x(), self.__ship.y(), self.__ship.direction())

        # draw each asteroid:
        for asteroid in self.__asteroids:
            self.__screen.draw_asteroid(asteroid, asteroid.x(), asteroid.y())

        # draw each torpedo:
        for torpedo in self.__torpedos:
            self.__screen.draw_torpedo(torpedo, torpedo.x(), torpedo.y(), torpedo.direction())
            # set time for torpedo:
            torpedo.update_count()
            if torpedo.count() == 200:
                self.__screen.unregister_torpedo(torpedo)
                self.__torpedos.remove(torpedo)

    def remove_destroyed_asteroids(self):
        self.__asteroids = [asteroid for asteroid in self.__asteroids if not asteroid.destroyed()]


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
