# URL Shortener with Expiry and Analytics

This project is a simple URL shortener that allows users to shorten URLs, set expiration times, and track analytics (such as access logs). It is built using Python's FastAPI framework and integrates with a database for storing URLs and logs.

## Features

- Shorten URLs with a custom expiration time.
- Redirect users to the original URL when accessing the shortened URL.
- Log access analytics (IP address, access time, etc.).
- Support for expired URLs and password protection (optional).

## Prerequisites

Before setting up the project, make sure you have the following installed:

- Python 3.8 or higher
- pip (Python's package installer)

## Setup Instructions

### 1. Clone the repository

Clone the repository to your local machine:

```bash
git clone https://github.com/Bharath-Bhonsle/short_url_app.git
cd your-repository-name
```

### 2. Set up a virtual environment

Create a virtual environment to isolate your project dependencies. You can use venv to create the environment.

- On Windows:


```bash
 python -m venv venv
 ```

- On macOS/Linux:

```bash
 python3 -m venv venv
 ```

### 3. Activate the virtual environment

- On Windows:

```bash
 .\venv\Scripts\activate
```
- On macOS/Linux:
```bash
source venv/bin/activate
```


### 4. Install the required dependencies

Once the virtual environment is activated, install the required dependencies using requirements.txt.
```bash 
 pip install -r requirements.txt
```

This will install all the necessary Python libraries, including FastAPI, SQLAlchemy, etc.

### 5. Set up the Database

Ensure your database is properly set up and configured in the project. The project uses SQLAlchemy for database interactions. Update the database URL in the database.py file as per your database setup.

Example:

- For a SQLite database:

 ```bash
 DATABASE_URL = "sqlite:///./url_shortener.db"
  ```

### 6. Run the FastAPI Application

To start the FastAPI application, run the following command:

```bash
uvicorn app.main:app --reload  
``` 

This will start the development server. You can access the application in your browser at http://127.0.0.1:8000.

## Testing the API Endpoints

Once your FastAPI application is running, you can test the API endpoints using any HTTP client like Postman or cURL.

Alternatively, FastAPI provides an interactive API documentation interface at:

-> [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

You can test the following endpoints from the documentation interface:

### `POST /shorten` - Shorten a URL and set an expiration time.

#### Example Request:

**Body:**
```json
{
  "original_url": "https://example.com",
  "expires_in": 36,
  "password": "yourpassword"
}
```

- original_url: The URL to be shortened.
- expires_in: The expiration time in hours.
- password: (Optional) A password to protect the shortened URL.
**Example Response:**
```json 
{
  "original_url": "https://example.com",
  "short_url": "https://short.ly/abc123",
  "expires_at": "2025-01-20T10:00:00"
}
```

- original_url: The original URL you provided.
- short_url: The shortened URL.
- expires_at: The expiration date and time for the shortened

**Notes:**
- Make sure to include the original_url in the request body.
- The password is optional but can be used to secure the shortened link.

### `GET /{short_url}` - Redirect to the original URL using the shortened URL.

#### Example Request:
```bash 
 URL: http://127.0.0.1:8000/abc123
```

#### Example Response:
```bash
Redirects to the original URL: https://example.com
 ```
##### Testing Expiry and Analytics:
```bash
- GET /{short_url} after the expiration time has passed will return a 410 Gone status.
- You can also track IP access logs in the database after each access request.
```
These steps will allow you to test the functionality of your URL shortener and ensure everything works as expected.

### `GET/analytics/{short_url}` - This endpoint returns the access count and a list of access logs, including the IP address and the timestamp of each access, for a given shortened URL.

#### Example Request:
```bash 
 URL: http://127.0.0.1:8000/analytics/abc123
```
#### Example Response:
```json
{
  "short_url": "abc123",
  "access_count": 3,
  "logs": [
    {
      "accessed_at": "2025-01-20T10:00:00",
      "ip_address": "192.168.1.1"
    },
    {
      "accessed_at": "2025-01-20T10:05:00",
      "ip_address": "192.168.1.2"
    },
    {
      "accessed_at": "2025-01-20T10:10:00",
      "ip_address": "192.168.1.3"
    }
  ]
}

```
This endpoint helps you track the usage and access statistics of the shortened URLs, making it easier to analyze user interactions.