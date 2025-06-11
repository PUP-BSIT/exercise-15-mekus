import random
import os

import pyfiglet

CHOICES = ['rock', 'paper', 'scissors']
QUIT_COMMAND = 'quit'

class RockPaperScissors:
    def __init__(self):
        self.choices = CHOICES
        self.quit_command = QUIT_COMMAND
        self.score = {'player': 0, 'computer': 0}

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_title(self):
        """Display the game title using pyfiglet."""
        print(pyfiglet.figlet_format('Rock! Paper! Scissors!'))

    def get_user_choice(self):
        """Prompt user for input and return it in lowercase."""
        print("Choices: rock, paper, scissors")
        prompt = f"Type your choice (or '{self.quit_command}' to exit): "
        return input(prompt).lower()

    def determine_winner(self, user_choice, computer_choice):
        """Determine the game result based on choices."""
        if user_choice == computer_choice:
            return 'tie'
        win_conditions = (
            (user_choice == 'rock' and computer_choice == 'scissors') or
            (user_choice == 'paper' and computer_choice == 'rock') or
            (user_choice == 'scissors' and computer_choice == 'paper')
        )
        return 'player' if win_conditions else 'computer'

    def display_score(self):
        """Display current score."""
        player_score = self.score['player']
        computer_score = self.score['computer']
        print(f'Score - Player: {player_score}, Computer: {computer_score}')

    def display_final_score(self):
        """Display final score when game ends."""
        print('Final Score - ', end='')
        self.display_score()

    def handle_result(self, winner):
        """Handle the result and update score."""
        if winner == 'tie':
            print("It's a tie!")
        elif winner == 'player':
            print('You win!')
            self.score['player'] += 1
        else:
            print('You lose!')
            self.score['computer'] += 1

    def main(self):
        """Main game loop."""
        self.clear_screen()
        self.display_title()

        while True:
            self.clear_screen()
            self.display_title()
            self.display_score()
            
            user_choice = self.get_user_choice()

            if user_choice == self.quit_command:
                print('Thanks for playing!')
                self.display_final_score()
                break

            if user_choice not in self.choices:
                print('Invalid choice. Try again.')
                input('Press Enter to continue...')
                continue

            computer_choice = random.choice(self.choices)
            print(f'Computer chose: {computer_choice}')

            winner = self.determine_winner(user_choice, computer_choice)
            self.handle_result(winner)

            self.display_score()
            input('Press Enter to continue...')
            
game = RockPaperScissors()
game.main()