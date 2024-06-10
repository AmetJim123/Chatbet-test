# ChatBet-Test

This project is a test for the ChatBet startup. It's a simple CRUD application for users, featuring a login and registration form. Users can create, read, update, and delete users. The login generates a token with JWT, and the user cannot access the CRUD operations without the token. The project also includes batch processing functions and uses Docker Compose for database management.

## Requirements

- Docker and Docker Compose installed on your machine
- MySQL Workbench or any other database manager to interact with the database (optional)

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/AmetJim123/Chatbet-test
    ```
2. **Navigate to the project directory:**
    ```bash
    cd Chatbet-test
    ```
3. **Run Docker Compose:**
    ```bash
    docker-compose up --build
    ```
4. **If the above command doesn't work, try:**
    ```bash
    sudo docker-compose up --build
    ```

## Usage

1. Once Docker Compose is running, open your browser and visit:
    ```
    http://localhost:3000
    ```
2. Thanks to FastAPI, you can access the automatically generated API documentation at:
    ```
    http://localhost:8000/docs
    ```

## Contributing

1. **Create a new branch:**
    ```bash
    git checkout -b nueva-funcionalidad
    ```
2. **Commit your changes:**
    ```bash
    git commit -am 'Agrega nueva funcionalidad'
    ```
3. **Push to the branch:**
    ```bash
    git push origin nueva-funcionalidad
    ```
4. **Submit a pull request**, and your changes will be reviewed.
5. If you have any questions, please open an issue.
6. **Thank you for your contribution!**

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
