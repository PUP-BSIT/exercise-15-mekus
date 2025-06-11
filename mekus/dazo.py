import os
import pyfiglet

WIN = "win"
LOSS = "loss"

MENU_CHOICES = {
    "1": "Enter Match Stats (Kills/Deaths/Assists)",
    "2": "Calculate Overall KDA",
    "3": "Log Match Outcome (Win/Loss)",
    "4": "View Win Rate",
    "5": "View Full Match Summary",
    "0": "Exit Module"
}

class MobileLegendsStats:
    """A class to track and display Mobile Legends player statistics."""

    def __init__(self):
        """Initialize player stats with default values."""
        self.codename = "Dazo"
        self.kills = 0
        self.deaths = 0
        self.assists = 0
        self.matches_played = 0
        self.wins = 0

    def clear_screen(self):
        """Clear the terminal screen based on the operating system."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def enter_match_stats(self):
        """
        Prompt user to enter match stats (kills, deaths, assists)
        and update totals.
        """
        self.clear_screen()
        print("--- Enter Match Stats ---\n")

        try:
            kills = int(input("Enter kills: "))
        except ValueError:
            print("Invalid input for kills. Use whole numbers.")
            return

        try:
            deaths = int(input("Enter deaths: "))
        except ValueError:
            print("Invalid input for deaths. Use whole numbers.")
            return

        try:
            assists = int(input("Enter assists: "))
        except ValueError:
            print("Invalid input for assists. Use whole numbers.")
            return

        self.kills += kills
        self.deaths += deaths
        self.assists += assists

        print("Match stats recorded!")

    def calculate_kda(self):
        """Calculate and display the player's KDA ratio."""
        self.clear_screen()
        print("--- KDA Calculation ---\n")

        if self.deaths == 0:
            print("KDA Ratio: ∞ (Perfect record!)")
            return

        kda_ratio = (self.kills + self.assists) / self.deaths
        print(f"Overall KDA Ratio: {kda_ratio:.2f}")

    def log_match_outcome(self):
        """
        Log whether the match was a win or loss,
        and update stats accordingly.
        """
        self.clear_screen()
        print("--- Log Match Outcome ---\n")

        match_result = input("Enter match result (win/loss): ").strip().lower()

        if match_result not in (WIN, LOSS):
            print("Invalid input. Please enter 'win' or 'loss'.")
            return

        self.matches_played += 1

        if match_result == WIN:
            self.wins += 1

        print(f"Match logged as a {match_result.title()}.")

    def view_win_rate(self):
        """Calculate and display the player's win rate."""
        self.clear_screen()
        print("--- Win Rate ---\n")

        if self.matches_played == 0:
            print("No matches logged yet.")
            return

        win_rate = (self.wins / self.matches_played) * 100
        print(
            f"Win Rate: {win_rate:.2f}% "
            f"({self.wins} out of {self.matches_played} matches)"
        )

    def print_kda_summary(self):
        """Display a short KDA summary in the match summary view."""
        if self.deaths == 0:
            print("KDA Ratio       : ∞")
        else:
            kda_ratio = (self.kills + self.assists) / self.deaths
            print(f"KDA Ratio       : {kda_ratio:.2f}")

    def print_win_rate_summary(self):
        """Display a short win rate summary in the match summary view."""
        if self.matches_played > 0:
            win_rate = (self.wins / self.matches_played) * 100
            print(f"Win Rate        : {win_rate:.2f}%")

    def display_totals(self):
        """Display total match stats."""
        print(f"Total Matches   : {self.matches_played}")
        print(f"Total Wins      : {self.wins}")
        print(f"Total Losses    : {self.matches_played - self.wins}")
        print(f"Total Kills     : {self.kills}")
        print(f"Total Deaths    : {self.deaths}")
        print(f"Total Assists   : {self.assists}")

    def view_summary(self):
        """Display a full summary of all tracked stats."""
        self.clear_screen()
        print("--- Full Match Summary ---\n")
        self.display_totals()
        self.print_win_rate_summary()
        self.print_kda_summary()

    def display_menu(self):
        """Display the main menu with formatted title and menu choices."""
        self.clear_screen()
        title = pyfiglet.figlet_format("ML STATS", font="slant")
        print(title)
        print(f"Legend: {self.codename}\n")

        for key, description in MENU_CHOICES.items():
            print(f"{key}. {description}")

    def handle_user_choice(self, choice):
        """Execute the appropriate action based on the user's menu choice."""
        actions = {
            "1": self.enter_match_stats,
            "2": self.calculate_kda,
            "3": self.log_match_outcome,
            "4": self.view_win_rate,
            "5": self.view_summary
        }

        if choice == "0":
            print("\nSee you next game, Legend!")
            return False

        action = actions.get(choice)

        if action is not None:
            action()
        else:
            print("Invalid choice. Try again.")

        input("\n[Press Enter to continue...]")
        return True

    def menu(self):
        """
        Run the main loop to display the menu and
        handle user input continuously.
        """
        while True:
            self.display_menu()
            # Exit the loop if the user selects the exit option
            user_choice = input("\nChoose an option: ").strip()
            if not self.handle_user_choice(user_choice):
                break