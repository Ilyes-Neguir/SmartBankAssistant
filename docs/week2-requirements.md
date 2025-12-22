# Week 2: AI in Requirements Engineering

## Overview

This document demonstrates how AI was used in Requirements Engineering for the SmartBank Assistant project, including requirements elicitation, classification, prioritization, quality analysis, and user story generation.

## 1. AI for Requirements Elicitation

### 1.1 Initial Requirements Gathering

**AI Tool Used**: ChatGPT  
**Approach**: Conversational requirements elicitation

**Initial Prompt:**
> "I need to build a banking application with AI chatbot. Help me identify all the requirements I should consider."

**AI-Generated Requirements List:**

1. **Functional Requirements:**
   - User authentication and authorization
   - Account management (view, create accounts)
   - Transaction management (view, create transactions)
   - AI chatbot for banking queries
   - Chat history storage
   - Multi-language support

2. **Non-Functional Requirements:**
   - Security (password hashing, JWT tokens)
   - Performance (response time < 500ms)
   - Scalability (support 100+ concurrent users)
   - Usability (responsive design)
   - Maintainability (modular code)

3. **Technical Requirements:**
   - RESTful API design
   - Database design (PostgreSQL)
   - Frontend framework (React)
   - Backend framework (FastAPI)
   - AI integration (Google Gemini)

### 1.2 Domain-Specific Requirements

**AI Prompt:**
> "What are the specific requirements for a banking application chatbot?"

**AI-Generated Banking-Specific Requirements:**

- **Security Requirements:**
  - Secure authentication (JWT)
  - Password encryption (bcrypt)
  - CORS protection
  - Input validation
  - SQL injection prevention

- **Banking Features:**
  - Account balance inquiries
  - Transaction history
  - Money transfers
  - Product information (cards, loans)
  - Interest rates and fees

- **AI Chatbot Requirements:**
  - Natural language understanding
  - Intent recognition
  - Context awareness
  - Multi-language support (English, French)
  - Conversation history

## 2. AI for Requirements Classification

### 2.1 Classification Framework

AI helped classify requirements into categories:

**Classification Prompt:**
> "Classify these requirements into Must-Have, Should-Have, and Nice-to-Have categories using MoSCoW method"

**AI Classification Results:**

#### Must-Have (M):
- User authentication (login, register)
- View account balances
- View transaction history
- AI chatbot basic functionality
- Secure password storage
- JWT authentication

#### Should-Have (S):
- Create new accounts
- Create transactions
- Chat history storage
- Multi-language support
- Account types (checking, savings, credit)

#### Could-Have (C):
- Transaction categorization
- Advanced AI features
- Email notifications
- Mobile app

#### Won't-Have (W):
- Real money transfers
- Credit card processing
- Investment features
- Bill payments

### 2.2 Functional vs Non-Functional Classification

**AI-Assisted Classification:**

**Functional Requirements:**
```python
FR1: User Authentication
  - FR1.1: User registration
  - FR1.2: User login
  - FR1.3: JWT token generation
  - FR1.4: Protected routes

FR2: Account Management
  - FR2.1: View accounts
  - FR2.2: Create account
  - FR2.3: View account details

FR3: Transaction Management
  - FR3.1: View transactions
  - FR3.2: Create transaction
  - FR3.3: Transaction categorization

FR4: AI Chatbot
  - FR4.1: Send message
  - FR4.2: Receive AI response
  - FR4.3: View chat history
  - FR4.4: Intent detection
```

**Non-Functional Requirements:**
```python
NFR1: Performance
  - NFR1.1: API response < 500ms
  - NFR1.2: Chatbot response < 3s

NFR2: Security
  - NFR2.1: Password hashing
  - NFR2.2: JWT expiration
  - NFR2.3: CORS protection

NFR3: Usability
  - NFR3.1: Responsive design
  - NFR3.2: Intuitive UI
  - NFR3.3: Clear error messages
```

## 3. AI for Requirements Prioritization

### 3.1 Priority Scoring

**AI Tool**: ChatGPT  
**Method**: Weighted scoring with AI assistance

