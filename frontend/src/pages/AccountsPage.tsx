import React, { useState, useEffect } from 'react';
import { accountApi } from '@/services/api';
import { Account } from '@/types';
import { CreditCard, Plus, DollarSign } from 'lucide-react';
import toast from 'react-hot-toast';

const AccountsPage: React.FC = () => {
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAccounts();
  }, []);

  const fetchAccounts = async () => {
    try {
      const data = await accountApi.getAccounts();
      setAccounts(data);
    } catch (error) {
      toast.error('Failed to load accounts');
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
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Your Accounts</h1>
        <button className="flex items-center px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90">
          <Plus className="h-4 w-4 mr-2" />
          Add Account
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {accounts.map((account) => (
          <div key={account.id} className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <CreditCard className="h-8 w-8 text-primary" />
              <span className="text-sm text-gray-500">****{account.account_number.slice(-4)}</span>
            </div>
            <h3 className="text-lg font-medium text-gray-900 capitalize">
              {account.account_type} Account
            </h3>
            <p className="text-3xl font-bold text-gray-900 mt-2">
              ${account.balance.toLocaleString()}
            </p>
            <p className="text-sm text-gray-500 mt-1">{account.currency}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AccountsPage;
