import tkinter as tk
import random

WIDTH = 800
HEIGHT = 400
GROUND_Y = HEIGHT - 50

GRAVITY = 2
JUMP_VELOCITY = -23
INITIAL_OBSTACLE_WIDTH = 30
INITIAL_OBSTACLE_HEIGHT = 50
INITIAL_OBSTACLE_SPEED = 8

class TRexGame:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack()

        self.torso = self.canvas.create_rectangle(80, GROUND_Y - 50, 110, GROUND_Y - 10, fill="purple")
        self.head = self.canvas.create_rectangle(85, GROUND_Y - 70, 105, GROUND_Y - 50, fill="gold")
        self.left_arm = self.canvas.create_rectangle(70, GROUND_Y - 45, 80, GROUND_Y - 25, fill="gold")
        self.right_arm = self.canvas.create_rectangle(110, GROUND_Y - 45, 120, GROUND_Y - 25, fill="gold")
        self.thanos_parts = [self.torso, self.head, self.left_arm, self.right_arm]

        self.thanos_y = GROUND_Y - 70
        self.is_jumping = False
        self.jump_velocity = 0
        self.jump_count = 0

        self.score = 0
        self.score_text = self.canvas.create_text(10, 10, anchor="nw", font=("Arial", 16), text="Score: 0")
        self.power_text = None
        self.final_form_text = None

        self.obstacles = []
        self.obstacle_speed = INITIAL_OBSTACLE_SPEED
        self.obstacle_width = INITIAL_OBSTACLE_WIDTH
        self.obstacle_height = INITIAL_OBSTACLE_HEIGHT
        self.powered_up = False
        self.final_form = False
        self.spawn_obstacle()

        root.bind("<space>", self.jump)
        self.update()

    def jump(self, event):
        if not self.is_jumping:
            self.jump_velocity = JUMP_VELOCITY
            self.is_jumping = True
            self.jump_count += 1

            if self.jump_count == 15 and not self.powered_up:
                self.activate_power()

    def activate_power(self):
        self.powered_up = True
        self.score += 100
        self.obstacle_speed *= 2
        self.obstacle_width += 20
        self.obstacle_height += 20
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
        self.power_text = self.canvas.create_text(WIDTH // 2, 50,
                                                  text="💥 POWER UNLEASHED 💥",
                                                  fill="purple", font=("Arial", 24))

    def activate_final_form(self):
        self.final_form = True
        self.obstacle_speed *= 1.5
        self.final_form_text = self.canvas.create_text(WIDTH // 2, 90,
                                                       text="💀 FINAL FORM 💀",
                                                       fill="red", font=("Arial", 24))

    def spawn_obstacle(self):
        x = WIDTH + random.randint(0, 200)
        y = GROUND_Y
        obs = self.canvas.create_rectangle(x, y - self.obstacle_height,
                                           x + self.obstacle_width, y,
                                           fill="red")
        self.obstacles.append(obs)
        self.root.after(random.randint(1500, 2500), self.spawn_obstacle)

    def move_thanos(self):
        self.thanos_y += self.jump_velocity
        self.jump_velocity += GRAVITY
        if self.thanos_y >= GROUND_Y - 70:
            self.thanos_y = GROUND_Y - 70
            self.is_jumping = False
            self.jump_velocity = 0

        y = self.thanos_y
        self.canvas.coords(self.head, 85, y, 105, y + 20)
        self.canvas.coords(self.torso, 80, y + 20, 110, y + 60)
        self.canvas.coords(self.left_arm, 70, y + 25, 80, y + 45)
        self.canvas.coords(self.right_arm, 110, y + 25, 120, y + 45)

    def check_collision(self):
        tx1, ty1, tx2, ty2 = self.canvas.bbox(self.torso)
        for obs in self.obstacles:
            x1, y1, x2, y2 = self.canvas.coords(obs)
            if tx1 < x2 and tx2 > x1 and ty2 > y1:
                self.game_over()
                return True
        return False

    def update(self):
        if self.is_jumping:
            self.move_thanos()

        for obs in self.obstacles[:]:
            self.canvas.move(obs, -self.obstacle_speed, 0)
            x1, y1, x2, y2 = self.canvas.coords(obs)

            if x2 < 0:
                self.canvas.delete(obs)
                self.obstacles.remove(obs)
                self.score += 1
                self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

                if self.score >= 125 and not self.final_form:
                    self.activate_final_form()

        if self.check_collision():
            return

        self.root.after(30, self.update)

    def game_over(self):
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="GAME OVER",
                                font=("Arial", 32), fill="black")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Thanos Runner: Power Mode")
    game = TRexGame(root)
    root.mainloop()