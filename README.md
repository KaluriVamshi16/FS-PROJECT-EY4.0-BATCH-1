# FS-PROJECT-EY4.0-BATCH-1
FinSight - AI Driven Personal Finance Management System:
FinSight is a modern, AI-powered financial management application designed to help you track expenses, manage budgets, and gain insights into your spending habits through a multilingual chatbot interface.

## 🚀 Overview

FinSight combines traditional expense tracking with the power of LLMs (Groq) to provide a seamless financial management experience. Whether you want to record a transaction in natural language or monitor your budget limits with custom alerts, FinSight has you covered.

## ✨ Features

- **AI Chatbot (Groq)**: Record expenses naturally (e.g., "Spent 500 on dinner") and get financial advice.
- **Support for Multiple Languages**: Interact in English, Telugu, or Hindi.
- **Budget Management**: Set monthly limits per category with dynamic progress bars.
- **Visual Alerts**: Progress bars change color based on usage (Green <40%, Orange 41-74%, Red 75%+).
- **80% Budget Alert System**: Automatic notifications via Django messages when you cross 80% of your budget.
- **Dashboard**: A comprehensive view of your total spending and budget status.
- **Expense Categorization**: Automatic detection of expense categories using NLP logic.
- **Secure Infrastructure**: Environment-based configuration for API keys and secrets.

## 🛠 Tech Stack

- **Backend**: Python 3, Django 4.2
- **Database**: SQLite
- **AI/LLM**: Groq Cloud API (Llama models)
- **Frontend**: Vanilla HTML5, CSS3 (Glassmorphism design), JavaScript
- **Deployment**: Whitenoise (Static files), Waitress/Gunicorn compatibility

## 📋 Prerequisites

- Python 3.8+
- [Groq API Key](https://console.groq.com/keys)

## ⚙️ Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repository-url>
   cd Finsight
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your-django-secret-key
   DEBUG=True
   GROQ_API_KEY=your-groq-api-key
   ```

5. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the server**:
   ```bash
   python manage.py runserver
   ```

## 💡 Usage

1.  **Dashboard**: Monitor your "Total Spending" and "Budget Status" at a glance.
2.  **Add Expense**: Go to the Expenses section or just tell the Chatbot: *"I spent 200 on fuel"*.
3.  **Manage Budgets**: Set your monthly limits for categories like Food, Travel, etc.
4.  **multilingual Support**: Switch between English, Telugu, and Hindi in the chatbot interface.

## 🏗 Architecture

The project is modularized into several Django apps:
- `apps.authentication`: User login and registration.
- `apps.chatbot`: AI processing and message handling.
- `apps.expenses`: Core expense tracking and NLP categorization.
- `apps.budgets`: Budgeting logic and alert management.
- `apps.dashboard`: Centralized user interface.
- `apps.core`: Shared utilities and base templates.

## 🤝 Contributing

1. Fork the Project.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the Branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.


## 📧 Contact

**FinSight Team** - K.Vamshi, K.Kishore Reddy, K.Vaishnavi, B.Padmaja

Project Link: https://github.com/KaluriVamshi16/FS-PROJECT-EY4.0-BATCH-1
