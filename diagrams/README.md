# UML Diagrams - SmartBank Assistant

This directory contains **4 comprehensive UML diagrams** that cover the entire SmartBank Assistant project.

## The 4 Diagrams

### 1. Complete Class Diagram
**File**: `01-complete-class-diagram.puml`

Shows all classes in the system:
- **Database Models**: User, Account, Transaction, ChatLog
- **Backend API**: FastAPI, Routers (Auth, Account, Transaction, Chat), Services (Gemini, JWT)
- **Frontend Components**: App, AuthProvider, Pages (Login, Dashboard, Accounts, Transactions, Chat), APIService
- **Relationships**: All associations and dependencies

### 2. System Architecture Diagram
**File**: `02-system-architecture-diagram.puml`

Shows the complete system architecture:
- **Client Layer**: User, Web Browser
- **Frontend Layer**: React components, State management, API client, Pages
- **Backend Layer**: FastAPI REST API, Authentication, Business logic, AI Service, Routes
- **Data Layer**: SQLAlchemy ORM, PostgreSQL Database with all tables
- **External Services**: Google Gemini AI API
- **Data Flow**: Complete flow from user to database and AI

### 3. Complete Sequence Diagram
**File**: `03-complete-sequence-diagram.puml`

Shows the complete user journey:
1. User Registration
2. User Login
3. View Accounts
4. Create Transaction
5. AI Chatbot Interaction
6. View Transaction History

Includes all interactions between:
- User
- Frontend (React)
- Backend API (FastAPI)
- Database (PostgreSQL)
- Gemini AI

### 4. Use Case Diagram
**File**: `04-use-case-diagram.puml`

Shows all system use cases organized by feature:
- **Authentication & Authorization**: Register, Login, Logout
- **Account Management**: View accounts, balances, create accounts
- **Transaction Management**: View history, create deposits/withdrawals/transfers
- **AI Chatbot Features**: Send messages, view history, get balance/transaction info
- **Dashboard & Navigation**: All navigation use cases

## How to Render Diagrams

### Option 1: Online (Easiest - Recommended)
1. Go to [PlantUML Online Server](http://www.plantuml.com/plantuml/uml/)
2. Open any `.puml` file from this directory
3. Copy the entire contents
4. Paste into the online editor
5. Click "Submit" to generate the diagram
6. Right-click the image to save as PNG or SVG

### Option 2: VS Code Extension
1. Install "PlantUML" extension in VS Code
2. Open any `.puml` file
3. Press `Alt+D` (or right-click → "Preview Current Diagram")
4. Export as PNG/SVG using the extension

### Option 3: Command Line
1. Download PlantUML from [plantuml.com](https://plantuml.com/starting)
2. Install Java (required)
3. Run: `java -jar plantuml.jar diagrams/*.puml`
4. PNG files will be generated in the same directory

### Option 4: Docker
```bash
docker run -d -p 8080:8080 plantuml/plantuml-server:jetty
# Then access http://localhost:8080
```

## Quick Render Script

**Windows (render-diagrams.bat):**
```batch
@echo off
echo Rendering all PlantUML diagrams...
for %%f in (diagrams\*.puml) do (
    echo Rendering %%f...
    java -jar plantuml.jar "%%f"
)
echo Done! Check diagrams folder for PNG files.
```

**Linux/Mac (render-diagrams.sh):**
```bash
#!/bin/bash
echo "Rendering all PlantUML diagrams..."
for file in diagrams/*.puml; do
    echo "Rendering $file..."
    plantuml "$file"
done
echo "Done! Check diagrams folder for PNG files."
```

## Diagram Coverage

These 4 diagrams comprehensively cover:

✅ **All Classes**: Database models, backend API, frontend components  
✅ **Complete Architecture**: All layers and components  
✅ **Full User Journey**: Registration through AI chat  
✅ **All Use Cases**: Every feature and functionality  

## Integration

- Diagrams are referenced in `UML_DIAGRAMS.md`
- Can be included in presentations
- Can be added to project reports
- Suitable for documentation

## Notes

- All diagrams use PlantUML syntax
- Can be rendered as PNG, SVG, PDF, or EPS
- Diagrams are self-contained and comprehensive
- Each diagram covers a major aspect of the system

---

**Total Diagrams**: 4 comprehensive diagrams  
**Format**: PlantUML (.puml)  
**Coverage**: Complete project
