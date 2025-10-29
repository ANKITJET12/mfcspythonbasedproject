"""
CipherMesh Core Logic - Web Version
Updated to match the correct implementation with tagged categories
"""

# ---------------------- Layer 1: Set Layer (Fixed with tags) ---------------------- #
class SetLayer:
    """
    Simpler and robust implementation:
    - We make encryption always emit a category tag (one character) before the shifted char
      so decryption becomes straightforward and unambiguous.
    - We operate only on printable ASCII range 32..126 inclusive (95 chars) and wrap inside it.
    - Categories: V (vowel), C (consonant), D (digit), S (symbol/space/other)
    """
    PRINT_MIN = 32
    PRINT_MAX = 126
    PRINT_RANGE = PRINT_MAX - PRINT_MIN + 1

    def __init__(self):
        self.vowels = set("AEIOUaeiou")
        self.digits = set("0123456789")
        # consonants are any alphabetic characters not in vowels
        # shifts chosen so categories remain distinct when reversed using the tag
        self.shifts = {'V': 5, 'C': 3, 'D': 2, 'S': 1}

    def _to_printable_index(self, ch):
        return ord(ch) - self.PRINT_MIN

    def _from_printable_index(self, idx):
        return chr((idx % self.PRINT_RANGE) + self.PRINT_MIN)

    def _shift_printable(self, ch, shift):
        idx = self._to_printable_index(ch)
        return self._from_printable_index(idx + shift)

    def _unshift_printable(self, ch, shift):
        idx = self._to_printable_index(ch)
        return self._from_printable_index(idx - shift)

    def _category_of(self, ch):
        if ch in self.vowels:
            return 'V'
        if ch.isalpha():
            return 'C'
        if ch in self.digits:
            return 'D'
        return 'S'

    def encrypt(self, text):
        encrypted = []
        steps = []
        for ch in text:
            cat = self._category_of(ch)
            shift = self.shifts[cat]
            # ensure we operate on printable characters; if char is already outside printable,
            # convert its code into printable range first
            if ord(ch) < self.PRINT_MIN or ord(ch) > self.PRINT_MAX:
                # map it into printable range using modulo to avoid crashes
                ch = self._from_printable_index(ord(ch))
            out = self._shift_printable(ch, shift)
            # We prefix with category tag to make decryption deterministic
            encrypted_piece = cat + out
            encrypted.append(encrypted_piece)
            steps.append({
                'input': ch,
                'rule': cat,
                'shift': shift,
                'output': encrypted_piece
            })
        return ''.join(encrypted), steps

    def decrypt(self, text):
        # Expecting pairs of (category, shifted_char)
        decrypted = []
        steps = []
        i = 0
        while i < len(text):
            cat = text[i]
            if i + 1 >= len(text):
                # malformed: no character after tag — treat remaining as symbol
                shifted = text[i]
                i += 1
                decrypted.append(shifted)
                steps.append({
                    'input': f'{cat}',
                    'rule': 'Symbol',
                    'shift': self.shifts.get(cat, self.shifts['S']),
                    'output': shifted
                })
                continue
            shifted = text[i+1]
            shift = self.shifts.get(cat, self.shifts['S'])
            original = self._unshift_printable(shifted, shift)
            decrypted.append(original)
            steps.append({
                'input': f'{cat}{shifted}',
                'rule': cat,
                'shift': shift,
                'output': original
            })
            i += 2
        return ''.join(decrypted), steps

# ---------------------- Layer 2: Function Layer (Fixed to printable range) ---------------------- #
class FunctionLayer:
    """
    Maps printable ASCII [32..126] -> indices [0..94] and applies affine transformation
    f(x) = (a*x + b) mod m where m = 95 (printable count). We always work within printable range.
    """
    PRINT_MIN = 32
    PRINT_MAX = 126
    M = PRINT_MAX - PRINT_MIN + 1  # 95

    def __init__(self, a=3, b=7, m=None):
        m = self.M if m is None else m
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

    def _to_index(self, ch):
        return ord(ch) - self.PRINT_MIN

    def _from_index(self, idx):
        return chr((idx % self.m) + self.PRINT_MIN)

    def encrypt(self, text):
        encrypted = []
        steps = []
        for ch in text:
            idx = self._to_index(ch)
            y = (self.a * idx + self.b) % self.m
            out = self._from_index(y)
            encrypted.append(out)
            steps.append({
                'input': ch,
                'input_ascii': ord(ch),
                'output': out,
                'output_ascii': ord(out),
                'formula': f"({self.a}×{idx}+{self.b}) mod {self.m} = {y}"
            })
        return ''.join(encrypted), steps

    def decrypt(self, text):
        decrypted = []
        steps = []
        for ch in text:
            y = self._to_index(ch)
            x = (self.a_inv * (y - self.b)) % self.m
            # Handle negative modulo correctly
            if x < 0:
                x = (x + self.m) % self.m
            out = self._from_index(x)
            decrypted.append(out)
            steps.append({
                'input': ch,
                'input_ascii': ord(ch),
                'output': out,
                'output_ascii': ord(out),
                'formula': f"f⁻¹({y}) = ({self.a_inv}×({y}-{self.b})) mod {self.m} = {x}"
            })
        return ''.join(decrypted), steps

# ---------------------- Layer 3: Graph Layer (block reversal) ---------------------- #
class GraphLayer:
    def __init__(self, block_size=4):
        self.block_size = block_size

    def _transform(self, text):
        transformed = []
        for i in range(0, len(text), self.block_size):
            block = text[i:i+self.block_size]
            transformed.append(block[::-1])
        return ''.join(transformed)

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
        # same operation because reversal is its own inverse
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
            'name': 'Layer 1: Set Classification Shift (Tagged)',
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

    def decrypt_with_details(self, ciphertext, set_layer_rules=None):
        """Decrypt with detailed processing information.
        
        Args:
            ciphertext: The encrypted text to decrypt
            set_layer_rules: Deprecated - no longer needed with tagged approach
        """
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
        
        # Layer 1: Set Layer (reverse) - now unambiguous with tags
        set_decrypted, set_steps = self.set_layer.decrypt(function_decrypted)
        details['layers'].append({
            'name': 'Reversing Layer 1: Set Classification Shift (Tagged)',
            'input': function_decrypted,
            'output': set_decrypted,
            'steps': set_steps
        })
        
        return {
            'plaintext': set_decrypted,
            'details': details
        }
