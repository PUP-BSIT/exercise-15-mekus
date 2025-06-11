import os
import pyfiglet

EXIT_CHOICE = "0"
MENU_CHOICES = {
    "1": "Agulto's Module",
    "2": "Dazo's Module",
    "3": "Jundam's Module",
    "4": "Olazo's Module",
    "5": "Serohijo's Module",
    "0": "Exit"
}

class MekusModules:
    """Handles the Mekus project module menu."""

    def __init__(self):
        """Initialize menu title."""
        self.title = "Mekus"

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        """Show the menu options."""
        self.clear_screen()
        print(pyfiglet.figlet_format(self.title))
        print("=== Mekus Module Menu ===\n")
        for key, description in MENU_CHOICES.items():
            print(f"{key}. {description}")

    def run_agulto_module(self):
        """Run Agulto's module."""
        # TODO(Agulto): Implement integration
        pass

    def run_dazo_module(self):
        """Run Dazo's module."""
        # TODO(Dazo): Implement integration
        pass

    def run_jundam_module(self):
        """Run Jundam's module."""
        # TODO(Jundam): Implement integration
        pass

    def run_olazo_module(self):
        """Run Olazo's module."""
        # TODO(Olazo): Implement integration
        pass

    def run_serohijos_module(self):
        """Run Serohijo's module."""
        # TODO(Serohijo): Implement integration
        pass

    def handle_user_choice(self, choice):
        """Handle a menu choice and run the selected module."""
        menu_handlers = {
            "1": self.run_agulto_module,
            "2": self.run_dazo_module,
            "3": self.run_jundam_module,
            "4": self.run_olazo_module,
            "5": self.run_serohijos_module
        }

        if choice == EXIT_CHOICE:
            print("\nExiting... Goodbye!")
            return False

        handler = menu_handlers.get(choice)
        if handler:
            handler()
        else:
            print("Invalid choice. Try again.")

        input("\n[Press Enter to return to the menu...]")
        return True

    def main(self):
        """Run the main menu loop."""
        while True:
            self.display_menu()
            # Exit loop early if user selects EXIT_CHOICE
            choice = input("\nChoose an option: ").strip()
            if not self.handle_user_choice(choice):
                break

if __name__ == "__main__":
    mekus = MekusModules()
    mekus.main()