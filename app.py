from flask import Flask, render_template, request, jsonify
from cipher_logic import CipherMesh, SetLayer, FunctionLayer, GraphLayer

app = Flask(__name__)

# Initialize cipher system
cipher_mesh = CipherMesh()

@app.route('/')
def index():
    """Main page route."""
    return render_template('index.html')

@app.route('/api/encrypt', methods=['POST'])
def encrypt():
    """Encryption API endpoint."""
    try:
        data = request.get_json()
        plaintext = data.get('plaintext', '')
        
        if not plaintext:
            return jsonify({'error': 'Plaintext is required'}), 400
        
        # Get detailed encryption process
        result = cipher_mesh.encrypt_with_details(plaintext)
        
        return jsonify({
            'success': True,
            'result': result['ciphertext'],
            'plaintext': plaintext,
            'details': result['details']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/decrypt', methods=['POST'])
def decrypt():
    """Decryption API endpoint."""
    try:
        data = request.get_json()
        ciphertext = data.get('ciphertext', '')
        
        if not ciphertext:
            return jsonify({'error': 'Ciphertext is required'}), 400
        
        # Get detailed decryption process
        result = cipher_mesh.decrypt_with_details(ciphertext)
        
        return jsonify({
            'success': True,
            'result': result['plaintext'],
            'ciphertext': ciphertext,
            'details': result['details']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import socket
    
    def find_free_port(start_port=5001, max_port=5010):
        """Find an available port starting from start_port."""
        for port in range(start_port, max_port + 1):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex(('localhost', port)) != 0:
                    return port
        return start_port  # Fallback to start_port if all are busy
    
    port = find_free_port()
    print(f"\n{'='*60}")
    print(f"  CipherMesh Web Application")
    print(f"  Running on: http://localhost:{port}")
    print(f"{'='*60}\n")
    app.run(debug=True, port=port, use_reloader=False)
