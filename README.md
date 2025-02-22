# Qwen Chat Application

A sophisticated chat application powered by **Qwen 2.5**, designed for seamless conversations with AI. This project features a sleek, old-money-inspired design, token tracking, and context-aware chat history.

![image](https://github.com/user-attachments/assets/3628e312-9ce1-43b9-b15b-c2d25c176178)


## Features

- **AI-Powered Chat**: Interact with the Qwen 2.5 model for natural language conversations.
- **Context-Aware Chat History**: Maintains conversation context across sessions.
- **Token Tracking**: Displays token usage for each message.
- **Elegant Design**: A luxurious, old-money-inspired UI with dark green and gold accents.
- **User Authentication**: Login and register functionality with session management.
- **Responsive Design**: Works seamlessly on desktop and mobile devices.

---

## Prerequisites

Before running the project, ensure you have the following installed:

- **Python 3.8+**
- **pip** (Python package manager)
- **SQLite** (for the database)
- **Qwen API Key** (from Alibaba Cloud)

---

## Installation

Follow these steps to set up the project locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/qwen-chat-app.git
   cd qwen-chat-app
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   Create a `.env` file in the root directory and add your Qwen API key:
   ```env
   API_KEY=your_qwen_api_key_here
   SECRET_KEY=your_secret_key_here
   ```

5. **Initialize the Database**:
   Run the following command to create the SQLite database:
   ```bash
   python init_db.py
   ```

---

## Running the Application

1. **Start the Flask Server**:
   ```bash
   python app.py
   ```

2. **Access the Application**:
   Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

3. **Login or Register**:
   - Use the login page to access the chat interface.
   - If you don't have an account, register using the registration page.

---

## Project Structure

```
qwen-chat-app/
├── app.py                  # Main Flask application
├── init_db.py              # Database initialization script
├── requirements.txt        # Python dependencies
├── static/
│   └── style.css           # Custom CSS for the application
├── templates/
│   ├── index.html          # Main chat interface
│   ├── login.html          # Login page
│   └── register.html       # Registration page
├── .env                    # Environment variables
└── README.md               # Project documentation
```

---

## Configuration

### Environment Variables
- `API_KEY`: Your Qwen API key from Alibaba Cloud.
- `SECRET_KEY`: A secret key for Flask session management (generate using `secrets.token_hex(16)`).

### Database
The application uses SQLite for storing user data and chat history. The database file (`chatbot.db`) will be created automatically when you run `init_db.py`.

---

## Usage

1. **Start a New Chat**:
   - Click the "New Chat" button in the sidebar to start a fresh conversation.

2. **Send Messages**:
   - Type your message in the input field and press Enter or click "Send".

3. **View Chat History**:
   - Previous chats are displayed in the sidebar. Click on a chat to load its history.

4. **Logout**:
   - Click the "Logout" button in the sidebar to end your session.

---

## Screenshots

### Login Page
![image](https://github.com/user-attachments/assets/8e838b0b-7445-4738-8f2a-b93d92338e3c)


### Chat Interface
![image](https://github.com/user-attachments/assets/c3c7d7e5-a5b9-4161-afdd-f313b863ec8b)


### Registration Page
![image](https://github.com/user-attachments/assets/711380a0-d845-447f-8a39-e832beb42828)


---

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeatureName`).
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **Qwen LLM**: Powered by Alibaba Cloud's Qwen model.
- **Bootstrap 5**: Used for responsive design and UI components.
- **Flask**: Backend framework for handling requests and sessions.

---

## Contact

For questions or feedback, feel free to reach out:

- **Your Name**: [talha@oraxyn.com](mailto:talha@oraxyn.com)
- **GitHub**: [muhammadtalhaishtiaq](https://github.com/muhammadtalhaishtiaq)

---

Enjoy chatting with Qwen! 🚀
