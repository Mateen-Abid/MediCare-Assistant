# 🏥 MediCare Assistant

A comprehensive healthcare chatbot application built with Django and Google's Gemini AI. MediCare Assistant provides evidence-based health information, wellness guidance, and support while emphasizing the importance of professional medical consultation.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Key Features](#key-features)
- [Security & Privacy](#security--privacy)
- [Contributing](#contributing)
- [License](#license)
- [Medical Disclaimer](#medical-disclaimer)

## ✨ Features

- **AI-Powered Healthcare Assistance**: Leverages Google's Gemini AI for intelligent, context-aware responses
- **User Authentication**: Secure signup and login system with email-based authentication
- **Conversation Management**: Create, view, and manage multiple conversation threads
- **Structured Responses**: Well-formatted, easy-to-read health information with proper markdown formatting
- **Evidence-Based Information**: Responses grounded in reputable sources (CDC, WHO, peer-reviewed guidance)
- **Professional Guidance**: Encourages consultation with licensed healthcare professionals
- **Responsive UI**: Modern, user-friendly chat interface
- **Session Management**: Persistent conversation history per user

## 🛠 Tech Stack

### Backend
- **Django 5.2.7** - Web framework
- **Django REST Framework 3.16.1** - API development
- **LangChain 1.0.3** - AI orchestration framework
- **LangChain Google GenAI 3.0.1** - Google Gemini integration
- **PostgreSQL** (optional) / **SQLite** (default) - Database
- **python-dotenv 1.2.1** - Environment variable management

### Frontend
- HTML5, CSS3, JavaScript
- Django Templates
  <img width="1918" height="1036" alt="login" src="https://github.com/user-attachments/assets/a4c14378-2ea7-4fd2-9c30-7d35dfae35b3" />
<img width="1918" height="1077" alt="dashboard" src="https://github.com/user-attachments/assets/5667cb2a-dd4e-4f71-83b5-522b0ea25a1c" />


### AI/ML
- **Google Gemini 2.5 Flash Lite** - Language model
- **LangChain Core** - Message handling and conversation management

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10+** (Python 3.12 recommended)
- **pip** (Python package manager)
- **PostgreSQL** (optional, for production) or SQLite (default, for development)
- **Google Gemini API Key** ([Get one here](https://makersuite.google.com/app/apikey))

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/MediCare-Assistant.git
cd MediCare-Assistant
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root directory:

```env
# Google Gemini API Key (Required)
API_KEY=your_gemini_api_key_here

# Database Configuration (Optional - defaults to SQLite)
# For PostgreSQL (Production)
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=5432

# For Supabase (if using)
# DB_NAME=postgres
# DB_USER=postgres.xxxxx
# DB_PASSWORD=your_password
# DB_HOST=db.xxxxx.supabase.co
# DB_PORT=5432
```

### Settings

The application automatically uses SQLite for development. To use PostgreSQL or Supabase, set the database environment variables in your `.env` file.

## 🎯 Usage

### Start the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

### Access the Application

1. **Sign Up**: Navigate to `/signup/` to create a new account
2. **Login**: Use `/login/` to access your account
3. **Chat**: Start conversations at `/chat/`

### Using the Chat Interface

1. Create a new conversation or select an existing one
2. Type your health-related questions
3. Receive structured, evidence-based responses
4. View conversation history
5. Delete conversations as needed

## 🔌 API Endpoints

### Authentication

- `POST /api/signup/` - Create a new user account
- `POST /api/login/` - Authenticate user
- `POST /api/logout/` - Log out current user
- `GET /api/user/` - Get current user information

### Conversations

- `GET /api/conversations/` - List all user conversations
- `POST /api/conversations/` - Create a new conversation
- `GET /api/conversations/<id>/` - Get conversation details
- `DELETE /api/conversations/<id>/` - Delete a conversation

### Messages

- `POST /api/conversations/<id>/messages/` - Send a message in a conversation

### Example API Request

```bash
# Send a message
curl -X POST http://127.0.0.1:8000/api/conversations/1/messages/ \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=your_session_id" \
  -d '{"content": "What are the symptoms of a common cold?"}'
```

## 📁 Project Structure

```
MediCare-Assistant/
│
├── app/                      # Main application
│   ├── models.py            # Database models (Conversation, Message)
│   ├── views.py             # API and page views
│   ├── serializers.py       # DRF serializers
│   ├── urls.py              # App URL routing
│   ├── constants.py         # System prompts and constants
│   ├── admin.py             # Django admin configuration
│   └── migrations/          # Database migrations
│
├── myproject/               # Django project settings
│   ├── settings.py          # Project configuration
│   ├── urls.py              # Root URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
│
├── templates/               # HTML templates
│   └── app/
│       ├── base.html        # Base template
│       ├── login.html       # Login page
│       ├── signup.html      # Signup page
│       └── chat.html        # Chat interface
│
├── static/                  # Static files (CSS, JS, images)
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (create this)
└── README.md                # This file
```

## 🔑 Key Features

### Healthcare-Focused AI

The chatbot is specifically trained to:
- Provide evidence-based health information
- Use supportive, plain-language explanations
- Encourage professional medical consultation
- Escalate urgent symptoms appropriately
- Respect privacy and confidentiality

### Structured Responses

All responses are automatically formatted with:
- Clear section headings
- Proper line breaks and spacing
- Bulleted and numbered lists
- Professional disclaimers

### Conversation Management

- Multiple conversation threads per user
- Automatic conversation titling
- Full conversation history
- Easy conversation deletion

## 🔒 Security & Privacy

- **Session-based Authentication**: Secure user sessions
- **CSRF Protection**: Built-in Django CSRF protection
- **Environment Variables**: Sensitive data stored in `.env` file
- **Privacy-First**: No unnecessary data storage
- **Professional Boundaries**: Clear disclaimers about medical advice

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 Python style guide
- Write clear, descriptive commit messages
- Add comments for complex logic
- Test your changes before submitting

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Medical Disclaimer

**IMPORTANT**: This chatbot is designed to provide general health information and wellness guidance. It is NOT a substitute for professional medical advice, diagnosis, or treatment.

- Always seek the advice of qualified health providers with any questions you may have regarding a medical condition
- Never disregard professional medical advice or delay seeking it because of information from this chatbot
- In case of a medical emergency, call your local emergency services immediately
- The information provided is for educational purposes only and should not be used for diagnosing or treating a health problem or disease

## 🚀 Deployment

### Deploy to Vercel

This project is configured for easy deployment on Vercel. See [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md) for detailed instructions.

**Quick Steps:**
1. Push your code to GitHub
2. Import project in [Vercel Dashboard](https://vercel.com/dashboard)
3. Add environment variables (API_KEY, SECRET_KEY, etc.)
4. Deploy!

**Important for Production:**
- Use PostgreSQL/Supabase (not SQLite)
- Set `DEBUG=False`
- Generate a secure `SECRET_KEY`
- Configure `ALLOWED_HOSTS`
- Set up proper database migrations

### Other Deployment Options

- **Railway**: Great for Django apps with PostgreSQL
- **Render**: Simple deployment with free tier
- **Heroku**: Traditional PaaS option
- **DigitalOcean App Platform**: Full control with scaling

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Contact the maintainers

## 🙏 Acknowledgments

- Google Gemini AI for powerful language model capabilities
- Django and Django REST Framework communities
- LangChain for AI orchestration tools
- All contributors and users of this project

---

**Made with ❤️ for better healthcare accessibility**

