from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
import base64

app = Flask(__name__)
CORS(app)  # allow cross-origin requests

# Simple SBOX for demo
SBOX = list(range(256))[::-1]  # reverse
inverse_SBOX = SBOX[::-1]

# Key expansion
def expand_key(user_key):
    hash_bytes = hashlib.sha256(user_key.encode()).digest()
    K1 = hash_bytes[:11]
    K2 = hash_bytes[11:22]
    K3 = hash_bytes[22:]
    return K1, K2, K3

# Encryption layers
def layer1(state, K1):
    return [(SBOX[b] ^ K1[i % len(K1)]) for i, b in enumerate(state)]

def layer2(state, K2):
    state = state[::-1]
    return [b ^ K2[i % len(K2)] for i, b in enumerate(state)]

def layer3(state, K3):
    return [((b + K3[i % len(K3)]) % 256) ^ K3[i % len(K3)] for i, b in enumerate(state)]

def xycrypt_encrypt(plaintext, user_key):
    K1, K2, K3 = expand_key(user_key)
    state = [ord(c) for c in plaintext]
    state = layer1(state, K1)
    state = layer2(state, K2)
    state = layer3(state, K3)
    # Base64 encode for readable ciphertext
    return base64.b64encode(bytes(state)).decode()

# Decryption layers
def layer3_decrypt(state, K3):
    return [((b ^ K3[i % len(K3)]) - K3[i % len(K3)]) % 256 for i, b in enumerate(state)]

def layer2_decrypt(state, K2):
    state = [b ^ K2[i % len(K2)] for i, b in enumerate(state)]
    return state[::-1]

def layer1_decrypt(state, K1):
    return [inverse_SBOX[b ^ K1[i % len(K1)]] for i, b in enumerate(state)]

def xycrypt_decrypt(ciphertext_b64, user_key):
    try:
        state = list(base64.b64decode(ciphertext_b64))
    except:
        return None  # invalid ciphertext
    K1, K2, K3 = expand_key(user_key)
    state = layer3_decrypt(state, K3)
    state = layer2_decrypt(state, K2)
    state = layer1_decrypt(state, K1)
    return ''.join(chr(b) for b in state)

# Routes
@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    plaintext = data.get('plaintext')
    key = data.get('key')
    if not plaintext or not key:
        return jsonify({'error': 'Provide plaintext and key'}), 400
    ciphertext = xycrypt_encrypt(plaintext, key)
    return jsonify({'ciphertext': ciphertext})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    ciphertext = data.get('ciphertext')
    key = data.get('key')
    if not ciphertext or not key:
        return jsonify({'error': 'Provide ciphertext and key'}), 400
    plaintext = xycrypt_decrypt(ciphertext, key)
    if plaintext is None:
        return jsonify({'error': 'Invalid ciphertext or key'}), 400
    return jsonify({'plaintext': plaintext})

if __name__ == '__main__':
    app.run(debug=True)
