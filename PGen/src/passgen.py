import random
import string
from cryptography.fernet import Fernet
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Generate a key for encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Define the database model using the new declarative_base location
Base = declarative_base()


class Password(Base):
    __tablename__ = 'passwords'

    id = Column(Integer, primary_key=True)
    service = Column(String)
    username = Column(String)  # New column for storing the username
    encrypted_password = Column(String)


# Create the SQLite engine and session
engine = create_engine('sqlite:///passwords.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def generate_password(length, use_uppercase, use_digits, use_special):
    """Generate a random password based on user-defined rules."""
    characters = string.ascii_lowercase

    if use_uppercase:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def encrypt_password(password):
    """Encrypt the password."""
    encrypted_password = cipher_suite.encrypt(password.encode())
    return encrypted_password.decode()


def save_password(service, username, password):
    """Save the encrypted password to the database along with the service and username."""
    new_password = Password(service=service, username=username, encrypted_password=password)
    session.add(new_password)
    session.commit()
    print("Password saved successfully.")


def main():
    # Ask user for password rules
    length = int(input("Enter the desired password length: "))
    use_uppercase = input("Include uppercase letters? (y/n): ").strip().lower() == 'y'
    use_digits = input("Include digits? (y/n): ").strip().lower() == 'y'
    use_special = input("Include special characters? (y/n): ").strip().lower() == 'y'

    # Generate password
    generated_password = generate_password(length, use_uppercase, use_digits, use_special)
    print(f"Generated Password: {generated_password}")

    # Ask if the user wants to save this password
    save_it = input("Do you want to save this password? (y/n): ").strip().lower()
    if save_it == 'y':
        service_name = input("Enter the name of the service for which this password is used: ")
        username = input("Enter the username associated with this password: ")
        encrypted_password = encrypt_password(generated_password)
        save_password(service_name, username, encrypted_password)


if __name__ == "__main__":
    main()