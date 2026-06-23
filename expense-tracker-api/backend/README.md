# Expense Tracker API

A simple backend API for tracking personal expenses. Built with Python and Flask. Data is stored in memory using a Python list, so it resets every time the server restarts — there's no database involved.

This was built as Project 2 for the DecodeLabs Full Stack internship track, focused on backend API design: routing, request validation, and proper HTTP status codes.

## Features

- Health check endpoint
- List all expenses
- Create a new expense (with validation)
- Get a single expense by id
- Update an expense
- Delete an expense
- Summary endpoint that returns total count and total amount spent

## Tech stack

- Python 3.8+
- Flask

## Setup

1. Clone or download this project, then move into the folder.

2. (Recommended) Create a virtual environment.

   On Windows:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

   On macOS/Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the server:
   ```bash
   python app.py
   ```

The API will be running at `http://127.0.0.1:5000`.

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/status` | Check if the API is running |
| GET | `/api/expenses` | Get all expenses |
| POST | `/api/expenses` | Create a new expense |
| GET | `/api/expenses/<id>` | Get one expense by id |
| PUT | `/api/expenses/<id>` | Update an expense (full payload required) |
| DELETE | `/api/expenses/<id>` | Delete an expense |
| GET | `/api/expenses/summary` | Get total count and total amount |

## Expense object

```json
{
  "id": 1,
  "title": "Lunch",
  "amount": 12.5,
  "category": "Food",
  "date": "2026-06-23"
}
```

- `id` – assigned automatically, can't be set by the client
- `title` – required, can't be blank
- `amount` – required, must be a number greater than 0
- `category` – required, can't be blank
- `date` – optional. If you don't send one, it's stored as an empty string (not left out of the response)

These rules apply to both creating (POST) and updating (PUT) an expense.

## Examples

**Health check**

```http
GET /api/status
```
```json
{ "message": "Expense Tracker API is running" }
```

**Create an expense**

```http
POST /api/expenses
Content-Type: application/json

{
  "title": "Lunch",
  "amount": 12.5,
  "category": "Food",
  "date": "2026-06-23"
}
```

Returns `201` on success:
```json
{
  "message": "Expense created successfully",
  "expense": {
    "id": 1,
    "title": "Lunch",
    "amount": 12.5,
    "category": "Food",
    "date": "2026-06-23"
  }
}
```

If a required field is missing, you get a `400` instead, e.g.:
```json
{ "error": "Title is required" }
```

**Get all expenses**

```http
GET /api/expenses
```

When there's nothing yet:
```json
{ "message": "No expenses found", "expenses": [] }
```

Otherwise:
```json
{
  "expenses": [
    {
      "id": 1,
      "title": "Lunch",
      "amount": 12.5,
      "category": "Food",
      "date": "2026-06-23"
    }
  ]
}
```

**Get a single expense**

```http
GET /api/expenses/1
```
```json
{
  "expense": {
    "id": 1,
    "title": "Lunch",
    "amount": 12.5,
    "category": "Food",
    "date": "2026-06-23"
  }
}
```

If the id doesn't exist, returns `404`:
```json
{ "error": "Expense not found" }
```

**Update an expense**

```http
PUT /api/expenses/1
Content-Type: application/json

{
  "title": "Groceries",
  "amount": 150.5,
  "category": "Food",
  "date": "2026-06-24"
}
```

Returns `200` on success:
```json
{
  "message": "Expense updated successfully",
  "expense": {
    "id": 1,
    "title": "Groceries",
    "amount": 150.5,
    "category": "Food",
    "date": "2026-06-24"
  }
}
```

PUT expects the full object, same as POST — partial updates aren't supported.

**Delete an expense**

```http
DELETE /api/expenses/1
```
```json
{ "message": "Expense deleted successfully" }
```

**Summary**

```http
GET /api/expenses/summary
```
```json
{ "total_expenses": 2, "total_amount": 163.0 }
```

## Status codes used

| Code | Meaning |
|------|-------------------|
| 200  | Request succeeded |
| 201  | Expense created |
| 400  | Bad request — missing/invalid fields, or bad JSON |
| 404  | Expense or route not found |

## Limitations

- Everything is stored in memory, so restarting the server clears all data
- No database, no authentication, no external services
- Built for learning/practice, not production use

## Possible next steps

- Add a database (SQLite/Postgres) for persistence
- Filtering expenses by category or date range
- Pagination for large lists
- Basic auth if this ever needs to be multi-user

