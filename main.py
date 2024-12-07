import ctypes
import random
import tkinter as tk

from PIL import Image, ImageTk


class ClickableCookie:
    def __init__(self, on_click, screen_width, usable_height):
        # Create cookie window
        self.window = tk.Toplevel()
        self.window.title("Cookie")
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        self.window.wm_attributes("-transparentcolor", self.window["bg"])

        # Set random position
        window_size = random.randint(75, 150)
        x = random.randint(0, screen_width - window_size)
        y = random.randint(0, usable_height - window_size)
        self.window.geometry(f"{window_size}x{window_size}+{x}+{y}")

        # Create cookie button
        self.cookie_image = Image.open("cookie.png")
        self.cookie_image = self.cookie_image.resize((int(0.9 * window_size), int(0.9 * window_size)))
        self.cookie_image = self.cookie_image.rotate(random.randint(0, 360))
        self.cookie_image = ImageTk.PhotoImage(self.cookie_image, master=self.window)

        self.button = tk.Button(
            self.window,
            command=lambda: self.clicked(on_click),
            image=self.cookie_image,
            borderwidth=0,
            highlightthickness=0,
        )
        self.button.pack(fill=tk.BOTH, expand=True)
        self.button.configure(bg=self.window["bg"])

        # Despawn cookie after a random time between 5 to 10 seconds
        self.window.after(random.randint(6000, 10000), self.destroy_animation)

    def clicked(self, callback):
        callback()
        self.window.after(0, self.destroy_animation)

    def destroy_animation(self):
        for size in range(self.window.winfo_width(), 0, -20):
            x = self.window.winfo_x() + (self.window.winfo_width() - size) // 2
            y = self.window.winfo_y() + (self.window.winfo_height() - size) // 2
            self.window.geometry(f"{size}x{size}+{x}+{y}")
            self.window.update()
            self.window.after(10)
        self.window.destroy()


class GameWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Cookie Clicker")
        self.root.geometry("200x30+0+0")

        # Screen setup
        user32 = ctypes.windll.user32
        self.screen_width = user32.GetSystemMetrics(0)
        self.screen_height = user32.GetSystemMetrics(1)
        self.usable_height = self.screen_height - user32.GetSystemMetrics(15)

        # Score setup
        self.frenzy = False
        self.score = self.get_score()

        # Taskbar
        self.taskbar = tk.Frame(self.root, bg="black", height=30)
        self.taskbar.pack(fill=tk.X, side=tk.TOP)

        # Close button
        close_button = tk.Button(self.taskbar, text="X", bg="red", fg="white", command=self.root.destroy)
        close_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Score label
        self.score_label = tk.Label(self.taskbar, text=f"Score: {self.score}", bg="black", fg="white")
        self.score_label.pack(side=tk.LEFT, padx=10)

        # Start spawning
        self.spawn_cookie()

    def cookie_clicked(self):
        # Update score
        self.score += 1
        self.score_label.config(text=f"Score: {self.score}")
        self.set_score(self.score)

        if random.randint(1, 100) == 1:
            self.start_frenzy()

    def start_frenzy(self):
        self.frenzy = True
        self.spawn_cookie()
        self.root.after(random.randint(8000, 16000), self.end_frenzy)

    def end_frenzy(self):
        self.frenzy = False

    def spawn_cookie(self):
        ClickableCookie(self.cookie_clicked, self.screen_width, self.usable_height)
        time_after = random.randint(500, 1500) if self.frenzy else random.randint(36000, 360000)
        self.root.after(time_after, self.spawn_cookie)

    def set_score(self, score):
        with open("score.txt", "w") as file:
            file.write(str(score))

    def get_score(self):
        try:
            with open("score.txt", "r") as file:
                return int(file.read())
        except FileNotFoundError:
            return 0


# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = GameWindow(root)
    root.mainloop()
