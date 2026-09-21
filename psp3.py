from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

# Health Check
@app.route("/health")
def health():
    return jsonify({
        "status": "UP",
        "psp": "PSP3"
    })

# Payment Endpoint
@app.route("/pay")
def pay():

    print("Payment request received by PSP3")

    delay = random.randint(3, 5)
    time.sleep(delay)

    # 60% Success
    if random.randint(1, 100) <= 60:
        status = "SUCCESS"
    else:
        status = "FAILED"

    return jsonify({
        "psp": "PSP3",
        "payment": status,
        "processing_time": f"{delay} seconds"
    })

# Home Page
@app.route("/")
def home():
    return "PSP3 Server Running"

if __name__ == "__main__":
    app.run(port=5003)