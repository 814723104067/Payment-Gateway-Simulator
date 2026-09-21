from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

# Health Check
@app.route("/health")
def health():
    return jsonify({
        "status": "UP",
        "psp": "PSP2"
    })

# Payment Endpoint
@app.route("/pay")
def pay():

    print("Payment request received by PSP2")

    delay = random.randint(2, 4)
    time.sleep(delay)

    # 80% Success
    if random.randint(1, 100) <= 80:
        status = "SUCCESS"
    else:
        status = "FAILED"

    return jsonify({
        "psp": "PSP2",
        "payment": status,
        "processing_time": f"{delay} seconds"
    })

# Home Page
@app.route("/")
def home():
    return "PSP2 Server Running"

if __name__ == "__main__":
    app.run(port=5002)