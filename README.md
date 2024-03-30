
# FastAPI User Authentication API

This is a simple FastAPI-based RESTful API for user authentication using JWT tokens and email verification. The API provides endpoints for user registration, JWT token generation, and token refresh.

## Setup

1. Clone the repository:
   \`\`\`bash
   git clone https://github.com/your_username/fastapi-user-authentication.git
   cd fastapi-user-authentication
   \`\`\`

2. Install dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. Set environment variables:
   Create a \`.env\` file in the root directory and add the following variables:
   \`\`\`dotenv
   PORT=8000
   \`\`\`

## Usage

1. Start the FastAPI server:
   \`\`\`bash
   uvicorn main:app --reload
   \`\`\`

2. Open your browser or API client (e.g., Postman) and access the following endpoints:

   - \`POST /addUser\`: Register a new user.
     - Request Body:
       \`\`\`json
       {
         "username": "example_user",
         "password": "strong_password",
         "email": "user@example.com"
       }
       \`\`\`
     - Response:
       \`\`\`json
       {
         "message": "User registered successfully. Please check your email for verification."
       }
       \`\`\`

   - \`POST /getJwt\`: Generate a JWT token for authentication.
     - Request Body:
       \`\`\`json
       {
         "username": "example_user",
         "password": "strong_password"
       }
       \`\`\`
     - Response:
       \`\`\`json
       {
         "access_token": "your_access_token",
         "token_type": "bearer"
       }
       \`\`\`

   - \`POST /refresh\`: Refresh an existing JWT token.
     - Request Header:
       \`\`\`
       Authorization: Bearer your_refresh_token
       \`\`\`
     - Response:
       \`\`\`json
       {
         "message": "Token refreshed successfully."
       }
       \`\`\`

## Dependencies

- [FastAPI](https://fastapi.tiangolo.com/): A modern web framework for building APIs with Python.
- [uvicorn](https://www.uvicorn.org/): ASGI server implementation to run FastAPI applications.
- Other dependencies are listed in \`requirements.txt\`.

## Contributing

1. Fork the repository.
2. Create a new branch (\`git checkout -b feature/your-feature\`).
3. Commit your changes (\`git commit -am 'Add new feature'\`).
4. Push to the branch (\`git push origin feature/your-feature\`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
EOF
