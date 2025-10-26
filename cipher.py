import sys
import os
import time
import random
import shutil

# ---------------------- UI and Color Definitions ---------------------- #
class UI:
    """Handles the UI, colors, and styling for the terminal."""
    RED = '\033[91m'
    DARKRED = '\033[31m'
    BRIGHTRED = '\033[38;5;196m'
    WHITE = '\033[97m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

    def _slow_print(self, text, speed=0.002):
        """Prints text with a typewriter effect for atmosphere."""
        for ch in text:
            sys.stdout.write(ch)
            sys.stdout.flush()
            time.sleep(speed)
        print()

    def clear_screen(self):
        """Clears the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def terminal_size(self):
        """Gets the current terminal size."""
        try:
            cols, rows = shutil.get_terminal_size(fallback=(120, 36))
        except:
            cols, rows = 120, 36
        return cols, rows

    def spiderweb(self):
        """Draws a spiderweb background for the top of the screen."""
        cols, rows = self.terminal_size()
        rows_to_draw = max(8, rows // 2)
        center_x, center_y = cols // 2, rows_to_draw // 2
        for r in range(rows_to_draw):
            row_chars = [' '] * cols
            for c in range(cols):
                if random.random() < 0.025:
                    row_chars[c] = random.choice(['.', '*', '+'])
            print(self.DARKRED + ''.join(row_chars) + self.ENDC)

    def print_big_title(self, text="CIPHERMESH"):
        """Prints the main title in a cleaner, more readable ASCII art format."""
        cols, _ = self.terminal_size()
        art = [
            " █████╗     ██╗    ██████╗    ██╗  ██╗   ███████╗   ██████╗    ███╗   ███╗   ███████╗    ██████╗    ██╗  ██╗",
            " ██╔══      ██║    ██╔══██╗   ██║  ██║   ██╔════╝   ██╔══██╗   ████╗ ████║   ██╔════╝   ██╔════╝   ██║  ██║",
            " ██║        ██║    ██████╔╝   ███████║   █████╗     ██████╔╝   ██╔████╔██║   █████╗      █████╗    ███████║",
            " ██║        ██║    ██╔══╝     ██╔══██║   ██╔══╝     ██╔══██╗   ██║╚██╔╝██║   ██╔══╝     ╚═══██╗    ██╔══██║",
            " ██╚══      ██║    ██║        ██║  ██║   ███████╗   ██║  ██║   ██║ ╚═╝ ██║   ███████╗   ██████╔╝   ██║  ██║",
            "  █████╗    ██╝    ██╝        ╚═╝  ╚═╝   ╚══════╝   ██╝  ██╝   ╚═╝     ╚═╝   ╚══════╝   ╚═════╝    ╚═╝  ╚═╝"
        ]
        box_width = max(len(line) for line in art)
        left = (cols - box_width) // 2
        
        print()
        for line in art:
            print(' ' * left + self.RED + self.BOLD + line + self.ENDC)
        print()
        
        tagline = "A Multi-Stage Secure Text Transformation System"
        print(self.WHITE + tagline.center(cols) + self.ENDC)
        print()

    def print_banner(self):
        """Prints the full startup screen."""
        self.clear_screen()
        self.spiderweb()
        self.print_big_title()

    def print_header(self, text):
        """Prints a styled header for content sections."""
        print(f"\n{self.BOLD}{self.RED}╔═[ {text} ]{'═' * (70 - len(text))}╗{self.ENDC}")

    def print_footer(self):
        """Prints a styled footer for content sections."""
        print(f"{self.BOLD}{self.RED}╚{'═' * 73}╝{self.ENDC}\n")

    def print_box(self, title, content):
        """Prints content inside a formatted box."""
        self.print_header(title)
        for line in content:
            print(f"{self.BOLD}{self.RED}  │ {line}{self.ENDC}")
        self.print_footer()

    def show_loader(self, text, duration=1.5):
        """Displays a loading animation."""
        chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        start_time = time.time()
        while time.time() - start_time < duration:
            for char in chars:
                sys.stdout.write(f"\r{self.RED}[*] {text}... {char}{self.ENDC}")
                sys.stdout.flush()
                time.sleep(0.05)
        sys.stdout.write(f"\r{self.RED}[+] {text}... Complete!     \n{self.ENDC}")
        time.sleep(0.5)

    def print_menu(self):
        """Prints the main menu options."""
        self.print_header("SYSTEM MENU")
        print(f"{self.BOLD}{self.RED}  ├─[1] Initiate Encryption Protocol{self.ENDC}")
        print(f"{self.BOLD}{self.RED}  ├─[2] Initiate Decryption Protocol{self.ENDC}")
        print(f"{self.BOLD}{self.RED}  ├─[3] Shutdown System{self.ENDC}")
        print(f"{self.BOLD}{self.RED}  └─")

    def get_input(self, prompt):
        """Gets user input with a styled prompt."""
        return input(f"{self.BOLD}{self.WHITE}    └─> {prompt}:{self.ENDC} ")

    def get_confirmation(self, prompt):
        """Gets a yes/no confirmation from the user."""
        while True:
            choice = self.get_input(f"{prompt} (y/n)").lower()
            if choice in ['y', 'yes']: return True
            elif choice in ['n', 'no']: return False

# ---------------------- Layer 1: Set Layer ---------------------- #
class SetLayer:
    def __init__(self):
        self.vowels = "AEIOUaeiou"
        self.consonants = "BCDFGHJKLMNPQRSTVWXYZcdfghjklmnpqrstvwxyz"
        self.digits = "0123456789"
        self.shifts = {'vowels': 5, 'consonants': 3, 'digits': 2, 'symbols': 1}
        self.ui = UI()

    def _shift_char(self, char, shift): return chr((ord(char) + shift) % 128)
    def _unshift_char(self, char, shift): return chr((ord(char) - shift) % 128)

    def encrypt(self, text):
        encrypted_chars = []
        self.ui.print_header("LAYER 1: SET CLASSIFICATION SHIFT")
        for char in text:
            if char in self.vowels: shift, rule = self.shifts['vowels'], "Vowel"
            elif char in self.consonants: shift, rule = self.shifts['consonants'], "Consonant"
            elif char in self.digits: shift, rule = self.shifts['digits'], "Digit"
            else: shift, rule = self.shifts['symbols'], "Symbol"
            encrypted_char = self._shift_char(char, shift)
            print(f"  {self.ui.WHITE}├── Input: '{char}' ({rule}) | Applying Shift: {shift} | Output: '{encrypted_char}'")
            encrypted_chars.append(encrypted_char)
        self.ui.print_footer()
        return "".join(encrypted_chars)

    def decrypt(self, text):
        decrypted_chars = []
        self.ui.print_header("REVERSING LAYER 1: SET CLASSIFICATION SHIFT")
        for char in text:
            decrypted_char = ''
            for rule, shift in self.shifts.items():
                unshifted_char = self._unshift_char(char, shift)
                is_match = False
                if rule == 'vowels' and unshifted_char in self.vowels: is_match = True
                elif rule == 'consonants' and unshifted_char in self.consonants: is_match = True
                elif rule == 'digits' and unshifted_char in self.digits: is_match = True
                if is_match:
                    decrypted_char = unshifted_char
                    print(f"  {self.ui.WHITE}├── Input: '{char}' | Matched Rule: {rule} | Reversing Shift: {shift} | Output: '{decrypted_char}'")
                    break
            if not decrypted_char:
                decrypted_char = self._unshift_char(char, self.shifts['symbols'])
                print(f"  {self.ui.WHITE}├── Input: '{char}' | Matched Rule: Symbol | Reversing Shift: {self.shifts['symbols']} | Output: '{decrypted_char}'")
            decrypted_chars.append(decrypted_char)
        self.ui.print_footer()
        return "".join(decrypted_chars)

# ---------------------- Layer 2: Function Layer ---------------------- #
class FunctionLayer:
    def __init__(self, a=3, b=7, m=128):
        if self._gcd(a, m) != 1: raise ValueError("'a' must be coprime to 'm'.")
        self.a, self.b, self.m = a, b, m
        self.a_inv = self._mod_inverse(a, m)
        self.ui = UI()

    def _gcd(self, a, b):
        while b: a, b = b, a % b
        return a

    def _mod_inverse(self, a, m):
        for x in range(1, m):
            if (a * x) % m == 1: return x
        return None

    def encrypt(self, text):
        encrypted_chars = []
        self.ui.print_header(f"LAYER 2: MATHEMATICAL SUBSTITUTION (f(x)=({self.a}x+{self.b})mod{self.m})")
        for char in text:
            x = ord(char)
            encrypted_val = (self.a * x + self.b) % self.m
            encrypted_char = chr(encrypted_val)
            print(f"  {self.ui.WHITE}├── Input: '{char}' (ASCII:{x}) | Applying f({x}) | Output: '{encrypted_char}' (ASCII:{encrypted_val})")
            encrypted_chars.append(encrypted_char)
        self.ui.print_footer()
        return "".join(encrypted_chars)

    def decrypt(self, text):
        decrypted_chars = []
        self.ui.print_header(f"REVERSING LAYER 2: INVERSE FUNCTION (f⁻¹(y))")
        for char in text:
            y = ord(char)
            decrypted_val = (self.a_inv * (y - self.b)) % self.m
            decrypted_char = chr(decrypted_val)
            print(f"  {self.ui.WHITE}├── Input: '{char}' (ASCII:{y}) | Applying f⁻¹({y}) | Output: '{decrypted_char}' (ASCII:{decrypted_val})")
            decrypted_chars.append(decrypted_char)
        self.ui.print_footer()
        return "".join(decrypted_chars)

# ---------------------- Layer 3: Graph Layer ---------------------- #
class GraphLayer:
    def __init__(self, block_size=4):
        self.block_size = block_size
        self.ui = UI()

    def _transform(self, text):
        transformed_text = ""
        for i in range(0, len(text), self.block_size):
            block = text[i:i+self.block_size]
            transformed_text += block[::-1]
        return transformed_text

    def encrypt(self, text):
        self.ui.print_header("LAYER 3: GRAPH TRANSFORMATION (BLOCK REVERSAL)")
        print(f"  {self.ui.WHITE}├── Input: {text}")
        encrypted_text = self._transform(text)
        print(f"  {self.ui.WHITE}└── Output: {encrypted_text}")
        self.ui.print_footer()
        return encrypted_text

    def decrypt(self, text):
        self.ui.print_header("REVERSING LAYER 3: GRAPH TRANSFORMATION")
        print(f"  {self.ui.WHITE}├── Input: {text}")
        decrypted_text = self._transform(text)
        print(f"  {self.ui.WHITE}└── Output: {decrypted_text}")
        self.ui.print_footer()
        return decrypted_text

# ---------------------- Main CipherMesh System ---------------------- #
class CipherMesh:
    def __init__(self):
        self.set_layer = SetLayer()
        self.function_layer = FunctionLayer()
        self.graph_layer = GraphLayer()
        self.ui = UI()

    def encrypt(self, plaintext):
        self.ui.clear_screen()
        self.ui.print_box("ENCRYPTION PROTOCOL: ACTIVE", [f"{self.ui.WHITE}Plaintext Payload: {plaintext}", f"Length: {len(plaintext)} characters"])
        self.ui.show_loader("Processing Layers")

        set_encrypted = self.set_layer.encrypt(plaintext)
        function_encrypted = self.function_layer.encrypt(set_encrypted)
        graph_encrypted = self.graph_layer.encrypt(function_encrypted)

        self.ui.print_box("ENCRYPTION SUMMARY", [
            f"{self.ui.RED}{self.ui.BOLD}SUCCESS: Plaintext transformed.",
            f"{self.ui.WHITE}Final Ciphertext: {self.ui.BRIGHTRED}{graph_encrypted}{self.ui.WHITE}",
            f"Resulting Length: {len(graph_encrypted)} characters"
        ])
        return graph_encrypted

    def decrypt(self, ciphertext):
        self.ui.clear_screen()
        self.ui.print_box("DECRYPTION PROTOCOL: ACTIVE", [f"{self.ui.WHITE}Ciphertext Payload: {ciphertext}", f"Length: {len(ciphertext)} characters"])
        self.ui.show_loader("Reversing Layers")

        graph_decrypted = self.graph_layer.decrypt(ciphertext)
        function_decrypted = self.function_layer.decrypt(graph_decrypted)
        set_decrypted = self.set_layer.decrypt(function_decrypted)

        self.ui.print_box("DECRYPTION SUMMARY", [
            f"{self.ui.RED}{self.ui.BOLD}SUCCESS: Ciphertext reverted.",
            f"{self.ui.WHITE}Final Plaintext: {self.ui.BRIGHTRED}{set_decrypted}{self.ui.WHITE}",
            f"Original Length: {len(set_decrypted)} characters"
        ])
        return set_decrypted

# ---------------------- Main execution ---------------------- #
if __name__ == "__main__":
    ui = UI()
    cipher_mesh = CipherMesh()

    def run_system():
        ui.print_banner()
        while True:
            ui.print_menu()
            choice = ui.get_input("Select an option (1-3)")

            if choice == '1':
                ui.clear_screen()
                ui.print_box("ENCRYPTION MODULE", ["Awaiting user input for plaintext payload."])
                plaintext = ui.get_input("Enter plaintext")
                if ui.get_confirmation(f"Confirm encryption for '{plaintext}'?"):
                    cipher_mesh.encrypt(plaintext)
                else:
                    print(f"\n{ui.RED}[!] Encryption aborted by user.{ui.ENDC}")
                input(f"\n{ui.WHITE}Press Enter to return to the main menu...{ui.ENDC}")
                ui.print_banner()

            elif choice == '2':
                ui.clear_screen()
                ui.print_box("DECRYPTION MODULE", ["Awaiting user input for ciphertext payload."])
                ciphertext = ui.get_input("Enter ciphertext")
                if ui.get_confirmation(f"Confirm decryption for '{ciphertext}'?"):
                    cipher_mesh.decrypt(ciphertext)
                else:
                    print(f"\n{ui.RED}[!] Decryption aborted by user.{ui.ENDC}")
                input(f"\n{ui.WHITE}Press Enter to return to the main menu...{ui.ENDC}")
                ui.print_banner()

            elif choice == '3':
                print(f"\n{ui.RED}{ui.BOLD}CipherMesh shutting down. Stay secure.{ui.ENDC}\n")
                break

            else:
                print(f"\n{ui.RED}[!] Invalid option. Please select 1, 2, or 3.{ui.ENDC}")
                time.sleep(2)
                ui.print_banner()
    run_system()

