from flask import Flask, render_template, request, jsonify
import requests
import csv
import os
import uuid
from datetime import datetime


app = Flask(__name__)

# PSP Servers
psps = [
    "http://127.0.0.1:5001",
    "http://127.0.0.1:5002",
    "http://127.0.0.1:5003"
]

current = 0

# Create logs folder
os.makedirs("logs", exist_ok=True)

log_file = "logs/transactions.csv"

# Create CSV file if it doesn't exist
if not os.path.exists(log_file):
    with open(log_file, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Time",
            "Transaction ID",
            "Customer",
            "Amount",
            "Payment Method",
            "PSP",
            "Status",
            "Processing Time"
        ])


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/pay", methods=["POST"])
def pay():
    global current

    customer = request.form["customer"]
    amount = request.form["amount"]
    method = request.form["method"]
    account = request.form["account"]

    # Generate unique transaction ID
    transaction_id = "TXN" + uuid.uuid4().hex[:8].upper()

    attempts = 0

    while attempts < len(psps):

        psp = psps[current]
        psp_name = f"PSP{current + 1}"

        try:
            # Check PSP health
            health = requests.get(
                psp + "/health",
                timeout=1
            )

            if health.status_code == 200:

                print(f"Trying payment through {psp_name}")

                response = requests.get(
                    psp + "/pay",
                    timeout=6
                )

                data = response.json()

                # Payment Successful
                if data["payment"] == "SUCCESS":

                    print(
                        f"Payment Successful via {data['psp']}"
                    )

                    with open(
                        log_file,
                        "a",
                        newline=""
                    ) as file:

                        writer = csv.writer(file)

                        writer.writerow([
                            datetime.now().strftime("%H:%M:%S"),
                            transaction_id,
                            customer,
                            amount,
                            method,
                            data["psp"],
                            "SUCCESS",
                            data["processing_time"]
                        ])

                    # Move to next PSP for next payment
                    current = (current + 1) % len(psps)

                    return jsonify({
                        "transaction_id": transaction_id,
                        "customer": customer,
                        "amount": amount,
                        "method": method,
                        "psp": data["psp"],
                        "status": "SUCCESS",
                        "processing_time": data["processing_time"]
                    })

                # Payment Failed
                else:

                    print(
                        f"{data['psp']} returned FAILED. "
                        f"Trying next PSP..."
                    )

                    with open(
                        log_file,
                        "a",
                        newline=""
                    ) as file:

                        writer = csv.writer(file)

                        writer.writerow([
                            datetime.now().strftime("%H:%M:%S"),
                            transaction_id,
                            customer,
                            amount,
                            method,
                            data["psp"],
                            "FAILED",
                            data["processing_time"]
                        ])

            # Move to next PSP
            current = (current + 1) % len(psps)
            attempts += 1

        except requests.exceptions.RequestException:

            print(f"{psp_name} is DOWN")

            # Log unavailable PSP
            with open(
                log_file,
                "a",
                newline=""
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    datetime.now().strftime("%H:%M:%S"),
                    transaction_id,
                    customer,
                    amount,
                    method,
                    psp_name,
                    "UNAVAILABLE",
                    "-"
                ])

            # Try next PSP
            current = (current + 1) % len(psps)
            attempts += 1

    # All PSPs failed
    print("All PSPs failed or are unavailable")

    return jsonify({
        "transaction_id": transaction_id,
        "customer": customer,
        "amount": amount,
        "method": method,
        "status": "FAILED",
        "reason": "All PSPs failed or are unavailable"
    }), 503


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )