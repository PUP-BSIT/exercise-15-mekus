import os  # Standard library

import pyfiglet  # Third-party library

# Dictionary of menu choices
MENU_CHOICES = {
    "1": "Check KDA (Kills/Deaths/Assists)",
    "2": "Check Headshot Accuracy",
    "3": "Check Win Rate",
    "4": "Check Spike Plant Success",
    "5": "Check Bomb Defusal Success",
    "0": "Exit Program"
}

class ValorantOps:
    """Handles Valorant statistics analysis for the agent."""

    def __init__(self):
        # Get agent's profile via user input
        self.agent_codename = input("Enter your agent codename: ")
        self.agent_rank = input("Enter your agent rank: ")
        self.agent_main_weapon = input("Enter your main weapon: ")
        self.agent_favorite_map = input("Enter your favorite map: ")

        # Menu actions mapped to corresponding methods
        self.actions = {
            "1": self.compute_kda,
            "2": self.calculate_headshot_accuracy,
            "3": self.evaluate_win_rate,
            "4": self.analyze_spike_plant_success,
            "5": self.check_bomb_defusal_success
        }

    def clear_screen(self):
        """Clears the terminal screen for better readability."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_banner(self):
        """Displays the banner and agent profile."""
        banner = pyfiglet.figlet_format("VALORANT STATS", font="slant")
        print(banner)
        print(f"Agent Codename : {self.agent_codename.upper()}")
        print(f"Rank           : {self.agent_rank}")
        print(f"Main Weapon    : {self.agent_main_weapon}")
        print(f"Favorite Map   : {self.agent_favorite_map}\n")

    def display_menu(self):
        """Displays the menu of available actions."""
        for key, desc in MENU_CHOICES.items():
            print(f"[{key}] {desc}")

    def handle_user_choice(self, choice):
        """
        Executes the selected menu action.

        Parameters:
            choice (str): The user's selected menu option.

        Returns:
            bool: False if user chooses to exit; True otherwise.
        """
        if choice == "0":
            print("Great job, Agent. Signing off...")
            return False

        if choice not in self.actions:
            print("Invalid option. Try again.")
            input("\nPress Enter to continue...")
            return True

        print("\n--- Result ---")
        self.actions[choice]()
        input("\nPress Enter to continue...")
        return True

    def compute_kda(self):
        """Calculates and displays the KDA (Kills + Assists) / Deaths."""
        self.clear_screen()
        try:
            kills = int(input("Enter kills: "))
            deaths = int(input("Enter deaths: "))
            assists = int(input("Enter assists: "))
        except ValueError:
            print("Invalid input. Please enter numbers only.")
            return

        if deaths == 0:
            print("\nKDA: No deaths, nice! You’re untouchable.")
            return

        kda = (kills + assists) / deaths
        print(
            f"\nKDA Breakdown:\n"
            f" - Kills  : {kills}\n"
            f" - Assists: {assists}\n"
            f" - Deaths : {deaths}\n"
            f" => KDA Ratio: ({kills} + {assists}) / {deaths} = {kda:.2f} "
            f"(impact actions per death)"
        )

    def calculate_headshot_accuracy(self):
        """Calculates and displays the headshot accuracy percentage."""
        self.clear_screen()
        try:
            headshots = int(input("Enter headshots: "))
            shots = int(input("Enter total shots: "))
        except ValueError:
            print("Please type numbers only.")
            return

        if shots == 0:
            print("You didn't fire any shots.")
            return

        accuracy = (headshots / shots) * 100
        print(f"Headshot Accuracy: {accuracy:.2f}%")

    def evaluate_win_rate(self):
        """Calculates and displays the win rate percentage."""
        self.clear_screen()
        try:
            wins = int(input("Enter number of wins: "))
            games = int(input("Enter total games: "))
        except ValueError:
            print("Please type numbers only.")
            return

        if games == 0:
            print("No games played yet.")
            return

        rate = (wins / games) * 100
        print(f"Win Rate: {rate:.2f}%")

    def analyze_spike_plant_success(self):
        """Calculates and displays the spike plant success rate."""
        self.clear_screen()
        try:
            success = int(input("Enter successful spike plants: "))
            tries = int(input("Enter total attempts: "))
        except ValueError:
            print("Please type numbers only.")
            return

        if tries == 0:
            print("You didn't try planting.")
            return

        rate = (success / tries) * 100
        print(f"Spike Plant Success: {rate:.2f}%")

    def check_bomb_defusal_success(self):
        """Calculates and displays the bomb defusal success rate."""
        self.clear_screen()
        try:
            defusals = int(input("Enter successful defusals: "))
            attempts = int(input("Enter total defusal attempts: "))
        except ValueError:
            print("Please type numbers only.")
            return

        if attempts == 0:
            print("No defusal attempts made.")
            return

        success_rate = (defusals / attempts) * 100
        print(f"Bomb Defusal Success Rate: {success_rate:.2f}%")

    def menu(self):
        """Main loop that runs the Valorant statistics program."""
        while True:
            self.clear_screen()
            self.display_banner()
            self.display_menu()
            choice = input("\nChoose an option: ")
            if not self.handle_user_choice(choice):
                break