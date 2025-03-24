#!/usr/bin/env python3
"""
Retrieve and generate a TOTP code using a secret stored in macOS Keychain.

Info:
    To store a new secret in Keychain:
    security add-generic-password -s "SERVICE_NAME" -a "ACCOUNT_NAME" -w "SECRET_KEY" -U

Note:
    - This script is a minimal OTP generator supporting only macOS Keychain.
    - For more advanced use cases, try `totp-cli`.
"""

import base64
import struct
import hmac
import hashlib
import time
import subprocess
import sys
import argparse


def get_secret_from_keychain(service: str, account: str) -> str:
    """Retrieve the secret from macOS Keychain using the `security` command."""
    try:
        result = subprocess.run(
            ["security", "find-generic-password",
                "-s", service, "-a", account, "-w"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(
            f"Error retrieving secret from Keychain: {e.stderr.strip()}", file=sys.stderr)
        sys.exit(1)


def generate_hotp(secret: str, counter: int) -> str:
    """Generate an HOTP token based on the given secret and counter."""
    try:
        key = base64.b32decode(secret, casefold=True)
    except base64.binascii.Error:
        print("Invalid base32-encoded secret.", file=sys.stderr)
        sys.exit(1)

    msg = struct.pack(">Q", counter)
    hmac_digest = hmac.new(key, msg, hashlib.sha1).digest()
    offset = hmac_digest[19] & 0xF
    code = (struct.unpack(
        ">I", hmac_digest[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000
    return f"{code:06d}"


def generate_totp(secret: str) -> str:
    """Generate a TOTP token based on the current time."""
    return generate_hotp(secret, counter=int(time.time()) // 30)


def main():
    """Main execution function."""

    parser = argparse.ArgumentParser(
        description="Generate a TOTP code using a secret from macOS Keychain.")
    parser.add_argument("--service", "-s", required=True,
                        help="The service name in Keychain.")
    parser.add_argument("--account", "-a", required=True,
                        help="The account name in Keychain.")

    args = parser.parse_args()

    secret = get_secret_from_keychain(args.service, args.account)
    print(generate_totp(secret))


if __name__ == "__main__":
    main()
