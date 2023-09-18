# Garrire

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0.0-green)
![Socket.IO](https://img.shields.io/badge/Socket.IO-4.0.1-yellow)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13.0-orange)
![License](https://img.shields.io/badge/License-MIT-red)

Garrire is a real-time chat application API built using Python, Flask, SocketIO, and PostgreSQL. It provides user creation and authentication using JWT, as well as the ability to join multiple chat rooms. This README will guide you through the setup and usage of the Garrire API.

## Getting Started

### Prerequisites

Before you can use the Garrire API, you'll need to have the following dependencies installed:

- Python
- PostgreSQL
- RabbitMQ (for the bot)

### Installation

1. Clone the Garrire repository:
   
```bash
git clone https://github.com/YourUsername/garrire.git
cd garrire
```

2. Set up the PostgreSQL database. Create a database named jobsitychatdb, and configure the database connection in the db.py file.
3. Start the RabbitMQ service for the bot. Make sure it's accessible and running on the specified host and port.
4. Start the Garrire API:
   
```bash
python garrire.py
```

Now, the Garrire API should be running on http://localhost:5000.

## Usage

### Endpoints
Garrire provides the following API endpoints:

- /message (POST): Send messages to chat rooms.
- /login (POST): Log in with a username and password.
- /signup (POST): Create a new user account.
- /users/<username> (GET, DELETE): Query or delete user accounts.
- /rooms (GET): List available chat rooms.
- /rooms/<room> (GET): Enter a chat room and view messages.

### Authentication
Garrire uses JWT-based authentication for protected endpoints. To authenticate, you need to obtain a JWT token by logging in with a valid username and password. You can then include this token in the Authorization header of your requests to access protected endpoints.

Here's an example of how to obtain a JWT token:

```bash
curl -X POST -d "username=your_username&password=your_password" http://localhost:5000/login
```

Include the token in subsequent requests like this:

```bash
curl -H "Authorization: Bearer your_token" http://localhost:5000/protected-endpoint
```
