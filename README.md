# SmartBank Assistant - Complete Web Application

A comprehensive banking assistant web application with AI chatbot integration, built with FastAPI backend and React frontend.

## 🏗️ Project Architecture

Based on the project requirements from rapport.txt:

| Component          | Technology Used               |
| ------------------ | ----------------------------- |
| Frontend           | React (Web App)               |
| Backend            | FastAPI (Python)              |
| AI (Chatbot / LLM) | Gemini (Google Generative AI) |
| Database           | PostgreSQL                    |
| Authentication     | JWT + Bcrypt                  |
| IDE                | Visual Studio Code            |

## 🚀 Features

### Core Banking Features
- **Account Management** - View balances, account types
- **Transaction History** - Complete transaction tracking
- **Money Transfers** - Internal and external transfers
- **Product Information** - Cards, loans, rates, fees

### AI Chatbot Features
- **Natural Language Processing** - Understands user queries in French/English
- **Intent Recognition** - Extracts user intent (balance check, transfers, etc.)
- **Contextual Responses** - Provides relevant banking information
- **Chat History** - Stores conversation history

### Security Features
- **JWT Authentication** - Secure token-based auth
- **Password Hashing** - Bcrypt encryption
- **User Authorization** - Protected routes and data access
- **Input Validation** - Comprehensive data validation

## 📁 Project Structure

```
smartbanking-app/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── auth/           # Authentication modules
│   │   ├── crud/           # Database operations
│   │   ├── routes/         # API endpoints
│   │   ├── schemas/        # Pydantic models
│   │   ├── services/       # Business logic (Gemini AI)
│   │   ├── db.py           # Database config
│   │   └── main.py         # FastAPI app
│   ├── models/             # SQLAlchemy models
│   ├── requirements.txt    # Dependencies
│   └── run.py              # Server startup
├── frontend/               # React Frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   ├── hooks/          # Custom hooks
│   │   ├── types/          # TypeScript types
│   │   └── styles/         # CSS styles
│   ├── package.json        # Dependencies
│   └── vite.config.ts      # Vite config
├── docs/                   # 13 Weeks Documentation
│   ├── week1-introduction.md
│   ├── week2-requirements.md
│   ├── week3-design.md
│   ├── week4-coding1.md
│   ├── week5-coding2.md
│   ├── week6-testing1.md
│   ├── week7-testing2.md
│   ├── week9-devops.md
│   ├── week10-maintenance.md
│   ├── week11-project-management.md
│   ├── week12-ai-products.md
│   └── week13-ethics.md
├── diagrams/               # UML Diagrams (PlantUML)
│   ├── 01-complete-class-diagram.puml
│   ├── 02-system-architecture-diagram.puml
│   ├── 03-complete-sequence-diagram.puml
│   └── 04-use-case-diagram.puml
├── PROJECT_REPORT.md       # Complete project report
├── PRESENTATION_SUMMARY.md # Presentation summary
├── presentation.html       # Interactive HTML presentation
├── UML_DIAGRAMS.md         # UML diagrams documentation
├── REQUIREMENTS_COVERAGE_CHECKLIST.md
├── docker-compose.yml      # Docker setup
└── README.md               # This file
```

## 🚀 Quick Start

### One-Click Run (Recommended)

**Windows:**
```bash
run.bat
```

**PowerShell:**
```powershell
.\run.ps1
```

The run script automatically:
- ✅ Checks Docker installation
- ✅ Starts PostgreSQL database
- ✅ Sets up Python backend environment
- ✅ Installs Node.js frontend dependencies
- ✅ Creates configuration files
- ✅ Starts both servers
- ✅ Opens browser to http://localhost:3000

