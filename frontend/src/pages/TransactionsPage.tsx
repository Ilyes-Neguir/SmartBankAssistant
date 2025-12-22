import React, { useState, useEffect } from 'react';
import { transactionApi } from '@/services/api';
import { Transaction } from '@/types';
import { ArrowUpRight, ArrowDownLeft, Calendar } from 'lucide-react';
import toast from 'react-hot-toast';

const TransactionsPage: React.FC = () => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTransactions();
  }, []);

  const fetchTransactions = async () => {
    try {
      const data = await transactionApi.getTransactions();
      setTransactions(data);
    } catch (error) {
      toast.error('Failed to load transactions');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Transaction History</h1>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-medium text-gray-900">All Transactions</h2>
        </div>
        <div className="divide-y divide-gray-200">
          {transactions.map((transaction) => (
            <div key={transaction.id} className="px-6 py-4 flex items-center justify-between">
              <div className="flex items-center">
                {transaction.type === 'deposit' ? (
                  <ArrowDownLeft className="h-5 w-5 text-green-500 mr-3" />
                ) : (
                  <ArrowUpRight className="h-5 w-5 text-red-500 mr-3" />
                )}
                <div>
                  <p className="text-sm font-medium text-gray-900">
                    {transaction.description || transaction.type}
                  </p>
                  <div className="flex items-center text-xs text-gray-500">
                    <Calendar className="h-3 w-3 mr-1" />
                    {new Date(transaction.timestamp).toLocaleDateString()}
                  </div>
                </div>
              </div>
              <p className={`text-sm font-medium ${
                transaction.type === 'deposit' ? 'text-green-600' : 'text-red-600'
              }`}>
                {transaction.type === 'deposit' ? '+' : '-'}${transaction.amount.toLocaleString()}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TransactionsPage;
