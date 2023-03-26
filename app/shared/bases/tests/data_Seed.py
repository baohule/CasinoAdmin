from app.shared.bases.base_model import DataSeeder

DataSeeder(number_of_users=1000, exclude_list=[
    'bet_detail_history','payment_history', 'action_history', 'admin', 'agent', 'game_list','balance', 'user']).generate()
