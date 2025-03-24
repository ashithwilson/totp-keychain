# TOTP Keychain

A simple Python script to generate TOTP (Time-Based One-Time Password) codes using secrets stored in the macOS Keychain.

## Why Use This?
- Minimal and easy-to-use OTP generator.
- Uses macOS Keychain for secure secret storage.
- Ideal for quickly generating OTP codes for services like Okta.

## Installation
### Requirements
- Python 3.7+
- macOS (Keychain support required)

### Usage

#### Store a Secret in Keychain

Before generating OTPs, store your secret in the macOS Keychain:

```console
security add-generic-password -s "SERVICE_NAME" -a "ACCOUNT_NAME" -w "SECRET_KEY" -U
```

Example:

```console
security add-generic-password -s "okta_totp" -a "okta" -w "MYSECRETKEY" -U
```

#### Generate an OTP

Run the script with your service and account name:

```console
python totp-keychain.py --service SERVICE_NAME --account ACCOUNT_NAME
```

Example:

```console
python totp-keychain.py --service okta_totp --account okta
```

This will output a 6-digit TOTP code.

## Notes

This script is designed specifically for macOS Keychain.

For a more feature-rich CLI, check out [totp-cli](https://github.com/yitsushi/totp-cli).
