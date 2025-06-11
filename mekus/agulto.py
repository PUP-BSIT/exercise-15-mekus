import os
import random

# Third-party libraries
from colorama import init, Fore  # Import colorama for colored terminal text 
import pyfiglet  # Import pyfiglet for ASCII art text

# Initialize colorama to automatically reset styles
init(autoreset=True)

# Constants
BACK_CHOICE = "0"  # Menu option to exit the game

# Dictionary mapping menu choices to descriptions
MENU_CHOICES = {
    "1": "Select Player",
    "2": "Shoot",
    "3": "Dunk",
    "4": "Three-Pointer",
    "5": "Check Stats",
    "6": "Rest and Recover",
    "0": "Exit Game"
}

# List of possible NBA teams
TEAMS = [
    "Los Angeles Lakers",
    "Golden State Warriors",
    "Boston Celtics",
    "Miami Heat",
    "Milwaukee Bucks",
    "Denver Nuggets"
]

# Class representing the NBA2K25 game
class NBA2K25:

    def __init__(self):
        # Initialize player attributes
        self.player_name = "LeBron James"
        self.team = "Los Angeles Lakers"
        self.points = 0
        self.stamina = 100
        self.shooting_skill = 85
        self.dunk_skill = 90
        self.three_point_skill = 75
        self.field_goal_attempted = 0
        self.field_goal_made = 0

    # Displays the game title using ASCII art
    def display_title(self):
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear terminal
        title = pyfiglet.figlet_format("NBA 2K25", font="slant")
        print(Fore.RED + title)

    # Allows player to input name and assigns a random team
    def select_player(self):
        self.player_name = input(
            Fore.YELLOW + "Enter player name: "
        ).strip()
        if not self.player_name:
            self.player_name = "LeBron James"  # Default name if input is empty

        self.team = random.choice(TEAMS)  # Randomly assign a team
        print(Fore.GREEN + pyfiglet.figlet_format(
            f"{self.player_name}", font="digital"
        ))
        print(Fore.LIGHTBLUE_EX + f"\nWelcome to {self.team}!")
        input(Fore.WHITE + "\nPress Enter to continue...")

    # Performs a 2-point jump shot attempt
    def shoot(self):
        self._attempt_shot(
            action_name="shoot",
            stamina_cost=5,
            points=2,
            success_chance=self.shooting_skill,
            success_text="SWISH!",
            success_message=f"{self.player_name} makes a jump shot! +2 points",
            fail_text="MISSED!",
            fail_message="The shot bounces off the rim!"
        )

    # Performs a dunk attempt
    def dunk(self):
        self._attempt_shot(
            action_name="dunk",
            stamina_cost=15,
            points=2,
            success_chance=self.dunk_skill,
            success_text="SLAM DUNK!",
            success_message=(
                f"🔥 {self.player_name} throws it down! +2 points 🔥"
            ),
            fail_text="BLOCKED!",
            fail_message="The defender swats it away!",
            min_stamina=15
        )

    # Performs a 3-point shot attempt
    def three_pointer(self):
        self._attempt_shot(
            action_name="three-pointer",
            stamina_cost=10,
            points=3,
            success_chance=self.three_point_skill,
            success_text="THREE!",
            success_message=(
                f"💰 {self.player_name} from downtown! +3 points 💰"
            ),
            fail_text="BRICK!",
            fail_message="Clanks off the backboard!",
            min_stamina=10
        )

    # Handles the logic for shot attempts including success/failure
    def _attempt_shot(
        self, action_name, stamina_cost, points, success_chance,
        success_text, success_message, fail_text, fail_message,
        min_stamina=0
    ):
        if self.stamina < min_stamina:
            print(Fore.RED + f"Not enough stamina to {action_name}!")
            input(Fore.WHITE + "\nPress Enter to continue...")
            return

        self.field_goal_attempted += 1
        self.stamina -= stamina_cost

        # Check for success based on chance
        if random.randint(1, 100) > success_chance:
            print(Fore.RED + pyfiglet.figlet_format(
                fail_text, font="digital"
            ))
            print(Fore.LIGHTRED_EX + fail_message)
            self.display_stats()
            input(Fore.WHITE + "\nPress Enter to continue...")
            return

        # If successful, update points and field goals made
        self.points += points
        self.field_goal_made += 1

        # Choose color and font based on type of shot
        success_color = (
            Fore.LIGHTBLUE_EX if points == 3 else Fore.LIGHTGREEN_EX
        )
        font = "smslant" if points != 2 else "big"

        print(success_color + pyfiglet.figlet_format(
            success_text, font=font
        ))
        print(success_color + success_message)
        self.display_stats()
        input(Fore.WHITE + "\nPress Enter to continue...")

    # Displays the player's current statistics
    def display_stats(self):
        print(Fore.YELLOW + "\n=== PLAYER STATS ===")
        print(Fore.CYAN + f"Player: {self.player_name}")
        print(Fore.CYAN + f"Team: {self.team}")
        print(Fore.GREEN + f"Points: {self.points}")

        if self.field_goal_attempted > 0:
            field_goal_pct = (
                self.field_goal_made / self.field_goal_attempted
            ) * 100
            print(Fore.LIGHTCYAN_EX +
                  f"FG: {self.field_goal_made}/{self.field_goal_attempted} "
                  f"({field_goal_pct:.1f}%)")

        print(Fore.LIGHTYELLOW_EX +
              f"Stamina: {self.stamina}/100")
        print(Fore.LIGHTGREEN_EX +
              f"Shooting: {self.shooting_skill}")
        print(Fore.LIGHTMAGENTA_EX +
              f"Dunking: {self.dunk_skill}")
        print(Fore.LIGHTBLUE_EX +
              f"3-Point: {self.three_point_skill}")

    # Wrapper to check and show stats from the menu
    def check_stats(self):
        self.display_title()
        self.display_stats()
        input(Fore.WHITE + "\nPress Enter to continue...")

    # Restores player stamina with a limit of 100
    def rest_and_recover(self):
        """Recover stamina up to a max of 100."""
        recovered = 20
        original_stamina = self.stamina
        self.stamina = min(100, self.stamina + recovered)
        gained = self.stamina - original_stamina

        print(Fore.GREEN + pyfiglet.figlet_format("Rest", font="standard"))
        print(Fore.LIGHTGREEN_EX +
              f"{self.player_name} takes a breather and recovers "
              f"{gained} stamina.")
        self.display_stats()
        input(Fore.WHITE + "\nPress Enter to continue...")

    # Displays the main menu and handles user input
    def menu(self):
        while True:
            self.display_title()
            print(Fore.YELLOW + "\n=== MAIN MENU ===")

            for key, desc in MENU_CHOICES.items():
                print(Fore.CYAN + f"{key}. {desc}")

            choice = input(Fore.YELLOW + "\nEnter choice: ").strip()

            if choice == BACK_CHOICE:
                self._exit_game()
                break

            self._handle_menu_choice(choice)

    # Handles execution of menu choices
    def _handle_menu_choice(self, choice):
        MENU_ACTIONS = {
            "1": self.select_player,
            "2": self.shoot,
            "3": self.dunk,
            "4": self.three_pointer,
            "5": self.check_stats,
            "6": self.rest_and_recover 
        }
        if choice not in MENU_ACTIONS:
            print(Fore.RED + "Invalid choice. Try again.")
            input(Fore.WHITE + "\nPress Enter to continue...")
            return

        MENU_ACTIONS[choice]()  # Call the corresponding method

    # Displays game over message and final stats
    def _exit_game(self):
        print(Fore.RED + pyfiglet.figlet_format(
            "Game Over!", font="slant"
        ))
        print(Fore.YELLOW + "Final Stats:")
        self.display_stats()