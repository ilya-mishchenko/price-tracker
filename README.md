## Price Tracker API

A REST API for tracking product prices over time, built with FastAPI and PostgreSQL.
Users can add products by URL, set a target price, manually refresh the current price, and view the full price history for any product.

## FEATURES

- Add and manage products with a target price
- Full price history per product
- Manual price refresh via scraper endpoint
- Paginated product listing

<img width="200" height="275" alt="cards (1)" src="https://github.com/user-attachments/assets/b69fb951-ba41-4346-b7e7-572271deeb18" />

## Limitations

Price scraping uses a generic CSS class heuristic — it searches for HTML elements whose class name contains the word price.

## Project Structure

```
app/
├── api/          # route handlers
├── db/           # SQLAlchemy models and database config
├── schemas/      # Pydantic request/response schemas
├── services/     # business logic
alembic/          # database migrations
```

## Installation

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies from requirements.txt
```
pip install -r requirements.txt
```
4. Configure environment variables
Create a .env file in the project root:
```
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=price_tracker
```
5. Run database migrations
6. Start the server

## API Endpoints


| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/products` | List all products (paginated) |
| `POST` | `/products` | Add a new product |
| `GET` | `/products/{id}` | Get a product by ID |
| `PATCH` | `/products/{id}` | Update target price |
| `DELETE` | `/products/{id}` | Delete a product |
| `POST` | `/products/{id}/refresh` | Scrape and update current price |
| `GET` | `/products/{id}/history` | Get full price history |
| `GET` | `/health` | Health check |
```
