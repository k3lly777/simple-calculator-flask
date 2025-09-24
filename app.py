from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- Basic arithmetic functions ---
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    # safe division: raise if dividing by zero
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

# --- Routes ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/calc", methods=["POST"])
def calculate():
    # expect JSON body: { num1: "...", num2: "...", op: "+" }
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Invalid request (no JSON)."}), 400

    # Validate inputs
    try:
        n1 = float(data.get("num1", ""))
        n2 = float(data.get("num2", ""))
    except Exception:
        return jsonify({"error": "Please provide valid numbers for num1 and num2."}), 400

    op = data.get("op", "")
    try:
        if op == "+":
            res = add(n1, n2)
        elif op == "-":
            res = subtract(n1, n2)
        elif op == "*":
            res = multiply(n1, n2)
        elif op == "/":
            try:
                res = divide(n1, n2)
            except ValueError:
                return jsonify({"error": "Division by zero is not allowed."}), 400
        else:
            return jsonify({"error": "Unsupported operation."}), 400

        # Return JSON result
        return jsonify({"result": res})
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500


if __name__ == "__main__":
    # debug=True is useful while developing; remove for production
    app.run(host="0.0.0.0", port=5000, debug=True)
