# RSA Cryptography Lab

An interactive RSA encryption and decryption application built with Python and Flask.

## Overview

RSA is a public-key cryptosystem based on number theory. This project makes the underlying algorithms visible through an interactive web application.

Users can generate an RSA key pair, encrypt a numeric message, decrypt the resulting ciphertext, and inspect the modular exponentiation steps used during the calculation.

## Features

- RSA key generation from two prime numbers
- Prime-number validation
- Euler's totient function
- Greatest common divisor and modular inverse
- RSA encryption and decryption
- Repeated-squaring modular exponentiation
- Step-by-step calculation display
- Input validation
- Python Flask backend
- Interactive browser interface

## How RSA Works

For two primes `p` and `q`:

```text
n = p × q
φ(n) = (p - 1)(q - 1)