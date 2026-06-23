from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest

# Initialize Flask application
app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False  # Keep JSON output order predictable

# In-memory storage for expenses
expenses = []  # List to hold expense objects
_next_id = 1   # Simple incremental id generator


def _get_next_id():
    """Return the next unique id for a new expense."""
    global _next_id
    nid = _next_id
    _next_id += 1
    return nid


def _find_expense(expense_id):
    """Return an expense by id or None if not found."""
    return next((e for e in expenses if e["id"] == expense_id), None)


def _validate_expense_data(data):
    """Validate incoming expense JSON payload.

    Returns: (is_valid: bool, error_message: str | None)
    """
    if not isinstance(data, dict):
        return False, "Invalid JSON data"

    # Title validation
    title = data.get("title")

    if title is None:
        return False, "Title is required"

    if not isinstance(title, str):
        return False, "Title must be text"

    if title.strip() == "":
        return False, "Title is required"
    # Amount validation
    amount = data.get("amount")
    if amount is None or str(amount).strip() == "":
        return False, "Amount is required"
    try:
        amount_val = float(amount)
    except (ValueError, TypeError):
        return False, "Amount must be a number"
    if amount_val <= 0:
        return False, "Amount must be greater than zero"

    # Category validation
    category = data.get("category")

    if category is None:
        return False, "Category is required"

    if not isinstance(category, str):
        return False, "Category must be text"

    if category.strip() == "":
        return False, "Category is required"

    return True, None


# Health check
@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({"message": "Expense Tracker API is running"}), 200


# Get all expenses
@app.route("/api/expenses", methods=["GET"])
def get_expenses():
    if not expenses:
        return jsonify({"message": "No expenses found", "expenses": []}), 200
    return jsonify({"expenses": expenses}), 200


# Create a new expense
@app.route("/api/expenses", methods=["POST"])
def create_expense():
    # Parse JSON safely and return friendly error when invalid
    try:
        data = request.get_json()
    except BadRequest:
        return jsonify({"error": "Invalid JSON data"}), 400

    if data is None:
        return jsonify({"error": "Invalid JSON data"}), 400

    # Validate payload
    valid, error_msg = _validate_expense_data(data)
    if not valid:
        return jsonify({"error": error_msg}), 400

    # Build expense object
    expense = {
        "id": _get_next_id(),
        "title": str(data.get("title")).strip(),
        "amount": float(data.get("amount")),
        "category": str(data.get("category")).strip(),
        "date": str(data.get("date")) if data.get("date") is not None else ""
    }

    expenses.append(expense)
    return jsonify({"message": "Expense created successfully", "expense": expense}), 201


# Get single expense by id
@app.route("/api/expenses/<int:expense_id>", methods=["GET"])
def get_expense(expense_id):
    expense = _find_expense(expense_id)
    if expense is None:
        return jsonify({"error": "Expense not found"}), 404
    return jsonify({"expense": expense}), 200


# Delete expense by id
@app.route("/api/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    expense = _find_expense(expense_id)
    if expense is None:
        return jsonify({"error": "Expense not found"}), 404
    expenses.remove(expense)
    return jsonify({"message": "Expense deleted successfully"}), 200


# Update an existing expense
@app.route("/api/expenses/<int:expense_id>", methods=["PUT"])
def update_expense(expense_id):
    # Parse JSON safely
    try:
        data = request.get_json()
    except BadRequest:
        return jsonify({"error": "Invalid JSON data"}), 400

    if data is None:
        return jsonify({"error": "Invalid JSON data"}), 400

    expense = _find_expense(expense_id)
    if expense is None:
        return jsonify({"error": "Expense not found"}), 404

    # Validate incoming data using existing validation function
    valid, error_msg = _validate_expense_data(data)
    if not valid:
        return jsonify({"error": error_msg}), 400

    # Update fields
    expense["title"] = str(data.get("title")).strip()
    expense["amount"] = float(data.get("amount"))
    expense["category"] = str(data.get("category")).strip()
    expense["date"] = str(data.get("date")) if data.get("date") is not None else expense.get("date", "")

    return jsonify({"message": "Expense updated successfully", "expense": expense}), 200


# Summary endpoint: total count and total amount
@app.route("/api/expenses/summary", methods=["GET"])
def expenses_summary():
    total_expenses = len(expenses)
    total_amount = sum((e.get("amount") or 0) for e in expenses)
    return jsonify({"total_expenses": total_expenses, "total_amount": total_amount}), 200


# Error handler for 404 routes
@app.errorhandler(404)
def handle_404(e):
    return jsonify({"error": "Route not found"}), 404


# Error handler for invalid JSON (BadRequest)
@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify({"error": "Invalid JSON data"}), 400


if __name__ == "__main__":
    # Run server on localhost:5000
    app.run(host="127.0.0.1", port=5000, debug=False)
