import tkinter as tk
from tkinter import messagebox, font
import random
import json
import os

class RPSGameGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🏆 Rock Paper Scissors Championship")
        self.root.geometry("800x700")
        self.root.configure(bg="#2C3E50")
        
        # Game state
        self.user_score = 0
        self.computer_score = 0
        self.round_num = 1
        self.rounds_history = []
        
        # Load stats
        self.stats = self.load_stats()
        
        # Emojis
        self.emojis = {'rock': '🪨', 'paper': '📄', 'scissors': '✂️'}
        
        self.create_widgets()
    
    def load_stats(self):
        """Load statistics from file"""
        try:
            if os.path.exists("rps_stats.json"):
                with open("rps_stats.json", 'r') as f:
                    return json.load(f)
        except:
            pass
        return {
            "matches_won": 0,
            "matches_lost": 0,
            "total_matches": 0,
            "rounds_won": 0,
            "rounds_lost": 0,
            "rounds_tied": 0,
            "total_rounds": 0
        }
    
    def save_stats(self):
        """Save statistics to file"""
        try:
            with open("rps_stats.json", 'w') as f:
                json.dump(self.stats, f, indent=2)
        except:
            pass
    
    def create_widgets(self):
        """Create all GUI elements"""
        # Title
        title_font = font.Font(family="Arial", size=28, weight="bold")
        title = tk.Label(self.root, text="🏆 Rock Paper Scissors Championship 🏆",
                        font=title_font, bg="#2C3E50", fg="#ECF0F1")
        title.pack(pady=20)
        
        # Score display
        score_frame = tk.Frame(self.root, bg="#34495E", relief=tk.RAISED, bd=3)
        score_frame.pack(pady=10, padx=50, fill=tk.X)
        
        score_font = font.Font(family="Arial", size=18, weight="bold")
        self.score_label = tk.Label(score_frame, 
                                    text=f"You: {self.user_score}  |  Round: {self.round_num}  |  Computer: {self.computer_score}",
                                    font=score_font, bg="#34495E", fg="#ECF0F1", pady=15)
        self.score_label.pack()
        
        # Result display area
        result_frame = tk.Frame(self.root, bg="#34495E", relief=tk.SUNKEN, bd=3)
        result_frame.pack(pady=20, padx=50, fill=tk.BOTH, expand=True)
        
        result_font = font.Font(family="Arial", size=16)
        self.result_label = tk.Label(result_frame, 
                                     text="Choose your weapon! 👇",
                                     font=result_font, bg="#34495E", fg="#ECF0F1",
                                     wraplength=600, justify=tk.CENTER)
        self.result_label.pack(expand=True)
        
        # Choice buttons
        button_frame = tk.Frame(self.root, bg="#2C3E50")
        button_frame.pack(pady=20)
        
        button_font = font.Font(family="Arial", size=20, weight="bold")
        
        choices = [
            ("🪨\nRock", "rock"),
            ("📄\nPaper", "paper"),
            ("✂️\nScissors", "scissors")
        ]
        
        for text, choice in choices:
            btn = tk.Button(button_frame, text=text, font=button_font,
                          width=10, height=4, bg="#3498DB", fg="white",
                          activebackground="#2980B9", relief=tk.RAISED, bd=5,
                          cursor="hand2",
                          command=lambda c=choice: self.play_round(c))
            btn.pack(side=tk.LEFT, padx=15)
        
        # Bottom buttons
        bottom_frame = tk.Frame(self.root, bg="#2C3E50")
        bottom_frame.pack(pady=10)
        
        small_font = font.Font(family="Arial", size=12)
        
        stats_btn = tk.Button(bottom_frame, text="📊 View Stats", font=small_font,
                             bg="#9B59B6", fg="white", command=self.show_stats,
                             cursor="hand2", padx=15, pady=5)
        stats_btn.pack(side=tk.LEFT, padx=10)
        
        reset_btn = tk.Button(bottom_frame, text="🔄 New Match", font=small_font,
                             bg="#E67E22", fg="white", command=self.reset_match,
                             cursor="hand2", padx=15, pady=5)
        reset_btn.pack(side=tk.LEFT, padx=10)
        
        quit_btn = tk.Button(bottom_frame, text="🚪 Quit", font=small_font,
                            bg="#E74C3C", fg="white", command=self.quit_game,
                            cursor="hand2", padx=15, pady=5)
        quit_btn.pack(side=tk.LEFT, padx=10)
    
    def play_round(self, user_choice):
        """Play a single round"""
        if self.user_score >= 2 or self.computer_score >= 2:
            messagebox.showinfo("Match Over", "Start a new match to play again!")
            return
        
        computer_choice = random.choice(['rock', 'paper', 'scissors'])
        result = self.determine_winner(user_choice, computer_choice)
        
        # Update stats
        self.stats['total_rounds'] += 1
        if result == "user":
            self.stats['rounds_won'] += 1
            self.user_score += 1
        elif result == "computer":
            self.stats['rounds_lost'] += 1
            self.computer_score += 1
        else:
            self.stats['rounds_tied'] += 1
        
        # Display result
        user_emoji = self.emojis[user_choice]
        comp_emoji = self.emojis[computer_choice]
        
        if result == "tie":
            result_text = f"🤝 It's a TIE!\n\nYou: {user_emoji} {user_choice.title()}\nComputer: {comp_emoji} {computer_choice.title()}\n\n🤖 Great minds think alike!"
        elif result == "user":
            result_text = f"🎉 You WIN this round!\n\nYou: {user_emoji} {user_choice.title()}\nComputer: {comp_emoji} {computer_choice.title()}\n\n🤖 You got me this round!"
        else:
            result_text = f"💻 Computer WINS this round!\n\nYou: {user_emoji} {user_choice.title()}\nComputer: {comp_emoji} {computer_choice.title()}\n\n🤖 Too easy! I saw that coming!"
        
        self.result_label.config(text=result_text)
        self.round_num += 1
        self.update_score()
        
        # Check for match winner
        if self.user_score >= 2:
            self.stats['matches_won'] += 1
            self.stats['total_matches'] += 1
            self.save_stats()
            self.root.after(500, self.show_victory)
        elif self.computer_score >= 2:
            self.stats['matches_lost'] += 1
            self.stats['total_matches'] += 1
            self.save_stats()
            self.root.after(500, self.show_defeat)
    
    def determine_winner(self, user, computer):
        """Determine round winner"""
        if user == computer:
            return "tie"
        elif (user == 'rock' and computer == 'scissors') or \
             (user == 'paper' and computer == 'rock') or \
             (user == 'scissors' and computer == 'paper'):
            return "user"
        else:
            return "computer"
    
    def update_score(self):
        """Update score display"""
        self.score_label.config(text=f"You: {self.user_score}  |  Round: {self.round_num}  |  Computer: {self.computer_score}")
    
    def show_victory(self):
        """Show victory popup with trophy"""
        trophy = """
        
🏆 CONGRATULATIONS! 🏆
YOU ARE THE CHAMPION!

       ___________
      '._==_==_=_.'
      .-\\:      /-.
     | (|:.     |) |
      '-|:.     |-'
        \\::.    /
         '::. .'
           ) (
         _.' '._
        `""""""`

🎉 VICTORY ACHIEVED! 🎉

Final Score: You {user} - {comp} Computer

🎺 *TRUMPET FANFARE* 🎺
🎊 *CONFETTI FALLING* 🎊
👏 *CROWD CHEERING* 👏

You have proven your superiority!
        """.format(user=self.user_score, comp=self.computer_score)
        
        messagebox.showinfo("🏆 CHAMPION! 🏆", trophy)
        self.result_label.config(text="🏆 YOU WON THE MATCH! 🏆\n\nClick 'New Match' to play again!")
    
    def show_defeat(self):
        """Show defeat message"""
        message = f"""
🤖 Computer Wins! 🤖

Final Score: You {self.user_score} - {self.computer_score} Computer

💻 Victory is mine! As calculated!

Better luck next time, human! 👾
        """
        messagebox.showinfo("Computer Wins", message)
        self.result_label.config(text="💻 Computer won the match!\n\nClick 'New Match' to try again!")
    
    def show_stats(self):
        """Show statistics popup"""
        win_rate = (self.stats['matches_won'] / self.stats['total_matches'] * 100) if self.stats['total_matches'] > 0 else 0
        
        stats_text = f"""
📊 ALL-TIME STATISTICS 📊

Matches Won:     {self.stats['matches_won']}
Matches Lost:    {self.stats['matches_lost']}
Total Matches:   {self.stats['total_matches']}
Win Rate:        {win_rate:.1f}%

Rounds Won:      {self.stats['rounds_won']}
Rounds Lost:     {self.stats['rounds_lost']}
Rounds Tied:     {self.stats['rounds_tied']}
Total Rounds:    {self.stats['total_rounds']}
        """
        messagebox.showinfo("Statistics", stats_text)
    
    def reset_match(self):
        """Reset current match"""
        self.user_score = 0
        self.computer_score = 0
        self.round_num = 1
        self.rounds_history = []
        self.update_score()
        self.result_label.config(text="Choose your weapon! 👇")
    
    def quit_game(self):
        """Quit the game"""
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.save_stats()
            self.root.quit()
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()


if __name__ == "__main__":
    game = RPSGameGUI()
    game.run()
