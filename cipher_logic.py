"""
CipherMesh Core Logic - Web Version
Extracted from cipher.py for use in web application
"""

# ---------------------- Layer 1: Set Layer ---------------------- #
class SetLayer:
    def __init__(self):
        self.vowels = "AEIOUaeiou"
        self.consonants = "BCDFGHJKLMNPQRSTVWXYZcdfghjklmnpqrstvwxyz"
        self.digits = "0123456789"
        self.shifts = {'vowels': 5, 'consonants': 3, 'digits': 2, 'symbols': 1}

    def _shift_char(self, char, shift):
        return chr((ord(char) + shift) % 128)

    def _unshift_char(self, char, shift):
        return chr((ord(char) - shift) % 128)

    def encrypt(self, text):
        encrypted_chars = []
        steps = []
        for char in text:
            if char in self.vowels:
                shift, rule = self.shifts['vowels'], "Vowel"
            elif char in self.consonants:
                shift, rule = self.shifts['consonants'], "Consonant"
            elif char in self.digits:
                shift, rule = self.shifts['digits'], "Digit"
            else:
                shift, rule = self.shifts['symbols'], "Symbol"
            encrypted_char = self._shift_char(char, shift)
            encrypted_chars.append(encrypted_char)
            steps.append({
                'input': char,
                'rule': rule,
                'shift': shift,
                'output': encrypted_char
            })
        return "".join(encrypted_chars), steps

    def decrypt(self, text):
        decrypted_chars = []
        steps = []
        for char in text:
            decrypted_char = ''
            matched_rule = None
            matched_shift = None
            for rule, shift in self.shifts.items():
                unshifted_char = self._unshift_char(char, shift)
                is_match = False
                if rule == 'vowels' and unshifted_char in self.vowels:
                    is_match = True
                elif rule == 'consonants' and unshifted_char in self.consonants:
                    is_match = True
                elif rule == 'digits' and unshifted_char in self.digits:
                    is_match = True
                if is_match:
                    decrypted_char = unshifted_char
                    matched_rule = rule.capitalize()
                    matched_shift = shift
                    break
            if not decrypted_char:
                decrypted_char = self._unshift_char(char, self.shifts['symbols'])
                matched_rule = "Symbol"
                matched_shift = self.shifts['symbols']
            decrypted_chars.append(decrypted_char)
            steps.append({
                'input': char,
                'rule': matched_rule,
                'shift': matched_shift,
                'output': decrypted_char
            })
        return "".join(decrypted_chars), steps

# ---------------------- Layer 2: Function Layer ---------------------- #
class FunctionLayer:
    def __init__(self, a=3, b=7, m=128):
        if self._gcd(a, m) != 1:
            raise ValueError("'a' must be coprime to 'm'.")
        self.a, self.b, self.m = a, b, m
        self.a_inv = self._mod_inverse(a, m)

    def _gcd(self, a, b):
        while b:
            a, b = b, a % b
        return a

    def _mod_inverse(self, a, m):
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return None

    def encrypt(self, text):
        encrypted_chars = []
        steps = []
        for char in text:
            x = ord(char)
            encrypted_val = (self.a * x + self.b) % self.m
            encrypted_char = chr(encrypted_val)
            encrypted_chars.append(encrypted_char)
            steps.append({
                'input': char,
                'input_ascii': x,
                'output': encrypted_char,
                'output_ascii': encrypted_val,
                'formula': f"({self.a}×{x}+{self.b}) mod {self.m} = {encrypted_val}"
            })
        return "".join(encrypted_chars), steps

    def decrypt(self, text):
        decrypted_chars = []
        steps = []
        for char in text:
            y = ord(char)
            decrypted_val = (self.a_inv * (y - self.b)) % self.m
            decrypted_char = chr(decrypted_val)
            decrypted_chars.append(decrypted_char)
            steps.append({
                'input': char,
                'input_ascii': y,
                'output': decrypted_char,
                'output_ascii': decrypted_val,
                'formula': f"f⁻¹({y}) = ({self.a_inv}×({y}-{self.b})) mod {self.m} = {decrypted_val}"
            })
        return "".join(decrypted_chars), steps

