## Virtual Theme Park Operations Dashboard

This Virtual Theme Park Operations Dashboard is a full stack web application for managing ride operations in a simulated theme park. Users can view and update ride wait time, capacity, and operating statuses through a browser-based dashboard. The application uses a Flask REST API and SQLite database to persist operational data.

## Features

- View all rides
- Track wait times
- Track ride capacity
- Track operating status
- Update ride information
- Persist changes in SQLite
- Frontend and backend validation
- Error handling
- Status-based ride card styling

## Technologies used

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Git

## How It Works

The frontend is built with HTML, CSS, and JavaScript and retrieves ride information from the Flask backend using HTTP requests. Flask exposes API endpoints for reading and updating ride data, while SQLite stores the ride information so changes persist between page refreshes and application restarts.

## Installation and Setup

1. Clone the repository
    ```bash
    git clone<>
2. Navigate into the project directory
    ```bash
    cd theme-park-mvp
3. Create a virtual environment
    ```bash
    python -m venv venv
    venv/script.activate
4. Install requirements
    ```bash
    pip install -r requirements.txt
5. Run the Flask application
    ```bash
    python app.py
6. Open the local URL in a browser
    http://127.0.0.1:5000

## API Endpoints

GET /api/rides - Returns all rides stored in the database
PUT /api/rides/<ride_id> - Updates wait time, capacity, and operating status for a specific ride

## Project Structure

```text
theme-park-mvp/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
└── static/
    ├── script.js
    └── style.css
```

## Validation and Error Handling

- Wait time: 0 - 240
- Capacity: 1 - 100
- Operating Statuses: "Operating" | "Delayed" | "Closed"
- Invalid data types are rejected by the backend
- Requests for rides that do not exist return a 404 response
- Invalid input returns a 400 response
- Failed API and network requests are handled by the frontend

## Future Improvements

- PostgreSQL - Migrate from SQLite to PostgreSQL to support a more production-ready database environment
- Historical data tracking - Save each data update with a timestamp
- Analytics dashboard - Use stored historical data to calculate average wait time, busiest ride, peak operating hours, etc
- Automatic ride simulation - Simulate changing queue sizes, wait times, and operating statuses over time
- Authentication - Add login functionality so only authorized employees can update information
