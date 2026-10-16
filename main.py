
from pathlib import Path

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


OUTPUT_DIR = Path("output")
PRIVATE_KEY_FILE = OUTPUT_DIR / "private_key.pem"
PUBLIC_KEY_FILE = OUTPUT_DIR / "public_key.pem"
ENCRYPTED_FILE = OUTPUT_DIR / "encrypted_message.bin"


def generate_keys():
    """Generate and save an RSA public/private key pair."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()

    PRIVATE_KEY_FILE.write_bytes(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )

    PUBLIC_KEY_FILE.write_bytes(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    )

    print("RSA key pair generated and saved.")
    return private_key, public_key


def load_keys():
    """Load the saved RSA keys."""
    private_key = serialization.load_pem_private_key(
        PRIVATE_KEY_FILE.read_bytes(),
        password=None,
    )
    public_key = serialization.load_pem_public_key(
        PUBLIC_KEY_FILE.read_bytes()
    )
    return private_key, public_key


def encrypt_message(message, public_key):
    """Encrypt a message with RSA-OAEP and SHA-256."""
    ciphertext = public_key.encrypt(
        message.encode("utf-8"),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    ENCRYPTED_FILE.write_bytes(ciphertext)
    return ciphertext


def decrypt_message(ciphertext, private_key):
    """Decrypt ciphertext with the RSA private key."""
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return plaintext.decode("utf-8")


def main():
    print("=== RSA Encryption and Decryption ===")
    print("1. Generate new keys")
    print("2. Load existing keys")

    choice = input("Choose an option (1 or 2): ").strip()

    if choice == "1":
        private_key, public_key = generate_keys()
    elif choice == "2":
        if not PRIVATE_KEY_FILE.exists() or not PUBLIC_KEY_FILE.exists():
            print("Error: Keys not found. Choose option 1 first.")
            return

        try:
            private_key, public_key = load_keys()
        except (ValueError, TypeError, OSError):
            print("Error: Could not load the saved keys.")
            return

        print("Existing keys loaded.")
    else:
        print("Error: Invalid option. Choose 1 or 2.")
        return

    message = input("Enter a short message to encrypt: ")

    if not message.strip():
        print("Error: Message cannot be empty.")
        return

    # RSA-2048 with OAEP and SHA-256 supports at most 190 bytes.
    if len(message.encode("utf-8")) > 190:
        print("Error: Message is too long. Maximum length is 190 bytes.")
        return

    try:
        ciphertext = encrypt_message(message, public_key)
        print("\nEncrypted message saved to:", ENCRYPTED_FILE)
        print("Ciphertext (hex):", ciphertext.hex())

        decrypted_message = decrypt_message(ciphertext, private_key)
        print("\nDecrypted message:", decrypted_message)

        if decrypted_message == message:
            print("SUCCESS: Decryption matches the original message.")
        else:
            print("ERROR: The decrypted message does not match.")

    except (ValueError, TypeError, OSError):
        print("Error: Encryption or decryption failed. Check the message and keys.")


if __name__ == "__main__":
    main()
