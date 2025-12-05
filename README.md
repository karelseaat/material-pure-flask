 # Material Dashboard Lite - Backend

Welcome to the backend repository for Material Dashboard Lite, a free-to-use Material Design admin template based on Google's Material Design Lite library. This project aims to provide a responsive, cross-device compatible admin template with a dark theme, built using modern web technologies such as CSS (Scss), JavaScript (ES6), and HTML5.

## Features

- Implementation of Material Design via Material Design Lite (https://getmdl.io)
- Uses Flask web framework for the backend
- Includes user authentication and authorization with Flask-Login
- Form validations using WTForms
- Database interactions using SQLAlchemy

## Installation & Setup

1. Fork or clone this repository, then navigate to your local copy:
   ```bash
   git clone https://github.com/<your_username>/material-dashboard-lite-backend.git
   cd material-dashboard-lite-backend
   ```

2. Install project dependencies with pip:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your SQLAlchemy database configuration in `config.py`.

4. Run the Flask development server:
   ```bash
   export FLASK_APP=app.py && flask run --debugger
   ```

## Usage

The application includes routes for user registration, login, password recovery, and logout using Flask-Login. The forms are validated with WTForms, and database interactions are handled using SQLAlchemy. For a complete list of available routes and their corresponding views, please refer to the `app.py` file.

## Contributing

We welcome contributions to this project! If you find any issues or would like to suggest new features, please open an issue on our [GitHub repository](https://github.com/CreativeIT/material-dashboard-lite-backend/issues). Pull requests are also highly encouraged for code improvements and bug fixes.

## License

This project is licensed under the MIT license. For more information, please refer to the `LICENSE` file.

Enjoy using Material Dashboard Lite! If you find it helpful, don't forget to star the repository on GitHub.