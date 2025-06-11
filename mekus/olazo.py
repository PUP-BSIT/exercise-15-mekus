# Import necessary standard libraries
import os
import random

# Import necessary third-party libraries
import pypokedex
from pokemon.skills import get_pokemon
from pyfiglet import figlet_format

# Game constants
FONT_STYLE = "cosmic"
MENU_WIDTH = 80
INITIAL_SCORE = 0
INITIAL_STREAK = 0
INITIAL_ATTEMPTS = 0

# Scoring constants
MIN_SCORE = 0
BASE_POINTS = 10
ATTEMPT_BONUS_MULTIPLIER = 5
STREAK_BONUS_MULTIPLIER = 0.1
BASE_STREAK_BONUS = 1

# Scoring penalties
SCORE_PENALTY = 2  # Points deducted for using a hint

# Difficulty levels
EASY_DIFFICULTY = "EASY"
MEDIUM_DIFFICULTY = "MEDIUM"
HARD_DIFFICULTY = "HARD"

# Difficulty configurations
DIFFICULTIES = {
    EASY_DIFFICULTY: {
        "MULTIPLIER": 1.0,
        "MAX_POKEMON": 150,  # Easy difficulty allows up to 150 Pokemon
        "ATTEMPTS": 3,
        "HINTS": 4,
    },
    MEDIUM_DIFFICULTY: {
        "MULTIPLIER": 1.5,
        "MAX_POKEMON": 250,  # Medium difficulty allows up to 250 Pokemon
        "ATTEMPTS": 2,
        "HINTS": 3,
    },
    HARD_DIFFICULTY: {
        "MULTIPLIER": 2.0,
        "MAX_POKEMON": 400,  # Hard difficulty allows up to 400 Pokemon
        "ATTEMPTS": 1,
        "HINTS": 2,
    },
}

# Unit conversion for Pokemon height and weight
POKEMON_UNIT_DIVISOR = 10

