import google.generativeai as genai
from config import settings
from typing import Dict, Any
import json

class GeminiService:
    """Service for interacting with Google's Gemini AI"""
    
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def process_banking_query(self, user_message: str, user_context: Dict[str, Any] = None) -> Dict[str, str]:
        """
        Process a banking query using Gemini AI
        
        Args:
            user_message: The user's message
            user_context: Context about the user (accounts, transactions, etc.)
        
        Returns:
            Dict containing bot response and detected intent
        """
        try:
            # Create context-aware prompt
            prompt = self._create_banking_prompt(user_message, user_context)
            
            # Generate response using Gemini
            response = self.model.generate_content(prompt)
            
            # Parse the response
            bot_response = response.text.strip()
            intent = self._detect_intent(user_message)
            
            return {
                "response": bot_response,
                "intent": intent
            }
            
        except Exception as e:
            return {
                "response": "I apologize, but I'm having trouble processing your request right now. Please try again later.",
                "intent": "error"
            }
    
    def _create_banking_prompt(self, user_message: str, user_context: Dict[str, Any] = None) -> str:
        """Create a context-aware prompt for the banking assistant"""
        
        base_prompt = """
        You are a helpful banking assistant. You can help customers with:
        - Checking account balances
        - Viewing transaction history
        - Transferring money between accounts
        - Providing information about banking products
        - Answering questions about fees and rates
        
        Respond in a friendly, professional manner. If you need specific account information that isn't provided, ask the user to provide it.
        """
        
        if user_context:
            context_info = f"""
            User Context:
            - Accounts: {user_context.get('accounts', 'Not available')}
            - Recent Transactions: {user_context.get('transactions', 'Not available')}
            - Total Balance: {user_context.get('total_balance', 'Not available')}
            """
            base_prompt += context_info
        
        prompt = f"{base_prompt}\n\nUser Message: {user_message}\n\nResponse:"
        return prompt
    
    def _detect_intent(self, user_message: str) -> str:
        """Detect the user's intent from their message"""
        message_lower = user_message.lower()
        
        if any(word in message_lower for word in ['balance', 'solde', 'argent']):
            return 'check_balance'
        elif any(word in message_lower for word in ['transaction', 'historique', 'historique']):
            return 'transaction_history'
        elif any(word in message_lower for word in ['transfer', 'virement', 'envoyer']):
            return 'transfer_money'
        elif any(word in message_lower for word in ['card', 'carte', 'credit']):
            return 'product_info'
        elif any(word in message_lower for word in ['loan', 'prêt', 'emprunt']):
            return 'product_info'
        elif any(word in message_lower for word in ['fee', 'frais', 'taux']):
            return 'rates_fees'
        elif any(word in message_lower for word in ['help', 'aide', 'assistance']):
            return 'help'
        else:
            return 'general_inquiry'
