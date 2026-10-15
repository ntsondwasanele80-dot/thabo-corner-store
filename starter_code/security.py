"""
security.py
------------
Task 6: A basic access-control gate for your sales reports.

This module covers KM-04 KT08: Data Security (the CIA triad —
Confidentiality, Integrity, Availability — and practical protections
like encryption / hashing and access control).

We are NOT building bank-grade security here — the goal is to
DEMONSTRATE that you understand why sensitive reports shouldn't be
open to anyone, and one simple way (password hashing) to protect them.

IMPORTANT SECURITY LESSON (this is the whole point of the task):
    NEVER store a password as plain text. Always store a HASH of the
    password. hashlib.sha256() is used below for learning purposes.
"""

import hashlib
import getpass


# In a real system this would live in a database, not in code.
# For this project, one hardcoded hash is fine — but note in your
# README why storing it in the database (KM-04 idea) would be better
# than hardcoding it here.
#
# The hash below is SHA-256 of the plain-text password "thabo2026".
# NEVER store the plain-text password itself.
STORED_PASSWORD_HASH = "303aab129dfebb892308f9419b69ba84fc5bddac3873066bbcf1b2b2c30fc842"


def hash_password(plain_text_password: str) -> str:
    """
    Turn a plain-text password into a SHA-256 hash (a fixed-length
    string of letters and numbers that CANNOT be reversed back into
    the original password).

    Args:
        plain_text_password: the password as typed by the user

    Returns:
        the hex-digest string of the SHA-256 hash
    """
    return hashlib.sha256(plain_text_password.encode()).hexdigest()


def check_password(attempt: str, stored_hash: str) -> bool:
    """
    Check whether a login attempt matches the stored hash — WITHOUT
    ever comparing plain-text passwords directly.

    Args:
        attempt: the plain-text password the user just typed
        stored_hash: the hash you saved earlier with hash_password()

    Returns:
        True if the attempt's hash matches stored_hash, False otherwise
    """
    return hash_password(attempt) == stored_hash


def login_gate(stored_hash: str, max_attempts: int = 3) -> bool:
    """
    Prompt the user for a password (hidden input, via getpass) and
    check it against stored_hash. Allow up to max_attempts tries.

    Returns:
        True if the user authenticated successfully, False if they
        ran out of attempts.
    """
    for attempt_number in range(max_attempts):
        attempt = getpass.getpass("Enter password to view reports: ")
        if check_password(attempt, stored_hash):
            print("Access granted.")
            return True
        else:
            print("Incorrect password. Try again.")

    print("Access denied — too many failed attempts.")
    return False


# ---------------------------------------------------------------------
# REFLECTION (answer in your README, not in code):
#
#   1. Confidentiality — how does this login gate support it?
#   2. Integrity — the login gate does NOT protect data integrity.
#      What in your database.py design (Task 3) helps with integrity
#      instead? (Hint: think about primary keys and data types.)
#   3. Availability — what is one risk to availability for a project
#      like this stored only on your own laptop, and what would you
#      recommend to protect against it?
# ---------------------------------------------------------------------