### Prerequisites
- **Docker Desktop** - [Download here](https://www.docker.com/products/docker-desktop/)
- **Python 3.8+** - For backend
- **Node.js 18+** - For frontend
- **Google AI API key** - [Get from here](https://makersuite.google.com/app/apikey)

### Manual Setup (Alternative)

1. **Start Database:**
```bash
docker-compose up -d postgres
```

2. **Backend Setup:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python run.py
```

3. **Frontend Setup:**
```bash
cd frontend
npm install
npm run dev
```

### Access Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database**: PostgreSQL on localhost:5432

## 🔧 Configuration

### Environment Variables
Create `.env` files:

**Backend (.env):**
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/smartbank
SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=your-gemini-api-key
```

**Frontend (.env):**
```env
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=SmartBank Assistant
```

## 🧪 Testing

```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

## 📚 API Documentation

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Banking
- `GET /api/accounts` - Get user accounts
- `POST /api/accounts` - Create account
- `GET /api/transactions` - Get transactions
- `POST /api/transactions` - Create transaction

### Chatbot
- `POST /api/chat/message` - Send message to chatbot
- `GET /api/chat/history` - Get chat history

## 🤖 Chatbot Integration

The chatbot uses Google's Gemini AI to:
- Understand natural language queries
- Provide banking information
- Process transaction requests
- Answer product questions
- Maintain conversation context

## 🔒 Security

- JWT token authentication
- Password hashing with bcrypt
- Input validation and sanitization
- CORS protection
- SQL injection prevention

## 🚀 Deployment

### Docker
```bash
docker-compose up -d
```

### Manual Deployment
1. Set up PostgreSQL database
2. Configure environment variables
3. Deploy backend to your server
4. Build and deploy frontend
5. Set up reverse proxy (nginx)

## 📖 Documentation

### Project Documentation
- **[PROJECT_REPORT.md](PROJECT_REPORT.md)** - Complete project report with all details
- **[PRESENTATION_SUMMARY.md](PRESENTATION_SUMMARY.md)** - Summary for presentations
- **[presentation.html](presentation.html)** - Interactive HTML presentation (15-20 slides)
- **[UML_DIAGRAMS.md](UML_DIAGRAMS.md)** - UML diagrams documentation
- **[REQUIREMENTS_COVERAGE_CHECKLIST.md](REQUIREMENTS_COVERAGE_CHECKLIST.md)** - Requirements coverage

### 13 Weeks Documentation (AI-First Software Engineering)
Complete documentation for each week/topic:
- [Week 1: Introduction to AI-First Software Engineering](docs/week1-introduction.md)
- [Week 2: AI in Requirements Engineering](docs/week2-requirements.md)
- [Week 3: AI in Software Design](docs/week3-design.md)
- [Week 4-5: AI in Coding & Development](docs/week4-coding1.md) | [Week 5](docs/week5-coding2.md)
- [Week 6-7: AI in Testing & QA](docs/week6-testing1.md) | [Week 7](docs/week7-testing2.md)
- [Week 9: AI in DevOps & AIOps](docs/week9-devops.md)
- [Week 10: AI in Software Maintenance](docs/week10-maintenance.md)
- [Week 11: AI in Project Management](docs/week11-project-management.md)
- [Week 12: AI-Enabled Software Products](docs/week12-ai-products.md)
- [Week 13: Ethics & Responsible AI](docs/week13-ethics.md)

### UML Diagrams
All diagrams are available in PlantUML format in the `diagrams/` folder:
- Complete Class Diagram
- System Architecture Diagram
- Sequence Diagram
- Use Case Diagram

To render diagrams, use [PlantUML Online](http://www.plantuml.com/plantuml/uml/) or VS Code PlantUML extension.

## 📞 Support

For issues and questions:
- Check the API documentation at `/docs`
- Review the test files for usage examples
- Read the complete project report in `PROJECT_REPORT.md`
- Open an issue on GitHub

---

**SmartBank Assistant** - Intelligent Banking Made Simple

**Project Type:** Full-Stack Web Application  
**Development Approach:** AI-First Software Engineering  
**Repository:** https://github.com/Ilyes-Neguir/SmartBankAssistant