**AI Prompt:**
> "Prioritize these requirements using a scoring system considering: business value, technical complexity, user impact, and dependencies"

**AI-Generated Priority Scores:**

| Requirement | Business Value | Complexity | User Impact | Dependencies | Priority Score |
|-------------|---------------|------------|-------------|--------------|----------------|
| User Authentication | 10 | 5 | 10 | 0 | **25** |
| View Accounts | 9 | 3 | 9 | Auth | **21** |
| AI Chatbot | 10 | 7 | 10 | Auth | **27** |
| View Transactions | 8 | 3 | 8 | Auth, Accounts | **19** |
| Create Transactions | 7 | 5 | 7 | Auth, Accounts | **19** |
| Chat History | 6 | 4 | 6 | Auth, Chat | **16** |

**Implementation Order (AI-Suggested):**
1. User Authentication (Foundation)
2. View Accounts (Core feature)
3. AI Chatbot (Differentiator)
4. View Transactions (Core feature)
5. Create Transactions (Enhancement)
6. Chat History (Enhancement)

### 3.2 Dependency Analysis

**AI-Generated Dependency Graph:**

```
User Authentication
    ↓
    ├──→ View Accounts
    ├──→ View Transactions
    ├──→ Create Transactions
    └──→ AI Chatbot
            ↓
            └──→ Chat History
```

## 4. AI for Quality Analysis

### 4.1 Requirements Quality Checklist

**AI-Generated Quality Criteria:**

✅ **Completeness**: All requirements captured?  
✅ **Consistency**: No conflicting requirements?  
✅ **Clarity**: Requirements are unambiguous?  
✅ **Testability**: Requirements can be verified?  
✅ **Traceability**: Requirements linked to features?  
✅ **Feasibility**: Requirements are achievable?

**AI Analysis Results:**

| Criterion | Status | AI Feedback |
|-----------|--------|-------------|
| Completeness | ✅ | "Most requirements captured. Consider adding error handling requirements." |
| Consistency | ✅ | "No conflicts detected. Requirements are consistent." |
| Clarity | ⚠️ | "Some requirements need more detail (e.g., 'AI chatbot' should specify capabilities)" |
| Testability | ✅ | "All requirements have clear acceptance criteria." |
| Traceability | ✅ | "Requirements are well-linked to user stories." |
| Feasibility | ✅ | "All requirements are technically feasible with chosen stack." |

### 4.2 Requirements Refinement

**AI Suggestions for Improvement:**

1. **Clarify AI Chatbot Requirements:**
   - Original: "AI chatbot for banking queries"
   - AI-Suggested: "AI chatbot that understands natural language banking queries, provides account information, transaction history, and product details. Supports English and French. Response time < 3 seconds."

2. **Add Error Handling:**
   - AI-Suggested: "System shall handle API errors gracefully with user-friendly error messages. Network failures shall be retried with exponential backoff."

3. **Specify Security Requirements:**
   - AI-Suggested: "Passwords must be hashed using bcrypt with minimum 10 salt rounds. JWT tokens must expire after 30 minutes of inactivity."

## 5. AI-Assisted User Story Generation

### 5.1 User Story Template

**AI-Generated Template:**
```
As a [user type],
I want to [action],
So that [benefit].

Acceptance Criteria:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
```

### 5.2 Generated User Stories

**AI Prompt:**
> "Generate user stories for a banking application with AI chatbot"

**AI-Generated User Stories:**

#### US1: User Registration
```
As a new user,
I want to register with my email and password,
So that I can access the banking application.

Acceptance Criteria:
- [ ] Registration form validates email format
- [ ] Password meets security requirements (min 8 chars)
- [ ] Duplicate email registration is prevented
- [ ] Password is hashed before storage
- [ ] Success message is displayed after registration
- [ ] User is redirected to login page
```

#### US2: View Account Balances
```
As a logged-in user,
I want to view all my account balances,
So that I know how much money I have in each account.

Acceptance Criteria:
- [ ] All user accounts are displayed
- [ ] Account balances are shown accurately
- [ ] Account types are clearly labeled
- [ ] Currency is displayed
- [ ] Total balance across all accounts is calculated
```

