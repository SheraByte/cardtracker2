import streamlit as st
import pandas as pd
from storage import CardStorage

# Access the shared session state
if 'card_storage' not in st.session_state:
    st.session_state.card_storage = CardStorage()

st.title("💳 Card Details")

cards_df = st.session_state.card_storage.get_all_cards()

if len(cards_df) == 0:
    st.info("No credit cards added yet")
else:
    # Create a simplified view with only name, limit, and remarks
    details_df = cards_df[['nickname', 'credit_limit', 'notes']]
    
    # Rename columns for better display
    details_df.columns = ['Card Name', 'Credit Limit', 'Remarks']
    
    # Format credit limit as currency
    details_df['Credit Limit'] = details_df['Credit Limit'].apply(lambda x: f"${x:,.2f}")
    
    # Display as a clean table
    st.dataframe(
        details_df,
        hide_index=True,
        column_config={
            "Card Name": st.column_config.TextColumn("Card Name", width="medium"),
            "Credit Limit": st.column_config.TextColumn("Credit Limit", width="small"),
            "Remarks": st.column_config.TextColumn("Remarks", width="large"),
        }
    )