class PokemonGame:
    """Main game class that handles all Pokemon guessing game logic."""

    def __init__(self):
        """Initialize the game with default values."""
        self.player_name = ""
        self.is_class_running = True
        self.score = INITIAL_SCORE
        self.highest_score = INITIAL_SCORE
        self.streak = INITIAL_STREAK
        self.highest_streak = INITIAL_STREAK
        self.difficulty = EASY_DIFFICULTY
        self.used_pokemon_ids = set()
        self.current_pokemon = None
        self.current_pokemon_ascii = ""
        self.is_game_active = False
        self.hints = []
        self.attempts_left = INITIAL_ATTEMPTS  # Initalize attempts left to 0

    def menu(self):
        """Main game loop."""
        self.display_welcome()
        self.get_player_name()
        self.clear_screen()

        # Call method to show the main menu
        self.show_main_menu()

    def display_welcome(self):
        """Display welcome message with ASCII art."""
        self.clear_screen(has_prompt=False)

        # Prepare welcome banner using ASCII art
        BANNER_JUSTIFICATION = "center"
        banner = figlet_format(
            "Who's That Pokemon?",
            font=FONT_STYLE,
            justify=BANNER_JUSTIFICATION,
            width=MENU_WIDTH,
        )

        # Print the welcome banner
        print(banner)
        print("Welcome! Let's see how well you know your Pokemon!")

    def get_player_name(self):
        """Get and validate player name."""

        # Loop until a valid name is entered
        while True:
            name = input("Please enter your name: ").strip()

            # Check if name is not empty
            if name:
                self.player_name = name  # Set player name

                print(f"\nHello, {name}! Let's start the game!")
                return  # Exit loop if name is valid

            print("Name cannot be empty. Please try again.")

    def show_main_menu(self):
        """Display main menu and handle user selection."""
        self.clear_screen(has_prompt=False)

        # Display main menu options
        while self.is_class_running:
            self.display_main_menu_options()
            self.handle_main_menu_choice()

    def get_main_menu_options(self):
        """Return the main menu options dictionary."""
        return {
            "START_GAME": self.start_game,
            "VIEW_INSTRUCTIONS": self.display_instructions,
            "CHANGE_DIFFICULTY": self.change_difficulty,
            "VIEW_STATS": self.display_stats,
            "RESET_GAME": self.reset_game,
        }

    def display_main_menu_options(self):
        """Display the main menu options."""

        # Prepare main menu title and options
        MAIN_MENU_TITLE = "MAIN MENU"
        self.display_menu(self.get_main_menu_options(), MAIN_MENU_TITLE)

    def handle_main_menu_choice(self):
        """Process user's main menu selection."""
        choice = self.get_choice(len(self.get_main_menu_options()))

        # If choice is 0, exit the game
        if choice == 0:
            self.exit_game()  # Exit the game
            return

        self.clear_screen(has_prompt=False)
        self.execute_menu_action(self.get_main_menu_options(), choice)

    def go_back_to_main_menu(self):
        """Clear screen and return to main menu."""
        self.show_main_menu()

    def start_game(self):
        """Start a new game round."""
        self.setup_round()

        # Main game loop for the round
        while self.attempts_left > 0 and self.is_game_active:
            self.display_round_state()
            self.show_round_menu()

        # Check if the class is still running before handling game over
        if not self.is_class_running:
            return  # Exit if class is not running

        # Out of ATTEMPTS
        self.handle_game_over()

    def display_round_state(self):
        """Display current round information and Pokemon."""
        self.clear_screen(has_prompt=False)

        self.display_round_state_info()
        self.display_pokemon()

    def setup_round(self):
        """Set up a new round with random Pokemon."""
        self.is_game_active = True
        self.attempts_left = DIFFICULTIES[self.difficulty]["ATTEMPTS"]
        self.select_random_pokemon()
        self.generate_hints()

    def display_round_state_info(self):
        """Display current round information."""
        ROUND_INFO_TITLE = "ROUND INFORMATION"

        # Define round information to display and their methods
        round_info = [
            f"SCORE: {self.score}",
            f"STREAK: {self.streak}",
            f"DIFFICULTY: {self.difficulty}",
            f"ATTEMPTS_LEFT: {self.attempts_left}",
            f"HINTS_AVAILABLE: {len(self.hints)}",
        ]

        self.show_box_display(ROUND_INFO_TITLE, round_info)

    def select_random_pokemon(self):
        """Select a random Pokemon that hasn't been used."""
        pokemon_id = self.generate_unique_pokemon_id()
        self.current_pokemon = pypokedex.get(dex=pokemon_id)
        self.used_pokemon_ids.add(pokemon_id)

    def generate_unique_pokemon_id(self):
        """Generate a unique Pokemon ID within the difficulty range."""
        MIN_POKEMON_ID = 1
        MAX_POKEMON_ID = DIFFICULTIES[self.difficulty]["MAX_POKEMON"]

        # Loop until a valid unique Pokemon ID is found
        while True:
            pokemon_id = random.randint(MIN_POKEMON_ID, MAX_POKEMON_ID)
            if self.is_valid_pokemon_id(pokemon_id):
                return pokemon_id  # Return the valid unique Pokemon ID

    def is_valid_pokemon_id(self, pokemon_id):
        """Check if Pokemon ID exists and hasn't been used."""
        pokemon = None
        try:
            # Check if the Pokemon ID exists in the Pypokedex
            pokemon = pypokedex.get(dex=pokemon_id)
        except Exception:
            # If ValueError is raised, the Pokemon ID does not exist
            return False

        return pokemon and (pokemon_id not in self.used_pokemon_ids)

    def is_pokemon_unique(self, pokemon_id):
        """Check if the Pokemon ID is unique for this game."""
        if pokemon_id not in self.used_pokemon_ids:
            self.current_pokemon = pypokedex.get(dex=pokemon_id)
            self.used_pokemon_ids.add(pokemon_id)
            return True

    def generate_hints(self):
        """Generate hints based on Pokemon data."""
        HINTS_COUNT = DIFFICULTIES[self.difficulty]["HINTS"]
        self.hints = self.create_possible_hints()[:HINTS_COUNT]

    def create_possible_hints(self):
        """Create all possible hints for the current Pokemon."""
        return [
            self.create_type_hint(),
            self.create_abilities_hint(),
            self.create_height_hint(),
            self.create_weight_hint(),
        ]

    def create_type_hint(self):
        """Create type hint string."""
        types = [t.capitalize() for t in self.current_pokemon.types]
        return f"Type: {', '.join(types)}"

    def create_abilities_hint(self):
        """Create abilities hint string."""
        abilities = [
            ability.name.capitalize()
            for ability in self.current_pokemon.abilities
        ]
        return f"Abilities: {', '.join(abilities)}"

    def create_height_hint(self):
        """Create height hint string."""
        return f"Height: {self.current_pokemon.height / POKEMON_UNIT_DIVISOR}m"

    def create_weight_hint(self):
        """Create weight hint string."""
        return f"Weight: {self.current_pokemon.weight / POKEMON_UNIT_DIVISOR}kg"

    def display_pokemon(self):
        """Display Pokemon ASCII art as silhouette."""
        pokemon_data = get_pokemon(pid=self.current_pokemon.dex)
        ascii_art = pokemon_data[self.current_pokemon.dex]["ascii"]
        self.current_pokemon_ascii = ascii_art

        silhouette = self.create_silhouette(ascii_art)
        print(f"{silhouette}\n")

    def create_silhouette(self, ascii_art):
        """Convert ASCII art to silhouette effect."""
        if not ascii_art:
            return ""

        SILHOUETTE_CHAR_MAP = {
            "@": "@",
            "\n": "\n",
        }

        return "".join(SILHOUETTE_CHAR_MAP.get(char, " ") for char in ascii_art)

    def show_round_menu(self):
        """Display round options and handle choice."""
        self.display_round_state_menu_options()
        self.handle_round_menu_choice()

    def get_round_menu_options(self):
        """Return the round menu options dictionary."""
        return {
            "MAKE_GUESS": self.process_guess,
            "VIEW_HINT": self.show_hint,
            "VIEW_STATS": self.display_stats,
        }

    def display_round_state_menu_options(self):
        """Display the round menu options."""
        ROUND_MENU_TITLE = "ROUND ACTIONS"
        self.display_menu(self.get_round_menu_options(), ROUND_MENU_TITLE)

    def handle_round_menu_choice(self):
        """Process user's round menu selection."""
        choice = self.get_choice(len(self.get_round_menu_options()))

        if choice == 0:
            self.go_back_to_main_menu()
            return

        self.clear_screen(has_prompt=False)
        self.display_round_state()  # Show current round state
        self.execute_menu_action(self.get_round_menu_options(), choice)

    def process_guess(self):
        """Handle player's Pokemon guess."""
        print(" === GUESS THE POKEMON ".ljust(MENU_WIDTH, "="))
        guess = input("ENTER YOUR GUESS: ").strip().lower()
        correct_name = self.current_pokemon.name.lower()

        self.handle_guess(guess, correct_name)

    def handle_guess(self, guess, correct_name):
        """Check if the player's guess is correct."""

        # Check if the guess matches the correct Pokemon name
        if guess == correct_name:
            self.handle_correct_guess()  # Call method to handle correct guess
            return  # Exit if guess is correct

        # Call method to handle wrong guess
        self.handle_wrong_guess()

    def handle_correct_guess(self):
        """Handle correct guess - update score and streak."""
        points = self.calculate_points()
        self.update_score_and_streak(points)
        self.update_highest_stats()
        self.display_correct_guess_message(points)
        self.clear_screen()
        # Start new round immediately
        self.setup_round()

    def update_score_and_streak(self, points):
        """Update player score and increment streak."""
        self.score += points
        self.streak += 1

    def display_correct_guess_message(self, points):
        """Display the correct guess confirmation message."""
        self.clear_screen(has_prompt=False)
        self.display_current_pokemon_art()

        # Title for correct guess feedback
        TITLE = "CORRECT GUESS"

        # Prepare messages for correct guess feedback
        messages = [
            f"Correct! It's {self.current_pokemon.name.capitalize()}!",
            f"You earned {points} points!",
        ]

        self.show_box_display(TITLE, messages)

    def display_current_pokemon_art(self):
        """Display the current Pokemon's ASCII art."""
        print(self.current_pokemon_ascii)

    def update_highest_stats(self):
        """Update highest score and streak if current is greater."""

        # Check if current score is greater than highest score
        if self.score > self.highest_score:
            self.highest_score = self.score  # Update highest score

        # Check if current streak is greater than highest streak
        if self.streak > self.highest_streak:
            self.highest_streak = self.streak  # Update highest streak

    def calculate_points(self):
        """Calculate points based on attempts and difficulty."""
        base_points = self.calculate_base_points()
        difficulty_multiplier = DIFFICULTIES[self.difficulty]["MULTIPLIER"]
        streak_bonus = self.calculate_streak_bonus()

        # Return total points as an integer
        return int(base_points * difficulty_multiplier * streak_bonus)

    def calculate_base_points(self):
        """Calculate base points with attempt bonus."""
        return BASE_POINTS + (self.attempts_left * ATTEMPT_BONUS_MULTIPLIER)

    def calculate_streak_bonus(self):
        """Calculate streak bonus multiplier."""
        return BASE_STREAK_BONUS + (self.streak * STREAK_BONUS_MULTIPLIER)

    def handle_wrong_guess(self):
        """Handle incorrect guess."""
        self.clear_screen(has_prompt=False)
        self.display_round_state()

        self.decrement_attempts()

        # Check if player has attempts remaining
        if self.has_attempts_remaining():
            self.display_retry_prompt()
            self.clear_screen()
            return  # Exit if attempts are still left

        # No attempts left, display game over message
        self.display_no_attempts_left_message()
        self.clear_screen()

    def decrement_attempts(self):
        """Decrease remaining attempts and show feedback."""
        self.attempts_left -= 1
        self.display_wrong_guess_message()

    def display_wrong_guess_message(self):
        """Display feedback for wrong guess."""

        # Title for wrong guess feedback
        TITLE = "WRONG GUESS"

        # Prepare messages for wrong guess feedback
        messages = [f"Incorrect! {self.attempts_left} attempts left."]

        self.show_box_display(TITLE, messages)

    def has_attempts_remaining(self):
        """Check if player has attempts remaining."""
        return self.attempts_left > 0

    def display_retry_prompt(self):
        """Prompt player to try again or use hint."""
        print("Try again or use a hint!")

    def display_no_attempts_left_message(self):
        """Display game over message when no attempts remain."""
        print("No more attempts left!")

    def show_hint(self):
        """Display next available hint."""

        # Check if there are any hints left
        if not self.hints:
            print("\nNo more HINTS available!")
            self.clear_screen()
            return

        # Retrieve the next hint and remove it from the list
        hint = self.hints.pop(0)

        # Prepare hint title and message
        HINT_TITLE = "HINT"
        HINT_MESSAGE = [
            f"Hint: {hint}",
        ]

        # Display hint in a formatted box
        self.show_box_display(HINT_TITLE, HINT_MESSAGE)

        # Small penalty for HINTS
        self.score = max(MIN_SCORE, self.score - SCORE_PENALTY)

        self.clear_screen()

    def handle_game_over(self):
        """Handle end of round when out of ATTEMPTS."""

        self.streak = INITIAL_STREAK  # Reset streak on game over

        self.clear_screen(has_prompt=False)

        # Display current Pokemon ASCII art
        self.display_current_pokemon_art()

        print(
            f"\nGame Over! "
            f"The Pokemon was {self.current_pokemon.name.capitalize()}."
        )
        self.clear_screen()

    def display_instructions(self):
        """Display game instructions."""

        # Title
        INSTRUCTIONS_TITLE = "HOW TO PLAY"

        # Instructions for the game
        INSTRUCTIONS = [
            "Guess the Pokemon from its silhouette!",
            "",
            "Gameplay:",
            "- You get limited attempts per Pokemon",
            "- Use hints carefully (they cost points)",
            "- Higher difficulty = more points",
            "",
            "Scoring:",
            "- Base points: 10",
            "- Bonus for remaining attempts",
            "- Streak multiplier",
            "- Difficulty multiplier",
        ]

        self.show_box_display(INSTRUCTIONS_TITLE, INSTRUCTIONS)
        self.clear_screen()

    def change_difficulty(self):
        """Allow player to change difficulty."""
        self.display_difficulty_options()
        self.handle_difficulty_choice()

    def display_difficulty_options(self):
        """Display available difficulty options."""
        difficulties = list(DIFFICULTIES.keys())
        self.display_menu(difficulties, "Select Difficulty")

    def handle_difficulty_choice(self):
        """Process user's difficulty selection."""
        print("NOTE: Changing the difficulty will reset your stats!\n")

        difficulties = list(DIFFICULTIES.keys())
        choice = self.get_choice(len(difficulties))

        if choice == 0:
            self.clear_screen(has_prompt=False)
            return

        self.reset_stats()  # Reset stats before changing difficulty
        self.set_difficulty(difficulties[choice - 1])
        self.clear_screen()

    def set_difficulty(self, difficulty):
        """Set the game difficulty and notify player."""
        self.difficulty = difficulty
        print(f"\nDifficulty set to {difficulty}!")

    def display_stats(self):
        """Display current player statistics."""

        # Title for player statistics
        PLAYER_STATS_TITLE = "PLAYER STATISTICS"

        # Prepare player statistics to display
        player_stats = [
            f"Player: {self.player_name}",
            f"Current Score: {self.score}",
            f"Highest Score: {self.highest_score}",
            f"Current Streak: {self.streak}",
            f"Highest Streak: {self.highest_streak}",
            f"Current Difficulty: {self.difficulty}",
            f"Pokemon Encountered: {len(self.used_pokemon_ids)}",
        ]

        self.show_box_display(PLAYER_STATS_TITLE, player_stats)

        self.clear_screen()

    def reset_game(self):
        """Reset game to initial state."""
        self.reset_stats()  # Reset player stats

        RESET_TITLE = "GAME RESET"
        RESET_MESSAGE = [
            "Game has been reset!",
        ]

        self.show_box_display(RESET_TITLE, RESET_MESSAGE)

        self.clear_screen()

    def reset_stats(self):
        """Reset player statistics to initial values."""
        self.score = INITIAL_SCORE
        self.streak = INITIAL_STREAK
        self.used_pokemon_ids.clear()

    def exit_game(self):
        """Exit game with confirmation."""
        print(f"\nThanks for playing, {self.player_name}!")
        self.is_class_running = False  # Set class running flag to False

        # Clear any pending game state
        self.is_game_active = False
        self.attempts_left = 0

    def display_menu(self, options, title):
        """Display formatted menu with options."""
        menu_options = self.format_menu_options(options)
        self.show_box_display(title, menu_options)

    def format_menu_options(self, options):
        """Format menu options with numbers."""
        START_COUNT = 1
        menu_options = []

        # Add each option with its corresponding number
        for option_count, option in enumerate(options, start=START_COUNT):
            menu_options.append(f"[{option_count}] {option.replace('_', ' ')}")

        # Add back option to return to previous menu
        menu_options.append("[0] BACK")
        return menu_options

    def show_box_display(self, title, items):
        """Display items in a formatted box."""
        self.print_box_top(title)
        self.print_box_items(items)
        self.print_box_bottom()

    def print_box_top(self, title):
        """Print the top border with title."""
        print(f" === {title} ".ljust(MENU_WIDTH, "="))

    def print_box_items(self, items):
        """Print all items in the box."""
        for item in items:
            print(f"| {item}".ljust(MENU_WIDTH, " ") + "|")

    def print_box_bottom(self):
        """Print the bottom border of the box."""
        print(" " + "=" * (MENU_WIDTH - 1))

    def get_choice(self, max_choice):
        """Get and validate user choice from menu options."""

        # Loop until a valid choice is made
        while True:
            choice = self.get_integer_choice("Enter your choice: ")

            # If choice is None, continue to prompt again
            if choice is None:
                continue

            # If choice is valid, return it
            if self.is_valid_choice(choice, max_choice):
                return choice

            print(f"Please enter a number between 0 and {max_choice}.")

    def get_integer_choice(self, prompt):
        try:
            # Prompt user for input and convert to integer
            return int(input(prompt).strip())
        except ValueError:
            print("Invalid input. Please enter a number.")
            return None

    def is_valid_choice(self, choice, max_choice):
        """Validate user choice against max options."""

        # Check if choice is within valid range
        if choice < 0 or choice > max_choice:
            return False

        # Return True if choice is valid
        return True

    def execute_menu_action(self, options_dict, choice):
        """Execute the selected menu action from the options dictionary."""
        selected_action = list(options_dict.values())[choice - 1]
        selected_action()

    def clear_screen(self, has_prompt=True):
        """Clear console screen."""

        # Check if the has_prompt flag is set to True
        if has_prompt:
            # Prompt the user before clearing the screen
            input("\nPress Enter to continue...")

        # Clear the console screen
        os.system("cls" if os.name == "nt" else "clear")