import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User, UserCreate, UserLogin } from '@/types';
import { authApi } from '@/services/api';
import toast from 'react-hot-toast';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (credentials: UserLogin) => Promise<void>;
  register: (userData: UserCreate) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  // DEMO MODE: Always logged in as demo user for presentation
  const demoUser: User = {
    id: 'demo-user-123',
    name: 'Admin User',
    email: 'admin@smartbank.com',
    created_at: new Date().toISOString(),
  };

  const [user, setUser] = useState<User | null>(demoUser);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Skip auth check for demo mode
    // checkAuth();
  }, []);

  const checkAuth = async () => {
    const token = localStorage.getItem('access_token');
    if (token) {
      try {
        const userData = await authApi.getMe();
        setUser(userData);
      } catch (error) {
        localStorage.removeItem('access_token');
      }
    }
    setLoading(false);
  };

  const login = async (credentials: UserLogin) => {
    try {
      const tokenData = await authApi.login(credentials);
      localStorage.setItem('access_token', tokenData.access_token);
      
      const userData = await authApi.getMe();
      setUser(userData);
      
      toast.success('Login successful!');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Login failed');
      throw error;
    }
  };

  const register = async (userData: UserCreate) => {
    try {
      await authApi.register(userData);
      toast.success('Registration successful! Please login.');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Registration failed');
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
    toast.success('Logged out successfully');
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
