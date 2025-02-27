import streamlit as st
from storage import CardStorage
from components import render_add_card_form, render_card_list
from utils import calculate_due_date
from datetime import datetime

# Access the shared session state
if 'card_storage' not in st.session_state:
    st.session_state.card_storage = CardStorage()

st.title("💳 Add/Modify Credit Cards")

# Add New Card Section
st.header("Add New Credit Card")
new_card_data = render_add_card_form()

if new_card_data:
    st.session_state.card_storage.add_card(new_card_data)
    st.success("Card added successfully!")
    
    # Clear the form inputs in session state
    if "new_nickname" in st.session_state:
        st.session_state.new_nickname = ""
    if "new_credit_limit" in st.session_state:
        st.session_state.new_credit_limit = 0.0
    if "new_notes" in st.session_state:
        st.session_state.new_notes = ""
    if "new_payment_status" in st.session_state:
        st.session_state.new_payment_status = "Unpaid"
        
    st.rerun()

# Quick Date Update Section
st.header("Quick Date Update")
cards = st.session_state.card_storage.get_all_cards()
if len(cards) > 0:
    selected_card = st.selectbox(
        "Select Card to Update",
        options=cards['nickname'].tolist(),
        key="quick_update_card"
    )

    card_idx = cards[cards['nickname'] == selected_card].index[0]
    card = cards.iloc[card_idx].to_dict()

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        new_statement_date = st.date_input(
            "New Statement Date",
            datetime.strptime(card['statement_date'], '%Y-%m-%d').date(),
            key="quick_statement_update"
        )

    with col2:
        auto_calculate = st.checkbox("Auto-calculate Due Date (21 days)", value=True)
        if auto_calculate:
            new_due_date = calculate_due_date(new_statement_date.strftime('%Y-%m-%d'))
            st.info(f"Calculated Due Date: {new_due_date}")
        else:
            new_due_date = st.date_input(
                "New Due Date",
                datetime.strptime(card['due_date'], '%Y-%m-%d').date(),
                key="quick_due_update"
            ).strftime('%Y-%m-%d')

    with col3:
        if st.button("Update Dates", type="primary"):
            updated_card = card.copy()
            updated_card['statement_date'] = new_statement_date.strftime('%Y-%m-%d')
            updated_card['due_date'] = new_due_date
            st.session_state.card_storage.update_card(card['id'], updated_card)
            st.success("Dates updated successfully!")
            st.rerun()

# Existing Cards Section
st.header("Modify Existing Cards")

def handle_status_change(card_id, new_status):
    card = st.session_state.card_storage.get_card(card_id)
    if card:
        card['payment_status'] = new_status
        st.session_state.card_storage.update_card(card_id, card)
        st.rerun()

def handle_delete(card_id):
    if st.session_state.card_storage.delete_card(card_id):
        st.success("Card deleted successfully!")
        st.rerun()

render_card_list(
    st.session_state.card_storage.get_all_cards(),
    handle_status_change,
    handle_delete,
    show_full_details=True
)
