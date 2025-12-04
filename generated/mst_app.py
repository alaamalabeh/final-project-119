import tkinter as tk
import random
import time

class MusicScaleTrainer:
    def __init__(self, master):
        """Initialize the main window and attributes for the trainer."""
        self.master = master
        self.master.title("Music Scale Trainer")
        self.difficulty_level = 1
        self.scales = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        self.progress = []
        
        # Create UI elements
        self.label = tk.Label(master, text="Select Difficulty Level:")
        self.label.pack()
        
        self.level_var = tk.IntVar(value=self.difficulty_level)
        self.level1 = tk.Radiobutton(master, text="Easy", variable=self.level_var, value=1, command=self.set_difficulty)
        self.level2 = tk.Radiobutton(master, text="Medium", variable=self.level_var, value=2, command=self.set_difficulty)
        self.level3 = tk.Radiobutton(master, text="Hard", variable=self.level_var, value=3, command=self.set_difficulty)
        self.level1.pack()
        self.level2.pack()
        self.level3.pack()
        
        self.start_button = tk.Button(master, text="Start Exercise", command=self.start_exercise)
        self.start_button.pack()
        
        self.scale_label = tk.Label(master, text="")
        self.scale_label.pack()
        
        self.answer_entry = tk.Entry(master)
        self.answer_entry.pack()
        
        self.submit_button = tk.Button(master, text="Submit Answer", command=self.check_answer)
        self.submit_button.pack()
        
        self.feedback_label = tk.Label(master, text="")
        self.feedback_label.pack()
        
        self.progress_label = tk.Label(master, text="")
        self.progress_label.pack()
        
        self.current_scale = ""
        
    def set_difficulty(self):
        """Set the difficulty level based on user selection."""
        self.difficulty_level = self.level_var.get()
        self.feedback_label.config(text=f"Difficulty set to level {self.difficulty_level}.")
        
    def start_exercise(self):
        """Start the scale exercise by generating a random scale."""
        self.progress.clear()
        self.generate_scale()
        
    def generate_scale(self):
        """Generate a random scale based on the selected difficulty level."""
        if self.difficulty_level == 1:
            self.current_scale = random.choice(self.scales)
        elif self.difficulty_level == 2:
            self.current_scale = random.choice(self.scales) + " Major"
        else:
            self.current_scale = random.choice(self.scales) + " Minor"
        
        self.scale_label.config(text=f"Play the scale: {self.current_scale}")
        self.answer_entry.delete(0, tk.END)
        self.feedback_label.config(text="")
        
    def check_answer(self):
        """Check the user's answer against the expected scale."""
        user_answer = self.answer_entry.get().strip()
        if user_answer.lower() == self.current_scale.lower():
            self.feedback_label.config(text="Correct!")
            self.progress.append(True)
        else:
            self.feedback_label.config(text=f"Wrong! The correct answer was: {self.current_scale}")
            self.progress.append(False)
        
        self.update_progress()
        self.generate_scale()
        
    def update_progress(self):
        """Update the progress label to show the number of correct answers."""
        correct_count = sum(self.progress)
        total_count = len(self.progress)
        self.progress_label.config(text=f"Progress: {correct_count}/{total_count}")

def main():
    """Main function to start the Music Scale Trainer application."""
    root = tk.Tk()
    app = MusicScaleTrainer(root)
    root.mainloop()

if __name__ == "__main__":
    main()