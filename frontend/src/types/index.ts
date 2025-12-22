// User types
export interface User {
  id: string;
  name: string;
  email: string;
  created_at: string;
}

export interface UserCreate {
  name: string;
  email: string;
  password: string;
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

// Account types
export interface Account {
  id: string;
  user_id: string;
  account_type: string;
  balance: number;
  currency: string;
  account_number: string;
  created_at: string;
}

export interface AccountCreate {
  account_type: string;
  balance: number;
  currency: string;
}

// Transaction types
export interface Transaction {
  id: string;
  account_id: string;
  amount: number;
  type: string;
  description?: string;
  category?: string;
  from_account_id?: string;
  to_account_id?: string;
  timestamp: string;
}

export interface TransactionCreate {
  account_id: string;
  amount: number;
  type: string;
  description?: string;
  category?: string;
  from_account_id?: string;
  to_account_id?: string;
}

// Chat types
export interface ChatMessage {
  id: string;
  user_id: string;
  message: string;
  is_user: boolean;
  bot_response?: string;
  intent_detected?: string;
  timestamp: string;
}

export interface ChatMessageCreate {
  message: string;
}

// API Response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}
