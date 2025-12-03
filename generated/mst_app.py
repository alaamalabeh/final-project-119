import random
import tkinter as tk
from tkinter import messagebox

class ScaleTrainer:
    def __init__(self, root):
        """Initialize the main window and scale trainer attributes."""
        self.root = root
        self.root.title("Music Scale Trainer")
        self.difficulty = 1  # Default difficulty level
        self.scales = ['C', 'D', 'E', 'F', 'G', 'A', 'B']  # Basic scales
        self.current_scale = ''
        self.score = 0
        self.attempts = 0
        
        # Create UI elements
        self.label = tk.Label(root, text="Welcome to the Music Scale Trainer!", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.scale_label = tk.Label(root, text="", font=("Helvetica", 14))
        self.scale_label.pack(pady=10)

        self.user_input = tk.Entry(root)
        self.user_input.pack(pady=10)

        self.check_button = tk.Button(root, text="Check Scale", command=self.check_scale)
        self.check_button.pack(pady=5)

        self.difficulty_label = tk.Label(root, text="Select Difficulty (1-3):")
        self.difficulty_label.pack(pady=5)

        self.difficulty_scale = tk.Scale(root, from_=1, to=3, orient=tk.HORIZONTAL, command=self.update_difficulty)
        self.difficulty_scale.pack(pady=5)

        self.score_label = tk.Label(root, text="Score: 0", font=("Helvetica", 14))
        self.score_label.pack(pady=10)

        self.next_scale()

    def next_scale(self):
        """Generate the next scale for the user to identify."""
        self.current_scale = random.choice(self.scales)
        self.scale_label.config(text=self.current_scale)

    def check_scale(self):
        """Check the user's input against the current scale."""
        user_answer = self.user_input.get().strip().upper()
        self.attempts += 1
        
        if user_answer == self.current_scale:
            self.score += self.difficulty
            messagebox.showinfo("Correct!", f"You identified the scale {self.current_scale} correctly!")
        else:
            messagebox.showerror("Incorrect!", f"The correct scale was {self.current_scale}.")

        self.score_label.config(text=f"Score: {self.score}")
        self.user_input.delete(0, tk.END)
        self.next_scale()

    def update_difficulty(self, value):
        """Update the difficulty level based on user selection."""
        self.difficulty = int(value)

def main():
    """Run the Music Scale Trainer application."""
    root = tk.Tk()
    app = ScaleTrainer(root)
    root.mainloop()

if __name__ == "__main__":
    main()