from datetime import datetime, timedelta

def calculate_due_date(statement_date):
    """Calculate due date based on statement date (typically 21 days after)"""
    statement_date = datetime.strptime(statement_date, '%Y-%m-%d')
    return (statement_date + timedelta(days=21)).strftime('%Y-%m-%d')

def validate_dates(statement_date, due_date):
    """Validate that due date is after statement date"""
    statement = datetime.strptime(statement_date, '%Y-%m-%d')
    due = datetime.strptime(due_date, '%Y-%m-%d')
    return due > statement

def get_status_color(status):
    """Return color code based on payment status"""
    colors = {
        'Paid': '#28a745',
        'Unpaid': '#dc3545',
        'Pending': '#ffc107'
    }
    return colors.get(status, '#6c757d')
