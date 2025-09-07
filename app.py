from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

# Simple SBOX for demo
SBOX = list(range(256))
SBOX = SBOX[::-1]  # just reverse for substitution
inverse_SBOX = SBOX[::-1]

def expand_key(user_key):
    # SHA-256 hash
    hash_bytes = hashlib.sha256(user_key.encode()).digest()
    # Split into 3 parts for layers
    K1 = hash_bytes[:11]
    K2 = hash_bytes[11:22]
    K3 = hash_bytes[22:]
    return K1, K2, K3

def layer1(state, K1):
    return [(SBOX[b] ^ K1[i % len(K1)]) for i, b in enumerate(state)]

def layer2(state, K2):
    # simple permutation: reverse + XOR with K2
    state = state[::-1]
    return [b ^ K2[i % len(K2)] for i, b in enumerate(state)]

def layer3(state, K3):
    return [((b + K3[i % len(K3)]) % 256) ^ K3[i % len(K3)] for i, b in enumerate(state)]

def xycrypt_encrypt(plaintext, user_key):
    K1, K2, K3 = expand_key(user_key)
    state = [ord(c) for c in plaintext]  # convert to ASCII
    state = layer1(state, K1)
    state = layer2(state, K2)
    state = layer3(state, K3)
    # convert to hex string for easy display
    return ''.join(f'{b:02x}' for b in state)

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    plaintext = data.get('plaintext')
    key = data.get('key')
    if not plaintext or not key:
        return jsonify({'error': 'Provide plaintext and key'}), 400
    ciphertext = xycrypt_encrypt(plaintext, key)
    return jsonify({'ciphertext': ciphertext})

if __name__ == '__main__':
    app.run(debug=True)






def layer3_decrypt(state, K3):
    return [((b ^ K3[i % len(K3)]) - K3[i % len(K3)]) % 256 for i, b in enumerate(state)]

def layer2_decrypt(state, K2):
    state = [b ^ K2[i % len(K2)] for i, b in enumerate(state)]
    return state[::-1]

def layer1_decrypt(state, K1):
    return [inverse_SBOX[b ^ K1[i % len(K1)]] for i, b in enumerate(state)]

def xycrypt_decrypt(ciphertext_hex, user_key):
    state = [int(ciphertext_hex[i:i+2], 16) for i in range(0, len(ciphertext_hex), 2)]
    K1, K2, K3 = expand_key(user_key)
    state = layer3_decrypt(state, K3)
    state = layer2_decrypt(state, K2)
    state = layer1_decrypt(state, K1)
    return ''.join(chr(b) for b in state)

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    ciphertext = data.get('ciphertext')
    key = data.get('key')
    if not ciphertext or not key:
        return jsonify({'error': 'Provide ciphertext and key'}), 400
    plaintext = xycrypt_decrypt(ciphertext, key)
    return jsonify({'plaintext': plaintext})

