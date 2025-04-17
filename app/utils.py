import numpy as np
import pandas as pd


def calculate_position_size(account_balance, risk_percentage, entry_price, stop_loss):
    """
    Calculate the position size based on risk parameters.
    
    Parameters:
    -----------
    account_balance : float
        Total account balance in USD
    risk_percentage : float
        Risk per trade as a percentage (e.g., 1 for 1%)
    entry_price : float
        Entry price of the trade
    stop_loss : float
        Stop loss price
    
    Returns:
    --------
    dict
        Dictionary containing position size, risk amount, and pips at risk
    """
    # Risk amount in USD
    risk_amount = account_balance * (risk_percentage / 100)
    
    # Calculate pips at risk
    pips_at_risk = abs(entry_price - stop_loss)
    
    # Position size calculation (simplified for forex standard lots)
    # 1 pip = 0.0001 for most pairs, 1 standard lot = 100,000 units
    pip_value = 10  # Assuming $10 per pip for 1 standard lot
    
    # Calculate position size in lots
    position_size = risk_amount / (pips_at_risk * pip_value)
    
    return {
        "position_size": position_size,
        "risk_amount": risk_amount,
        "pips_at_risk": pips_at_risk
    }


def calculate_risk_reward_ratio(entry_price, stop_loss, take_profit=None):
    """
    Calculate the risk-to-reward ratio.
    
    Parameters:
    -----------
    entry_price : float
        Entry price of the trade
    stop_loss : float
        Stop loss price
    take_profit : float, optional
        Take profit price
        
    Returns:
    --------
    float or None
        Risk-to-reward ratio if take_profit is provided, None otherwise
    """
    if take_profit is None:
        return None
    
    risk = abs(entry_price - stop_loss)
    reward = abs(entry_price - take_profit)
    
    if risk == 0:
        return None
    
    return reward / risk


def calculate_expected_value(avg_rr, winrate, risk_per_trade):
    """
    Calculate the expected value per trade.
    
    Parameters:
    -----------
    avg_rr : float
        Average risk-to-reward ratio
    winrate : float
        Win rate as a percentage (e.g., 40 for 40%)
    risk_per_trade : float
        Risk per trade as a percentage of account
        
    Returns:
    --------
    dict
        Dictionary containing expected value and profit projections
    """
    win_prob = winrate / 100
    loss_prob = 1 - win_prob
    
    # Expected value calculation
    ev_per_trade = (win_prob * avg_rr - loss_prob) * risk_per_trade
    
    # Profit projections
    projections = {}
    for n_trades in [10, 50, 100]:
        projections[n_trades] = ev_per_trade * n_trades
    
    return {
        "expected_value_per_trade": ev_per_trade,
        "projections": projections
    }


def calculate_trade_statistics(trades_df):
    """
    Calculate statistics from trade journal.
    
    Parameters:
    -----------
    trades_df : pd.DataFrame
        DataFrame containing trade records
        
    Returns:
    --------
    dict
        Dictionary containing trade statistics
    """
    if trades_df.empty:
        return {
            "winrate": 0,
            "avg_rr": 0,
            "total_pnl": 0,
            "win_count": 0,
            "loss_count": 0
        }
    
    # Convert result column to numeric if it's not
    if trades_df['result'].dtype == 'object':
        trades_df['result'] = pd.to_numeric(trades_df['result'], errors='coerce')
    
    win_count = len(trades_df[trades_df['status'] == 'Win'])
    loss_count = len(trades_df[trades_df['status'] == 'Loss'])
    total_trades = win_count + loss_count
    
    if total_trades == 0:
        winrate = 0
    else:
        winrate = (win_count / total_trades) * 100
    
    # Calculate average R:R 
    avg_rr = trades_df['rr'].mean() if 'rr' in trades_df.columns else 0
    
    # Calculate total P/L
    total_pnl = trades_df['result'].sum()
    
    return {
        "winrate": winrate,
        "avg_rr": avg_rr,
        "total_pnl": total_pnl,
        "win_count": win_count,
        "loss_count": loss_count
    } 