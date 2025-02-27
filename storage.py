from datetime import datetime
import pandas as pd

# In-memory storage
class CardStorage:
    def __init__(self):
        self.cards = pd.DataFrame(columns=[
            'id', 'nickname', 'statement_date', 'due_date', 
            'payment_status', 'credit_limit', 'notes', 
            'created_at', 'updated_at'
        ])
        
    def add_card(self, card_data):
        card_data['id'] = len(self.cards) + 1
        card_data['created_at'] = datetime.now()
        card_data['updated_at'] = datetime.now()
        self.cards = pd.concat([self.cards, pd.DataFrame([card_data])], ignore_index=True)
        return card_data['id']
    
    def update_card(self, card_id, card_data):
        card_data['updated_at'] = datetime.now()
        self.cards.loc[self.cards['id'] == card_id, card_data.keys()] = card_data.values()
        
    def get_card(self, card_id):
        return self.cards[self.cards['id'] == card_id].iloc[0].to_dict() if len(self.cards[self.cards['id'] == card_id]) > 0 else None
    
    def get_all_cards(self):
        return self.cards
    
    def delete_card(self, card_id):
        self.cards = self.cards[self.cards['id'] != card_id]
