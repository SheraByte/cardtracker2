import streamlit as st
from datetime import datetime
from utils import calculate_due_date, validate_dates, get_status_color

def render_add_card_form():
    """Render the add card form"""
    with st.form("add_card_form"):
        nickname = st.text_input("Card Nickname", key="new_nickname")
        statement_date = st.date_input("Statement Date", key="new_statement_date")
        due_date = st.date_input("Due Date", key="new_due_date")

        credit_limit = st.number_input("Credit Limit", min_value=0.0, key="new_credit_limit")
        payment_status = st.selectbox("Payment Status", 
                                    options=['Unpaid', 'Pending', 'Paid'],
                                    key="new_payment_status")
        notes = st.text_area("Notes", key="new_notes")

        submitted = st.form_submit_button("Add Card")

        if submitted:
            if not nickname:
                st.error("Card nickname is required")
                return None

            card_data = {
                'nickname': nickname,
                'statement_date': statement_date.strftime('%Y-%m-%d'),
                'due_date': due_date.strftime('%Y-%m-%d'),
                'payment_status': payment_status,
                'credit_limit': credit_limit,
                'notes': notes
            }

            if not validate_dates(card_data['statement_date'], card_data['due_date']):
                st.error("Due date must be after statement date")
                return None

            return card_data
    return None

def render_card_list(cards_df, on_status_change, on_delete=None, show_full_details=False):
    """Render the list of cards"""
    if len(cards_df) == 0:
        st.info("No credit cards added yet")
        return

    # Filtering
    status_filter = st.selectbox("Filter by Status", 
                                options=['All', 'Unpaid', 'Pending', 'Paid'])

    if status_filter != 'All':
        cards_df = cards_df[cards_df['payment_status'] == status_filter]

    # Sorting
    sort_by = st.selectbox("Sort by", 
                          options=['Due Date', 'Statement Date', 'Card Nickname'])
    sort_column = {
        'Due Date': 'due_date',
        'Statement Date': 'statement_date',
        'Card Nickname': 'nickname'
    }[sort_by]
    cards_df = cards_df.sort_values(sort_column)

    # Display cards
    for _, card in cards_df.iterrows():
        with st.container():
            if show_full_details:
                col1, col2, col3, col4 = st.columns([2, 2, 1, 1])

                with col1:
                    st.subheader(card['nickname'])
                    st.write(f"Statement Date: {card['statement_date']}")
                    st.write(f"Due Date: {card['due_date']}")

                with col2:
                    st.write(f"Credit Limit: Rs.{card['credit_limit']:,.2f}")
                    st.write(f"Notes: {card['notes']}")

                with col3:
                    status = st.selectbox(
                        "Status",
                        options=['Unpaid', 'Pending', 'Paid'],
                        key=f"status_{card['id']}",
                        index=['Unpaid', 'Pending', 'Paid'].index(card['payment_status'])
                    )

                    if status != card['payment_status']:
                        on_status_change(card['id'], status)

                with col4:
                    if on_delete and st.button("Delete", key=f"delete_{card['id']}", type="secondary"):
                        on_delete(card['id'])
            else:
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.subheader(card['nickname'])
                    st.write(f"Statement Date: {card['statement_date']}")
                    st.write(f"Due Date: {card['due_date']}")

                with col2:
                    st.markdown(
                        f'<div style="padding: 10px; border-radius: 5px; '
                        f'background-color: {get_status_color(card["payment_status"])}; '
                        f'color: white; text-align: center;">'
                        f'{card["payment_status"]}</div>',
                        unsafe_allow_html=True
                    )

            st.markdown("<hr>", unsafe_allow_html=True)
