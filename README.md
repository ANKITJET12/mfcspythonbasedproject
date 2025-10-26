# mfcspythonbasedproject



 
CipherMesh: A Multi-Stage Secure Text Transformation System

Introduction
CipherMesh is a terminal-based, multi-stage secure text transformation system built in Python. Designed as a comprehensive bachelor-level project, it integrates core concepts from Mathematical Foundations of Computer Science (MFCS) to create a unique, layered encryption and decryption pipeline.
The application features an immersive, red-themed "hacker-style" terminal interface, providing a highly engaging and verbose user experience. It demonstrates how abstract mathematical principles (Set Theory, Functions, Graph Theory) can be practically applied to build a robust cryptographic-inspired tool.
About
CipherMesh operates on the principle of a sequential cryptographic pipeline. Instead of relying on a single algorithm, it processes plaintext through three distinct, independent layers of transformation. The final ciphertext's security is derived from this layered complexity.
The system is designed to be fully reversible. The decryption process meticulously reverses each layer in the opposite order, applying the mathematical inverse of each transformation to perfectly reconstruct the original plaintext.
System Workflow
1.	Initialization: The user launches the application and is greeted by the main CipherMesh splash screen, featuring the ASCII art banner and a "spiderweb" background. The system menu prompts the user for a primary action.
 
2.	Encryption Protocol:
o	The user selects [1] Initiate Encryption Protocol.
o	The system requests a plaintext payload.
o	After user confirmation, the payload is processed through the three layers sequentially.
 
3.	Processing Pipeline:
o	Layer 1 (Set): The text is analyzed, and characters are shifted based on their set (vowel, consonant, etc.).
o	Layer 2 (Function): The output from Layer 1 is fed into an affine cipher, applying a mathematical function to each character's ASCII value.
 

o	Layer 3 (Graph): The output from Layer 2 undergoes a block-reversal transformation, obfuscating the final character relationships.

4.	Decryption Protocol:
o	The user selects [2] Initiate Decryption Protocol and provides the final ciphertext.
o	The system reverses the pipeline: Layer 3 is undone, then Layer 2 is inverted, and finally, Layer 1's shifts are reversed.
o	The original plaintext is restored and presented to the user.
 
 
Features
•	Immersive 'Hacker-Style' Terminal UI: A visually engaging, red-and-black themed interface inspired by professional cybersecurity tools like Metasploit. It includes a dynamic "spiderweb" background, styled headers, and formatted output.
•	Layer 1 - Set Layer (Classification Encryption):
o	Applies Set Theory concepts.
o	Classifies all input characters into disjoint sets: vowels, consonants, digits, and symbols.
o	Applies a unique shift value to each set, making simple frequency analysis more difficult.
•	Layer 2 - Function Layer (Mathematical Substitution):
o	Based on MFCS concepts of Functions and Relations.
o	Applies a bijective affine cipher f(x) = (3x + 7) mod 128 to the ASCII value of each character.
o	Includes the calculation of the modular multiplicative inverse to ensure a valid, reversible decryption function.
•	Layer 3 - Graph Layer (Relational Encryption):
o	Inspired by Graph Theory, treating text as a sequence of vertices.
o	Applies a relational transformation by reversing the text in fixed-size blocks (e.g., ABCD-EFGH becomes DCBA-HGFE).
o	This layer effectively obfuscates character adjacencies and patterns (n-grams) left by the previous layers.
•	Full Decryption Pipeline:
o	A robust decryption module that perfectly reverses each layer in the opposite order (Graph -> Function -> Set).
o	Guarantees lossless restoration of the original plaintext from the ciphertext.
•	Interactive & Verbose Mode:
o	Provides detailed, step-by-step terminal output during both encryption and decryption, showing the input and output of each specific layer.
o	Includes user-friendly confirmation prompts and "processing" loaders to enhance the user experience.
Source Files
This project is contained entirely within a single script, simplifying execution and distribution.
•	cipher.py
o	Description: The main and only Python script. It contains the complete application, including:
	The UI class for all screen rendering, colors, and styling.
	The SetLayer, FunctionLayer, and GraphLayer classes, each containing their respective encrypt and decrypt logic.
	The main CipherMesh class that manages the overall encryption/decryption pipeline.


