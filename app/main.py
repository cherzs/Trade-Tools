import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

# Add app directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import custom modules
from utils import (calculate_position_size, calculate_risk_reward_ratio, 
                  calculate_expected_value, calculate_trade_statistics)
from data_handler import TradeJournal

# Set page config
st.set_page_config(
    page_title="Trade Tools",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize trade journal
trade_journal = TradeJournal()

# Add CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.8rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #e0e0e0;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 0.5rem;
        padding: 1rem;
        box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
        text-align: center;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
    }
    .win {
        color: #28a745;
    }
    .loss {
        color: #dc3545;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.markdown("# Trade Tools 📈")
app_mode = st.sidebar.radio(
    "Pilih Fitur",
    ["Risk & Position Size Calculator", "Manual Trade Journal", "Expected Profit Projection"]
)

# Main app header
st.markdown("<h1 class='main-header'>Trade Tools</h1>", unsafe_allow_html=True)

# Function to display Risk Calculator
def show_risk_calculator():
    st.markdown("<h2 class='section-header'>Risk & Position Size Calculator</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Input Parameters")
        account_balance = st.number_input("Modal Akun (USD)", min_value=1.0, value=1000.0, step=100.0)
        risk_percentage = st.number_input("Risk per Trade (%)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
        entry_price = st.number_input("Entry Price", min_value=0.0001, value=1.0, format="%.4f", step=0.0001)
        stop_loss = st.number_input("Stop Loss", min_value=0.0001, value=0.9950, format="%.4f", step=0.0001)
        take_profit = st.number_input("Take Profit (Optional)", min_value=0.0, value=1.0100, format="%.4f", step=0.0001)
        
        calculate_button = st.button("Calculate", use_container_width=True)
    
    with col2:
        st.subheader("Results")
        
        if calculate_button:
            # Calculate position size and risk
            position_size_result = calculate_position_size(
                account_balance, risk_percentage, entry_price, stop_loss
            )
            
            # Calculate risk reward ratio if take profit is provided
            if take_profit > 0:
                rr_ratio = calculate_risk_reward_ratio(entry_price, stop_loss, take_profit)
            else:
                rr_ratio = None
            
            # Display results
            metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
            
            with metrics_col1:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.markdown(f"<div class='metric-value'>{position_size_result['position_size']:.2f} lots</div>", unsafe_allow_html=True)
                st.markdown("<div class='metric-label'>Position Size</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with metrics_col2:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.markdown(f"<div class='metric-value'>${position_size_result['risk_amount']:.2f}</div>", unsafe_allow_html=True)
                st.markdown("<div class='metric-label'>Risk Amount</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with metrics_col3:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                if rr_ratio:
                    st.markdown(f"<div class='metric-value'>{rr_ratio:.2f}</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='metric-value'>N/A</div>", unsafe_allow_html=True)
                st.markdown("<div class='metric-label'>Risk-to-Reward Ratio</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Additional information
            st.markdown("### Trade Details")
            trade_details = pd.DataFrame({
                "Parameter": ["Entry Price", "Stop Loss", "Pips at Risk", "Take Profit"],
                "Value": [
                    f"{entry_price:.4f}",
                    f"{stop_loss:.4f}",
                    f"{position_size_result['pips_at_risk']:.4f}",
                    f"{take_profit:.4f}" if take_profit > 0 else "Not set"
                ]
            })
            st.dataframe(trade_details, use_container_width=True, hide_index=True)
            
            # Visualization of risk to reward ratio if take profit is provided
            if rr_ratio:
                fig = go.Figure()
                
                # Determine if it's a buy or sell trade
                is_buy = entry_price < take_profit
                
                price_range = max(abs(entry_price - stop_loss), abs(entry_price - take_profit)) * 1.2
                y_min = min(entry_price, stop_loss, take_profit) - price_range * 0.1
                y_max = max(entry_price, stop_loss, take_profit) + price_range * 0.1
                
                # Add entry, stop loss, take profit lines
                fig.add_trace(go.Scatter(
                    x=[0, 1], y=[entry_price, entry_price],
                    mode='lines', name='Entry',
                    line=dict(color='blue', width=2)
                ))
                
                fig.add_trace(go.Scatter(
                    x=[0, 1], y=[stop_loss, stop_loss],
                    mode='lines', name='Stop Loss',
                    line=dict(color='red', width=2)
                ))
                
                fig.add_trace(go.Scatter(
                    x=[0, 1], y=[take_profit, take_profit],
                    mode='lines', name='Take Profit',
                    line=dict(color='green', width=2)
                ))
                
                # Update layout
                fig.update_layout(
                    title='Risk-to-Reward Visualization',
                    xaxis=dict(
                        showticklabels=False,
                        showgrid=False,
                        zeroline=False
                    ),
                    yaxis=dict(
                        title='Price',
                        range=[y_min, y_max]
                    ),
                    height=400,
                    margin=dict(l=0, r=0, t=40, b=0)
                )
                
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Input parameters and click 'Calculate' to see results.")

# Function to display Trade Journal
def show_trade_journal():
    st.markdown("<h2 class='section-header'>Manual Trade Journal</h2>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Add Trade", "Trade History"])
    
    with tab1:
        st.subheader("Add New Trade")
        
        col1, col2 = st.columns(2)
        
        with col1:
            trade_pair = st.text_input("Pair (e.g., EUR/USD)", value="EUR/USD")
            entry_price = st.number_input("Entry Price", min_value=0.0001, value=1.0, format="%.4f", step=0.0001)
            stop_loss = st.number_input("Stop Loss", min_value=0.0001, value=0.9950, format="%.4f", step=0.0001)
            take_profit = st.number_input("Take Profit", min_value=0.0, value=1.0100, format="%.4f", step=0.0001)
        
        with col2:
            position_size = st.number_input("Position Size (lots)", min_value=0.01, value=0.1, step=0.01)
            result_pips = st.number_input("Result (pips)", value=0.0, step=1.0)
            trade_status = st.selectbox("Outcome", options=["Win", "Loss"])
            notes = st.text_area("Notes", height=100)
        
        # Calculate RR if take profit is set
        rr = calculate_risk_reward_ratio(entry_price, stop_loss, take_profit) if take_profit > 0 else None
        
        if st.button("Add Trade to Journal", use_container_width=True):
            # Prepare trade data
            trade_data = {
                "pair": trade_pair,
                "entry_price": entry_price,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
                "position_size": position_size,
                "result": result_pips,
                "status": trade_status,
                "rr": rr if rr else 0,
                "notes": notes
            }
            
            # Add to journal
            if trade_journal.add_trade(trade_data):
                st.success("Trade added to journal successfully!")
            else:
                st.error("Failed to add trade to journal.")
    
    with tab2:
        st.subheader("Trade History")
        
        # Get trades from journal
        trades_df = trade_journal.get_trades()
        
        if not trades_df.empty:
            # Calculate statistics
            stats = calculate_trade_statistics(trades_df)
            
            # Display summary metrics
            metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
            
            with metrics_col1:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.markdown(f"<div class='metric-value'>{stats['winrate']:.1f}%</div>", unsafe_allow_html=True)
                st.markdown("<div class='metric-label'>Win Rate</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with metrics_col2:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.markdown(f"<div class='metric-value'>{stats['avg_rr']:.2f}</div>", unsafe_allow_html=True)
                st.markdown("<div class='metric-label'>Avg R:R Ratio</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with metrics_col3:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                value_class = "win" if stats['total_pnl'] >= 0 else "loss"
                st.markdown(f"<div class='metric-value {value_class}'>{stats['total_pnl']:.1f} pips</div>", unsafe_allow_html=True)
                st.markdown("<div class='metric-label'>Total P/L</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Win/Loss chart
            if stats['win_count'] > 0 or stats['loss_count'] > 0:
                fig = px.pie(
                    names=['Wins', 'Losses'],
                    values=[stats['win_count'], stats['loss_count']],
                    color=['Wins', 'Losses'],
                    color_discrete_map={'Wins': '#28a745', 'Losses': '#dc3545'},
                    title="Win/Loss Distribution"
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
            
            # Display trade history
            st.markdown("### Trade Records")
            
            # Format the dataframe for display
            display_df = trades_df.copy()
            
            # Convert date column to datetime if it's not
            if 'date' in display_df.columns:
                display_df['date'] = pd.to_datetime(display_df['date'])
                display_df['date'] = display_df['date'].dt.strftime("%Y-%m-%d %H:%M")
            
            # Format numeric columns
            for col in ['entry_price', 'stop_loss', 'take_profit']:
                if col in display_df.columns:
                    display_df[col] = display_df[col].map(lambda x: f"{x:.4f}" if pd.notnull(x) else "")
            
            if 'rr' in display_df.columns:
                display_df['rr'] = display_df['rr'].map(lambda x: f"{x:.2f}" if pd.notnull(x) else "")
            
            # Reorder columns for better display
            columns_order = [
                'date', 'pair', 'entry_price', 'stop_loss', 'take_profit', 
                'position_size', 'result', 'status', 'rr', 'notes'
            ]
            display_df = display_df[[col for col in columns_order if col in display_df.columns]]
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Add option to clear journal
            if st.button("Clear Journal", type="secondary"):
                if trade_journal.clear_trades():
                    st.success("Journal cleared successfully!")
                    st.experimental_rerun()
                else:
                    st.error("Failed to clear journal.")
        else:
            st.info("No trades in the journal yet. Add some trades to see them here.")

# Function to display Expected Profit Projection
def show_profit_projection():
    st.markdown("<h2 class='section-header'>Expected Profit Projection</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Input Parameters")
        
        # Get trade statistics if available
        trades_df = trade_journal.get_trades()
        stats = calculate_trade_statistics(trades_df) if not trades_df.empty else None
        
        # Set default values based on trade history if available
        default_rr = stats['avg_rr'] if stats and stats['avg_rr'] > 0 else 2.0
        default_winrate = stats['winrate'] if stats and stats['winrate'] > 0 else 40.0
        
        avg_rr = st.number_input("Average R:R Ratio", min_value=0.1, value=default_rr, step=0.1)
        winrate = st.number_input("Win Rate (%)", min_value=0.0, max_value=100.0, value=default_winrate, step=1.0)
        risk_per_trade = st.number_input("Risk per Trade (%)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
        
        # Add button to use values from journal
        if stats and not trades_df.empty:
            if st.button("Use Values from Journal", use_container_width=True):
                avg_rr = stats['avg_rr']
                winrate = stats['winrate']
        
        calculate_button = st.button("Calculate Projection", use_container_width=True)
    
    with col2:
        st.subheader("Projection Results")
        
        if calculate_button:
            # Calculate expected value
            ev_results = calculate_expected_value(avg_rr, winrate, risk_per_trade)
            
            # Display expected value per trade
            ev_per_trade = ev_results['expected_value_per_trade']
            ev_class = "win" if ev_per_trade >= 0 else "loss"
            
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-value {ev_class}'>{ev_per_trade:.2f}%</div>", unsafe_allow_html=True)
            st.markdown("<div class='metric-label'>Expected Value per Trade</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("")  # Add some space
            
            # Display projections
            st.markdown("### Projected Profit (% of Account)")
            
            projections_df = pd.DataFrame({
                "Number of Trades": list(ev_results['projections'].keys()),
                "Projected Profit (%)": list(ev_results['projections'].values())
            })
            
            # Create a bar chart for projections
            fig = px.bar(
                projections_df,
                x="Number of Trades",
                y="Projected Profit (%)",
                color="Projected Profit (%)",
                color_continuous_scale=["red", "#ffcc00", "green"],
                text="Projected Profit (%)"
            )
            
            fig.update_traces(
                texttemplate='%{text:.2f}%',
                textposition='outside'
            )
            
            fig.update_layout(
                height=400,
                margin=dict(l=0, r=0, t=10, b=0)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Interpretation
            st.markdown("### Interpretation")
            
            if ev_per_trade > 0:
                st.success(
                    f"Based on your parameters (Win Rate: {winrate}%, R:R: {avg_rr}, Risk: {risk_per_trade}%), "
                    f"your trading strategy has a positive expected value of {ev_per_trade:.2f}% per trade."
                )
                st.info(
                    f"With consistent execution, you can expect to grow your account by approximately "
                    f"{ev_results['projections'][100]:.2f}% over 100 trades."
                )
            else:
                st.error(
                    f"Based on your parameters (Win Rate: {winrate}%, R:R: {avg_rr}, Risk: {risk_per_trade}%), "
                    f"your trading strategy has a negative expected value of {ev_per_trade:.2f}% per trade."
                )
                st.warning(
                    "Consider adjusting your strategy to improve your win rate or risk-to-reward ratio."
                )
        else:
            st.info("Enter parameters and click 'Calculate Projection' to see results.")

# Display the selected feature
if app_mode == "Risk & Position Size Calculator":
    show_risk_calculator()
elif app_mode == "Manual Trade Journal":
    show_trade_journal()
elif app_mode == "Expected Profit Projection":
    show_profit_projection()

# Footer
st.markdown("---")
st.markdown("**Trade Tools** - Developed to help traders manage risk, track performance, and project profits.") 