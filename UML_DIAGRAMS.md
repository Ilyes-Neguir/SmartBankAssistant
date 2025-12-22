# UML Diagrams - SmartBank Assistant

This document contains **4 comprehensive UML diagrams** that cover the entire SmartBank Assistant project.

## Table of Contents

1. [Complete Class Diagram](#1-complete-class-diagram)
2. [System Architecture Diagram](#2-system-architecture-diagram)
3. [Complete Sequence Diagram](#3-complete-sequence-diagram)
4. [Use Case Diagram](#4-use-case-diagram)

## Overview

These 4 diagrams provide complete coverage of the SmartBank Assistant system:
- **Class Diagram**: All classes, models, and components (Database, Backend, Frontend)
- **Architecture Diagram**: Complete system structure and data flow (all layers)
- **Sequence Diagram**: Full user journey from registration to AI chat (all workflows)
- **Use Case Diagram**: All system features and functionalities (all requirements)

All diagrams are available as PlantUML files in the `diagrams/` directory and can be rendered as images.

---

## 1. Complete Class Diagram

**File**: `diagrams/01-complete-class-diagram.puml`

This comprehensive class diagram shows all classes in the SmartBank Assistant system:

### Database Models
- **User**: User authentication and profile data
- **Account**: Banking accounts (checking, savings, credit)
- **Transaction**: Financial transactions with categorization
- **ChatLog**: AI conversation history

### Backend API Classes
- **FastAPI**: Main application with routers and middleware
- **AuthRouter**: Authentication endpoints (register, login, logout)
- **AccountRouter**: Account management endpoints
- **TransactionRouter**: Transaction management endpoints
- **ChatRouter**: AI chatbot endpoints
- **GeminiService**: AI service integration with Google Gemini
- **JWTHandler**: JWT token management

### Frontend Components
- **App**: Main React application with routing
- **AuthProvider**: Authentication state management
- **LoginPage**: User login interface
- **DashboardPage**: Main dashboard with overview
- **AccountsPage**: Account management interface
- **TransactionsPage**: Transaction history interface
- **ChatPage**: AI chatbot interface
- **APIService**: API client for backend communication

### Relationships
- User owns multiple Accounts and ChatLogs
- Account contains multiple Transactions
- Frontend components communicate with Backend via APIService
- Backend routers use services and models
- AI Service integrates with external Gemini API

**To render**: Open `diagrams/01-complete-class-diagram.puml` in PlantUML

---

## 2. System Architecture Diagram

**File**: `diagrams/02-system-architecture-diagram.puml`

This diagram shows the complete system architecture with all layers and data flow:

### Layers

1. **Client Layer**
   - User
   - Web Browser

2. **Frontend Layer (React + TypeScript)**
   - React UI Components
   - State Management (useAuth Hook)
   - API Client (Axios)
   - Pages (Login, Dashboard, Accounts, Transactions, Chat)

3. **Backend Layer (FastAPI + Python)**
   - FastAPI REST API
   - Authentication Module (JWT + Bcrypt)
   - Business Logic (CRUD Operations)
   - AI Service (Gemini Integration)
   - Routes (/auth, /accounts, /transactions, /chat)

4. **Data Layer**
   - SQLAlchemy ORM
   - PostgreSQL Database
     - Users Table
     - Accounts Table
     - Transactions Table
     - ChatLogs Table

5. **External Services**
   - Google Gemini AI API

### Data Flow
- User interactions flow from Browser → Frontend → Backend → Database
- AI queries flow from Backend → Gemini API
- Authentication tokens flow through all protected routes
- Database operations use ORM for abstraction

**To render**: Open `diagrams/02-system-architecture-diagram.puml` in PlantUML

---

## 3. Complete Sequence Diagram

**File**: `diagrams/03-complete-sequence-diagram.puml`

This comprehensive sequence diagram shows the complete user journey through all major workflows:

### Workflows Covered

1. **User Registration**
   - Form validation
   - Password hashing
   - Database insertion
   - Success response

2. **User Login**
   - Credential verification
   - JWT token generation
   - Token storage
   - Dashboard redirect

3. **Account Management**
   - JWT verification
   - Database query
   - Account list display

4. **Transaction Management**
   - Form validation
   - Balance checking
   - Transaction creation
   - Balance update

5. **AI Chatbot Interaction**
   - Message storage
   - Context retrieval (accounts, transactions)
   - AI API call with context
   - Response storage and display

6. **Transaction History**
   - JWT verification
   - Database query
   - History display

### Participants
- User
- Frontend (React)
- Backend API (FastAPI)
- Database (PostgreSQL)
- Gemini AI (Google)

**To render**: Open `diagrams/03-complete-sequence-diagram.puml` in PlantUML

---

## 4. Use Case Diagram

**File**: `diagrams/04-use-case-diagram.puml`

This diagram shows all system use cases organized by feature area:

### Use Case Groups

1. **Authentication & Authorization**
   - Register Account
   - Login to System
   - Logout

2. **Account Management**
   - View All Accounts
   - View Account Balance
   - Create New Account
   - View Account Details

3. **Transaction Management**
   - View Transaction History
   - Create Deposit
   - Create Withdrawal
   - Create Transfer
   - View Transaction Details

4. **AI Chatbot Features**
   - Send Chat Message
   - View Chat History
   - Get Account Balance via Chat
   - Get Transaction Info via Chat
   - Get Banking Product Info

5. **Dashboard & Navigation**
   - View Dashboard
   - Navigate to Accounts
   - Navigate to Transactions
   - Navigate to Chat

### Dependencies
- All protected features require authentication (Login)
- AI Chatbot extends basic chat with specialized queries
- Account viewing includes balance display
- Transaction history includes transaction details

**To render**: Open `diagrams/04-use-case-diagram.puml` in PlantUML

---

## How to Render Diagrams

### Option 1: Online (Easiest - Recommended)
1. Go to [PlantUML Online Server](http://www.plantuml.com/plantuml/uml/)
2. Open any `.puml` file from the `diagrams/` directory
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

## Diagram Coverage Summary

These 4 comprehensive diagrams cover:

✅ **All Classes**: Database models, backend API classes, frontend components  
✅ **Complete Architecture**: All layers (Client, Frontend, Backend, Data, External)  
✅ **Full User Journey**: Registration → Login → Accounts → Transactions → AI Chat  
✅ **All Use Cases**: Every feature and functionality in the system  

## Integration with Project

- Diagrams are based on actual project implementation
- All classes, components, and flows are from the real codebase
- Use cases match all functional requirements
- Architecture reflects the deployed system structure

---

**Total Diagrams**: 4 comprehensive diagrams  
**Format**: PlantUML (.puml)  
**Coverage**: Complete project  
**Location**: `diagrams/` directory
