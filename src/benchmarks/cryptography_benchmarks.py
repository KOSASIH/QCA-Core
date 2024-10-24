# src/benchmarks/cryptography_benchmarks.py

import time
import memory_profiler
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
import numpy as np
import concurrent.futures
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class CryptographyBenchmarks:
    def __init__(self, key_size=16, rsa_key_size=2048):
        self.key_size = key_size
        self.rsa_key_size = rsa_key_size
        self.aes_key = get_random_bytes(self.key_size)
        self.rsa_key = RSA.generate(self.rsa_key_size)
        self.cipher_aes = AES.new(self.aes_key, AES.MODE_EAX)

    @memory_profiler.profile
    def benchmark_aes_encryption(self, data):
        """Benchmark AES encryption."""
        start_time = time.time()
        ciphertext, tag = self.cipher_aes.encrypt_and_digest(data)
        end_time = time.time()
        return end_time - start_time, len(ciphertext)

    @memory_profiler.profile
    def benchmark_aes_decryption(self, ciphertext):
        """Benchmark AES decryption."""
        start_time = time.time()
        cipher = AES.new(self.aes_key, AES.MODE_EAX, nonce=self.cipher_aes.nonce)
        plaintext = cipher.decrypt(ciphertext)
        end_time = time.time()
        return end_time - start_time

    @memory_profiler.profile
    def benchmark_rsa_encryption(self, data):
        """Benchmark RSA encryption."""
        start_time = time.time()
        ciphertext = self.rsa_key.encrypt(data, None)[0]
        end_time = time.time()
        return end_time - start_time, len(ciphertext)

    @memory_profiler.profile
    def benchmark_rsa_decryption(self, ciphertext):
        """Benchmark RSA decryption."""
        start_time = time.time()
        plaintext = self.rsa_key.decrypt(ciphertext)
        end_time = time.time()
        return end_time - start_time

    @memory_profiler.profile
    def benchmark_sha256(self, data):
        """Benchmark SHA-256 hashing."""
        start_time = time.time()
        hash_object = SHA256.new(data)
        hash_value = hash_object.hexdigest()
        end_time = time.time()
        return end_time - start_time, hash_value

    def run_benchmarks(self, data):
        """Run all benchmarks in parallel and log results."""
        results = {}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_aes_enc = executor.submit(self.benchmark_aes_encryption, data)
            future_aes_dec = executor.submit(self.benchmark_aes_decryption, data)
            future_rsa_enc = executor.submit(self.benchmark_rsa_encryption, data)
            future_rsa_dec = executor.submit(self.benchmark_rsa_decryption, data)
            future_sha256 = executor.submit(self.benchmark_sha256, data)

            results['AES Encryption'] = future_aes_enc.result()
            results['AES Decryption'] = future_aes_dec.result()
            results['RSA Encryption'] = future_rsa_enc.result()
            results['RSA Decryption'] = future_rsa_dec.result()
            results['SHA-256'] = future_sha256.result()

        # Log results
        for algorithm, (time_taken, size) in results.items():
            logging.info(f"{algorithm} - Time: {time_taken:.6f} seconds, Size: {size if size else 'N/A'} bytes")

# Example usage
if __name__ == "__main__":
    benchmark = CryptographyBenchmarks()
    data = get_random_bytes(1024)  # 1 KB of random data
    benchmark.run_benchmarks(data)
