from app.shared.bases.base_model import DataSeeder

DataSeeder(
    number_of_records=1000,
    exclude_list=[
        "bet_detail_history",
        "payment_history",
        "action_history",
        "game_list",
        "balance",
        "admin",

    ],
).generate()
