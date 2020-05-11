import arcade
from random import randrange
import tkinter as tk

root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
screen_title = "want coin"


class PickUpCoin(arcade.Window):
    def __init__(self):
        super().__init__(screen_width, screen_height, screen_title, True)

        self.coins_number = 50
        self.coin_scale = 1 * (screen_width / 1920)
        self.coins_list = arcade.SpriteList()
        for i in range(self.coins_number):
            coin_sprite = arcade.Sprite("gold_1.png", self.coin_scale)
            coin_sprite.center_x = randrange(50, screen_width - 50)
            coin_sprite.center_y = randrange(50, screen_height - 50)
            coin_sprite.change_x = randrange(-10, 11)
            coin_sprite.change_y = randrange(-10, 11)
            self.coins_list.append(coin_sprite)

        self.movement_speed = 15
        self.player_scale = 0.7 * (screen_width / 1920)
        self.player_sprite = arcade.Sprite("slimeBlock.png", self.player_scale)
        self.player_sprite.center_y = screen_height//2
        self.player_sprite.center_x = screen_width//2
        self.player_sprite.change_y = 0
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        self.score = 0
        self.time = 0
        self.highest_score = []
        self.set_mouse_visible(False)

        self.left_pressed = False
        self.right_pressed = False
        self.down_pressed = False
        self.up_pressed = False

        self.acceleration = 0.3
        self.friction = 0.97

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            exit()
        if symbol == arcade.key.UP:
            self.up_pressed = True
        if symbol == arcade.key.DOWN:
            self.down_pressed = True
        if symbol == arcade.key.RIGHT:
            self.right_pressed = True
        if symbol == arcade.key.LEFT:
            self.left_pressed = True

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            self.up_pressed = False
        if symbol == arcade.key.DOWN:
            self.down_pressed = False
        if symbol == arcade.key.RIGHT:
            self.right_pressed = False
        if symbol == arcade.key.LEFT:
            self.left_pressed = False

    def on_draw(self):
        arcade.set_background_color(arcade.color.ELECTRIC_BLUE)
        arcade.start_render()
        self.player_list.draw()
        self.coins_list.draw()
        if self.score == self.coins_number:
            arcade.draw_text(f"Your Score: {round(self.highest_score[-1], 3)}.\n"
                             f"Press ALT+F4 to close.",
                             660, 540, arcade.color.BLACK, 40, 600, "center")

    def on_update(self, delta_time=1/60):

        if (self.left_pressed and not self.right_pressed
                and abs(self.player_sprite.change_x) <= abs(self.movement_speed)):
            self.player_sprite.change_x -= self.acceleration
        elif (not self.left_pressed and self.right_pressed
              and abs(self.player_sprite.change_x) <= abs(self.movement_speed)):
            self.player_sprite.change_x += self.acceleration

        if (self.up_pressed and not self.down_pressed
                and abs(self.player_sprite.change_y) <= abs(self.movement_speed)):
            self.player_sprite.change_y += self.acceleration
        elif (not self.up_pressed and self.down_pressed
              and abs(self.player_sprite.change_y) <= abs(self.movement_speed)):
            self.player_sprite.change_y -= self.acceleration

        self.player_sprite.change_x *= self.friction
        self.player_sprite.change_y *= self.friction

        if self.player_sprite.center_x < 0 + 50 * self.player_scale:
            self.player_sprite.center_x = 0 + 50 * self.player_scale
        elif self.player_sprite.center_x > screen_width - 50 * self.player_scale:
            self.player_sprite.center_x = screen_width - 50 * self.player_scale
        if self.player_sprite.center_y > screen_height - 30 * self.player_scale:
            self.player_sprite.center_y = screen_height - 30 * self.player_scale
        elif self.player_sprite.center_y < 0 + 70 * self.player_scale:
            self.player_sprite.center_y = 0 + 70 * self.player_scale

        self.player_list.update()

        self.coins_list.update()
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coins_list)
        for i in self.coins_list:
            if i.center_x >= screen_width and i.change_x > 0:
                i.change_x *= -1
            elif i.center_x <= 0 and i.change_x < 0:
                i.change_x *= -1
            if i.center_y >= screen_height and i.change_y > 0:
                i.change_y *= -1
            elif i.center_y <= 0 and i.change_y < 0:
                i.change_y *= -1

        for i in coin_hit_list:
            i.remove_from_sprite_lists()
            self.score += 1
        self.time += 1/60
        if self.score == self.coins_number:
            self.highest_score.append(self.score/self.time)
            self.highest_score.sort()


def main():
    PickUpCoin()
    arcade.run()


if __name__ == "__main__":
    main()