# ---------------------- Layer 3: Graph Layer ---------------------- #
class GraphLayer:
    def __init__(self, block_size=4):
        self.block_size = block_size

    def _transform(self, text):
        transformed_text = ""
        for i in range(0, len(text), self.block_size):
            block = text[i:i+self.block_size]
            transformed_text += block[::-1]
        return transformed_text

    def encrypt(self, text):
        encrypted_text = self._transform(text)
        # Show block transformation
        blocks = []
        for i in range(0, len(text), self.block_size):
            block = text[i:i+self.block_size]
            reversed_block = block[::-1]
            blocks.append({
                'original': block,
                'transformed': reversed_block
            })
        return encrypted_text, blocks

    def decrypt(self, text):
        # Decrypt is same as encrypt for block reversal
        decrypted_text = self._transform(text)
        blocks = []
        for i in range(0, len(text), self.block_size):
            block = text[i:i+self.block_size]
            reversed_block = block[::-1]
            blocks.append({
                'original': block,
                'transformed': reversed_block
            })
        return decrypted_text, blocks

# ---------------------- Main CipherMesh System ---------------------- #
class CipherMesh:
    def __init__(self):
        self.set_layer = SetLayer()
        self.function_layer = FunctionLayer()
        self.graph_layer = GraphLayer()

    def encrypt_with_details(self, plaintext):
        """Encrypt with detailed processing information."""
        details = {
            'plaintext': plaintext,
            'length': len(plaintext),
            'layers': []
        }
        
        # Layer 1: Set Layer
        set_encrypted, set_steps = self.set_layer.encrypt(plaintext)
        details['layers'].append({
            'name': 'Layer 1: Set Classification Shift',
            'input': plaintext,
            'output': set_encrypted,
            'steps': set_steps
        })
        
        # Layer 2: Function Layer
        function_encrypted, function_steps = self.function_layer.encrypt(set_encrypted)
        details['layers'].append({
            'name': 'Layer 2: Mathematical Substitution',
            'input': set_encrypted,
            'output': function_encrypted,
            'steps': function_steps,
            'formula': f'f(x) = ({self.function_layer.a}x + {self.function_layer.b}) mod {self.function_layer.m}'
        })
        
        # Layer 3: Graph Layer
        graph_encrypted, graph_blocks = self.graph_layer.encrypt(function_encrypted)
        details['layers'].append({
            'name': 'Layer 3: Graph Transformation (Block Reversal)',
            'input': function_encrypted,
            'output': graph_encrypted,
            'blocks': graph_blocks
        })
        
        return {
            'ciphertext': graph_encrypted,
            'details': details
        }

    def decrypt_with_details(self, ciphertext):
        """Decrypt with detailed processing information."""
        details = {
            'ciphertext': ciphertext,
            'length': len(ciphertext),
            'layers': []
        }
        
        # Layer 3: Graph Layer (reverse)
        graph_decrypted, graph_blocks = self.graph_layer.decrypt(ciphertext)
        details['layers'].append({
            'name': 'Reversing Layer 3: Graph Transformation',
            'input': ciphertext,
            'output': graph_decrypted,
            'blocks': graph_blocks
        })
        
        # Layer 2: Function Layer (reverse)
        function_decrypted, function_steps = self.function_layer.decrypt(graph_decrypted)
        details['layers'].append({
            'name': 'Reversing Layer 2: Inverse Function',
            'input': graph_decrypted,
            'output': function_decrypted,
            'steps': function_steps,
            'formula': f'f⁻¹(y) = ({self.function_layer.a_inv}×(y-{self.function_layer.b})) mod {self.function_layer.m}'
        })
        
        # Layer 1: Set Layer (reverse)
        set_decrypted, set_steps = self.set_layer.decrypt(function_decrypted)
        details['layers'].append({
            'name': 'Reversing Layer 1: Set Classification Shift',
            'input': function_decrypted,
            'output': set_decrypted,
            'steps': set_steps
        })
        
        return {
            'plaintext': set_decrypted,
            'details': details
        }
