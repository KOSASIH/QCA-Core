# src/algorithms/cryptography/post_quantum_cryptography.py

from ntru import NTRU
import json
import os
import time
import hashlib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class PostQuantumCryptography:
    def __init__(self, p=11, q=127, d=1):
        self.ntru = NTRU(p, q, d)
        self.public_key = None
        self.private_key = None

    def generate_keypair(self):
        """Generate a public/private key pair."""
        self.public_key, self.private_key = self.ntru.generate_keypair()
        self.save_keys()
        logging.info("Generated and saved key pair.")
        return self.public_key, self.private_key

    def save_keys(self):
        """Save the public and private keys to files."""
        keys = {
            'public_key': self.public_key,
            'private_key': self.private_key
        }
        with open('keys.json', 'w') as f:
            json.dump(keys, f)
        logging.info("Keys saved to keys.json.")

    def load_keys(self):
        """Load the public and private keys from files."""
        if os.path.exists('keys.json'):
            with open('keys.json', 'r') as f:
                keys = json.load(f)
                self.public_key = keys['public_key']
                self.private_key = keys['private_key']
                logging.info("Keys loaded from keys.json.")
        else:
            logging.error("Key file not found. Please generate keys first.")

    def encrypt(self, message: str) -> dict:
        """Encrypt a message using the public key."""
        start_time = time.time()
        ciphertext = self.ntru.encrypt(message, self.public_key)
        encryption_time = time.time() - start_time
        logging.info(f"Encryption completed in {encryption_time:.4f} seconds.")
        
        # Create a hash of the ciphertext for integrity check
        integrity_hash = hashlib.sha256(ciphertext.encode()).hexdigest()
        return {
            'ciphertext': ciphertext,
            'integrity_hash': integrity_hash
        }

    def decrypt(self, encrypted_data: dict) -> str:
        """Decrypt a ciphertext using the private key."""
        start_time = time.time()
        ciphertext = encrypted_data['ciphertext']
        integrity_hash = encrypted_data['integrity_hash']

        # Verify integrity
        if integrity_hash != hashlib.sha256(ciphertext.encode()).hexdigest():
            logging.error("Integrity check failed! The ciphertext may have been tampered with.")
            raise ValueError("Integrity check failed!")

        plaintext = self.ntru.decrypt(ciphertext, self.private_key)
        decryption_time = time.time() - start_time
        logging.info(f"Decryption completed in {decryption_time:.4f} seconds.")
        return plaintext

    def hybrid_encrypt(self, message: str) -> dict:
        """Hybrid encryption using NTRU and symmetric encryption (e.g., AES)."""
        # Placeholder for hybrid encryption implementation
        logging.warning("Hybrid encryption is not yet implemented.")
        return self.encrypt(message)

# Example usage
if __name__ == "__main__":
    pqc_instance = PostQuantumCryptography()
    pqc_instance.generate_keypair()
    pqc_instance.load_keys()

    message = "Hello, Quantum World!"
    encrypted_data = pqc_instance.encrypt(message)
    logging.info(f"Encrypted Data: {encrypted_data}")

    decrypted_message = pqc_instance.decrypt(encrypted_data)
    logging.info(f"Decrypted Message: {decrypted_message}")
