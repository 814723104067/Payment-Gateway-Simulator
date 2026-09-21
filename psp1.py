from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

# Health Check
@app.route("/health")
def health():
    return jsonify({
        "status": "UP",
        "psp": "PSP1"
    })

# Payment Endpoint
@app.route("/pay")
def pay():

    print("Payment request received by PSP1")

    delay = random.randint(1, 3)
    time.sleep(delay)

    # 95% Success
    if random.randint(1, 100) <= 95:
        status = "SUCCESS"
    else:
        status = "FAILED"

    return jsonify({
        "psp": "PSP1",
        "payment": status,
        "processing_time": f"{delay} seconds"
    })


@app.route("/")
def home():
    return "PSP1 Server Running"


if __name__ == "__main__":
    app.run(port=5001)