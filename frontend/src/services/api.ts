import axios from 'axios';
import { User, UserCreate, UserLogin, Token, Account, AccountCreate, Transaction, TransactionCreate, ChatMessage, ChatMessageCreate } from '@/types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authApi = {
  register: async (userData: UserCreate): Promise<User> => {
    const response = await api.post('/api/auth/register', userData);
    return response.data;
  },

  login: async (credentials: UserLogin): Promise<Token> => {
    const response = await api.post('/api/auth/login', credentials);
    return response.data;
  },

  getMe: async (): Promise<User> => {
    const response = await api.get('/api/auth/me');
    return response.data;
  },
};

// Demo data for presentation mode
const demoAccounts: Account[] = [
  {
    id: 'acc-1',
    user_id: 'demo-user-123',
    account_type: 'checking',
    balance: 15420.50,
    currency: 'USD',
    account_number: '1234567890',
    created_at: new Date().toISOString(),
  },
  {
    id: 'acc-2',
    user_id: 'demo-user-123',
    account_type: 'savings',
    balance: 8500.00,
    currency: 'USD',
    account_number: '0987654321',
    created_at: new Date().toISOString(),
  },
  {
    id: 'acc-3',
    user_id: 'demo-user-123',
    account_type: 'credit',
    balance: 2500.00,
    currency: 'USD',
    account_number: '5555666677',
    created_at: new Date().toISOString(),
  },
];

const demoTransactions: Transaction[] = [
  {
    id: 'txn-1',
    account_id: 'acc-1',
    amount: 500.00,
    type: 'deposit',
    description: 'Salary Deposit',
    category: 'income',
    timestamp: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 'txn-2',
    account_id: 'acc-1',
    amount: 125.50,
    type: 'withdrawal',
    description: 'Grocery Store Purchase',
    category: 'food',
    timestamp: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 'txn-3',
    account_id: 'acc-2',
    amount: 1000.00,
    type: 'deposit',
    description: 'Monthly Savings',
    category: 'savings',
    timestamp: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 'txn-4',
    account_id: 'acc-1',
    amount: 85.00,
    type: 'withdrawal',
    description: 'Restaurant Dinner',
    category: 'food',
    timestamp: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 'txn-5',
    account_id: 'acc-3',
    amount: 150.00,
    type: 'withdrawal',
    description: 'Online Shopping',
    category: 'shopping',
    timestamp: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000).toISOString(),
  },
];

// Account API
export const accountApi = {
  getAccounts: async (): Promise<Account[]> => {
    try {
      const response = await api.get('/api/accounts');
      return response.data;
    } catch (error) {
      // Return demo data if API fails (for presentation)
      console.log('Using demo accounts data');
      return demoAccounts;
    }
  },

  createAccount: async (accountData: AccountCreate): Promise<Account> => {
    const response = await api.post('/api/accounts', accountData);
    return response.data;
  },

  getAccount: async (accountId: string): Promise<Account> => {
    const response = await api.get(`/api/accounts/${accountId}`);
    return response.data;
  },

  updateAccount: async (accountId: string, accountData: Partial<AccountCreate>): Promise<Account> => {
    const response = await api.put(`/api/accounts/${accountId}`, accountData);
    return response.data;
  },

  deleteAccount: async (accountId: string): Promise<void> => {
    await api.delete(`/api/accounts/${accountId}`);
  },
};

// Transaction API
export const transactionApi = {
  getTransactions: async (): Promise<Transaction[]> => {
    try {
      const response = await api.get('/api/transactions');
      return response.data;
    } catch (error) {
      // Return demo data if API fails (for presentation)
      console.log('Using demo transactions data');
      return demoTransactions;
    }
  },

  createTransaction: async (transactionData: TransactionCreate): Promise<Transaction> => {
    const response = await api.post('/api/transactions', transactionData);
    return response.data;
  },

  getTransaction: async (transactionId: string): Promise<Transaction> => {
    const response = await api.get(`/api/transactions/${transactionId}`);
    return response.data;
  },

  updateTransaction: async (transactionId: string, transactionData: Partial<TransactionCreate>): Promise<Transaction> => {
    const response = await api.put(`/api/transactions/${transactionId}`, transactionData);
    return response.data;
  },

  deleteTransaction: async (transactionId: string): Promise<void> => {
    await api.delete(`/api/transactions/${transactionId}`);
  },
};

// Chat API
export const chatApi = {
  sendMessage: async (messageData: ChatMessageCreate): Promise<ChatMessage> => {
    try {
      const response = await api.post('/api/chat/message', messageData);
      return response.data;
    } catch (error) {
      // Return demo response if API fails (for presentation)
      console.log('Using demo chat response');
      return {
        id: `chat-${Date.now()}`,
        user_id: 'demo-user-123',
        message: messageData.message,
        is_user: true,
        bot_response: "I'm a demo AI assistant. In the full version, I can help you with your banking questions, account balances, transactions, and more!",
        intent_detected: 'general_query',
        timestamp: new Date().toISOString(),
      };
    }
  },

  getChatHistory: async (): Promise<ChatMessage[]> => {
    try {
      const response = await api.get('/api/chat/history');
      return response.data;
    } catch (error) {
      // Return empty history if API fails (for presentation)
      console.log('Using demo chat history (empty)');
      return [];
    }
  },
};

export default api;