#### US3: AI Chatbot Interaction
```
As a user,
I want to chat with an AI assistant,
So that I can get banking information quickly without navigating menus.

Acceptance Criteria:
- [ ] Chat interface is accessible from main navigation
- [ ] User can type messages in natural language
- [ ] AI understands banking-related queries
- [ ] Responses are relevant and helpful
- [ ] Chat history is preserved
- [ ] Supports both English and French
```

#### US4: Transaction History
```
As a user,
I want to view my transaction history,
So that I can track my spending and income.

Acceptance Criteria:
- [ ] All transactions are displayed in chronological order
- [ ] Transaction details include: amount, type, date, description
- [ ] Transactions can be filtered by type
- [ ] Transactions are paginated (20 per page)
- [ ] Total income and expenses are calculated
```

### 5.3 User Story Refinement

**AI-Assisted Refinement:**

**Original Story:**
> "As a user, I want to use the chatbot."

**AI-Refined Story:**
```
As a banking customer,
I want to interact with an AI-powered chatbot using natural language,
So that I can quickly get answers to my banking questions without waiting for human support.

Acceptance Criteria:
- [ ] Chatbot is accessible from the main dashboard
- [ ] I can type questions in English or French
- [ ] Chatbot understands queries about:
  - Account balances
  - Transaction history
  - Banking products (cards, loans)
  - Interest rates and fees
- [ ] Responses are provided within 3 seconds
- [ ] Chat history is saved and accessible
- [ ] Chatbot provides helpful, accurate information
- [ ] If chatbot cannot answer, it suggests contacting support
```

## 6. Requirements Documentation

### 6.1 AI-Generated Requirements Document Structure

**AI-Suggested Structure:**

1. **Introduction**
   - Project Overview
   - Purpose
   - Scope

2. **Functional Requirements**
   - Authentication
   - Account Management
   - Transaction Management
   - AI Chatbot

3. **Non-Functional Requirements**
   - Performance
   - Security
   - Usability
   - Maintainability

4. **User Stories**
   - Epic 1: Authentication
   - Epic 2: Account Management
   - Epic 3: Transactions
   - Epic 4: AI Chatbot

5. **Acceptance Criteria**
   - Per user story

6. **Technical Requirements**
   - Technology Stack
   - Architecture
   - Integration Requirements

### 6.2 Requirements Traceability Matrix

**AI-Generated Matrix:**

| Requirement ID | User Story | Feature | Status |
|----------------|------------|---------|--------|
| FR1.1 | US1 | User Registration | ✅ Implemented |
| FR1.2 | US1 | User Login | ✅ Implemented |
| FR2.1 | US2 | View Accounts | ✅ Implemented |
| FR2.2 | US2 | Create Account | ✅ Implemented |
| FR3.1 | US4 | View Transactions | ✅ Implemented |
| FR4.1 | US3 | AI Chatbot | ✅ Implemented |
| FR4.2 | US3 | Chat History | ✅ Implemented |

## 7. Impact on Project

### 7.1 Benefits

✅ **Comprehensive Requirements**: AI helped identify requirements we might have missed  
✅ **Better Organization**: AI-assisted classification and prioritization  
✅ **Quality Assurance**: AI quality analysis improved requirements  
✅ **User Stories**: AI-generated well-structured user stories  
✅ **Time Savings**: ~40% faster requirements gathering

### 7.2 Challenges

⚠️ **Over-specification**: AI sometimes suggested overly detailed requirements  
⚠️ **Context Understanding**: AI needed multiple iterations to understand domain  
⚠️ **Validation**: Human review still necessary for accuracy

## 8. Conclusion

AI significantly enhanced the Requirements Engineering phase by:

1. **Elicitation**: Identifying comprehensive requirements
2. **Classification**: Organizing requirements systematically
3. **Prioritization**: Determining implementation order
4. **Quality Analysis**: Ensuring requirements quality
5. **User Story Generation**: Creating well-structured stories

The AI-assisted approach resulted in more complete, organized, and high-quality requirements documentation.

---

**Next**: [Week 3: AI in Software Design](week3-design.md)

