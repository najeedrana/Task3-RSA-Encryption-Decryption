
# RSA Encryption and Decryption System

## 1. Project Description

This project implements an RSA encryption and decryption system in Python. It demonstrates asymmetric cryptography, where a public key is used to encrypt a message and a private key is used to decrypt it.

The program uses the Python `cryptography` library.

## 2. Features

- Generate a 2048-bit RSA public and private key pair.
- Save and load RSA keys in PEM format.
- Encrypt short text messages using the public key.
- Decrypt ciphertext using the private key.
- Use OAEP padding with SHA-256.
- Save encrypted messages as binary files.
- Validate menu choices and reject empty messages.
- Check the message size before encryption.
- Confirm that the decrypted message matches the original.

## 3. Technologies

- Python 3
- `cryptography` library
- RSA public-key cryptography
- OAEP padding
- SHA-256

## 4. Installation

Install Python 3, then install the required library:

```bash
python -m pip install cryptography
```

## 5. How to Run

Run the program from the project directory:

```bash
python main.py
```

Choose option 1 to generate new keys or option 2 to load existing keys. Enter a short message when prompted.

The program displays the ciphertext and the decrypted message, then reports whether decryption matches the original.

## 6. Output Files

The program creates an `output` directory containing:

- `private_key.pem` — the RSA private key.
- `public_key.pem` — the RSA public key.
- `encrypted_message.bin` — the encrypted message.

These files are generated when the program runs.

## 7. How RSA Works

RSA is an asymmetric cryptographic algorithm that uses a public key and a private key.

The public key can be shared and is used for encryption. The private key must be kept secret and is used for decryption.

This program uses RSA with a 2048-bit key and OAEP padding with SHA-256. For this configuration, the maximum plaintext size for direct RSA encryption is 190 bytes.

## 8. Testing

The program was tested with:

- Generating a new key pair.
- Encrypting and decrypting `Hello RSA`.
- Loading existing keys and encrypting another message.
- Rejecting an empty message.
- Checking longer messages against the RSA plaintext-size limit.

Successful tests confirm that the decrypted text matches the original message.

## 9. Limitations and Security Notes

- RSA can encrypt only relatively short messages directly.
- The private key is saved without password protection for this educational demonstration.
- The generated private key should not be shared or committed to a public repository.
- This program is intended for learning and is not a complete production encryption system.

## 10. Author

Information Security coursework project.
