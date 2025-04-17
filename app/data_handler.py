import pandas as pd
import os
import datetime


class TradeJournal:
    """
    A class to handle trade journal operations: saving, loading, and analyzing trades.
    """
    
    def __init__(self, data_path="../data"):
        """
        Initialize the TradeJournal with a data path.
        
        Parameters:
        -----------
        data_path : str
            Path to the directory where trade data will be stored
        """
        self.data_path = data_path
        self.journal_file = os.path.join(data_path, "trade_journal.csv")
        self.trades_df = self._load_trades()
        
        # Create data directory if it doesn't exist
        os.makedirs(data_path, exist_ok=True)
    
    def _load_trades(self):
        """
        Load trades from CSV file or create an empty DataFrame if file doesn't exist.
        
        Returns:
        --------
        pd.DataFrame
            DataFrame containing trade records
        """
        if os.path.exists(self.journal_file):
            return pd.read_csv(self.journal_file)
        else:
            # Define columns for the trade journal
            columns = [
                'date', 'pair', 'entry_price', 'stop_loss', 'take_profit', 
                'position_size', 'result', 'status', 'rr', 'notes'
            ]
            return pd.DataFrame(columns=columns)
    
    def add_trade(self, trade_data):
        """
        Add a new trade to the journal.
        
        Parameters:
        -----------
        trade_data : dict
            Dictionary containing trade information
            
        Returns:
        --------
        bool
            True if trade was added successfully
        """
        # Add current date if not provided
        if 'date' not in trade_data:
            trade_data['date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Add the trade as a new row
        self.trades_df = pd.concat([self.trades_df, pd.DataFrame([trade_data])], 
                                  ignore_index=True)
        
        # Save to file
        return self._save_trades()
    
    def _save_trades(self):
        """
        Save trades to CSV file.
        
        Returns:
        --------
        bool
            True if trades were saved successfully
        """
        try:
            self.trades_df.to_csv(self.journal_file, index=False)
            return True
        except Exception as e:
            print(f"Error saving trades: {e}")
            return False
    
    def get_trades(self):
        """
        Get all trades as a DataFrame.
        
        Returns:
        --------
        pd.DataFrame
            DataFrame containing all trade records
        """
        return self.trades_df
    
    def clear_trades(self):
        """
        Clear all trades from the journal.
        
        Returns:
        --------
        bool
            True if trades were cleared successfully
        """
        self.trades_df = pd.DataFrame(columns=self.trades_df.columns)
        return self._save_trades() 