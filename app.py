from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)


def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    return gcd, y1, x1 - (a // b) * y1


def mod_inverse(e, phi):
    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        return None
    return x % phi


def mod_pow(base, exponent, modulus):
    result = 1
    base %= modulus
    steps = []

    while exponent > 0:
        steps.append({
            "result": result,
            "base": base,
            "exponent": exponent
        })
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent //= 2

    return result, steps


def choose_e(phi):
    e = 3
    while e < phi:
        if math.gcd(e, phi) == 1:
            return e
        e += 2
    return None


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/api/generate")
def generate():
    data = request.get_json()
    try:
        p = int(data["p"])
        q = int(data["q"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Enter two prime numbers."}), 400

    if not is_prime(p) or not is_prime(q):
        return jsonify({"error": "Both p and q must be prime numbers."}), 400
    if p == q:
        return jsonify({"error": "Choose two different prime numbers."}), 400

    n = p * q
    phi = (p - 1) * (q - 1)
    e = choose_e(phi)
    d = mod_inverse(e, phi)

    return jsonify({
        "p": p,
        "q": q,
        "n": n,
        "phi": phi,
        "e": e,
        "d": d
    })


@app.post("/api/encrypt")
def encrypt():
    data = request.get_json()
    try:
        message = int(data["message"])
        e = int(data["e"])
        n = int(data["n"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Enter valid numeric values."}), 400

    if message < 0 or message >= n:
        return jsonify({"error": "The message must satisfy 0 ≤ m < n."}), 400

    ciphertext, steps = mod_pow(message, e, n)
    return jsonify({"ciphertext": ciphertext, "steps": steps})


@app.post("/api/decrypt")
def decrypt():
    data = request.get_json()
    try:
        ciphertext = int(data["ciphertext"])
        d = int(data["d"])
        n = int(data["n"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Enter valid numeric values."}), 400

    message, steps = mod_pow(ciphertext, d, n)
    return jsonify({"message": message, "steps": steps})


if __name__ == "__main__":
    app.run(debug=True)
