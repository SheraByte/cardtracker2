import streamlit as st
from storage import CardStorage
from components import render_add_card_form, render_card_list

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