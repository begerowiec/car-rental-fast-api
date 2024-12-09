# Car Rental API

Welcome to the **Car Rental API** repository! This project showcases a RESTful API designed for a car rental service. The API provides endpoints for managing car rentals, customers, and bookings, making it an ideal solution for learning, testing, or implementing a car rental system.

## Features

- **RESTful API**: Built with scalability and simplicity in mind.
- **Endpoint Testing**: Comprehensive tests for all API endpoints using **Postman** in JavaScript.
- **Database Integration**: Supports CRUD operations for customers, cars, and bookings.
- **Modular Structure**: Easy to extend and adapt for other use cases.

---

## Getting Started

Follow the steps below to set up the project on your local machine.

### Prerequisites

1. **Python**: Ensure Python 3.8 or higher is installed.
2. **Postman**: For endpoint testing.
3. **Database**: A database setup (e.g., MySQL, MongoDB, or SQLite, depending on the project configuration).
4. **Git**: To clone the repository.

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/car-rental-api.git
   cd car-rental-api
   ```
2. **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
4. **Set Up Environment Variables Create a .env file in the project root and configure the following variables:**
    ```bash
    URL_DATABASE = your_database_host
    ```
5. **Run Database Migrations If using a framework like Django, apply migrations:**
    ```bash
    python manage.py migrate
    ```
6. **Run the API**
    ```bash
    uvicorn main:app --reload
    ```
    The API will start running on the configured port (default: http://localhost:8000).

## Testing the Endpoints

Comprehensive endpoint tests are included in the /test folder. The tests are written in JavaScript and are designed to run in Postman.

### Running the Tests
1. **Open Postman.**
2. **Import the CarRentalAPI_TestCollection.json file located in the /test folder.**
3. **Run the test collection to validate the API's functionality**

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue to discuss potential improvements.

Start exploring the API and feel free to customize it to fit your needs. Happy coding! 🚗✨