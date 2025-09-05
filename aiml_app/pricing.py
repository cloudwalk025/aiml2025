from datetime import date

# Deadline for early registration
EARLY_DEADLINE = date(2025, 6, 30)

PRICES = {
    "regular_early": 400,
    "regular_late": 500,
    "student_early": 250,
    "student_late": 300,
    "listener_early": 150,
    "listener_late": 200,
}

def get_registration_price(reg_type):
    today = date.today()
    if "early" in reg_type and today > EARLY_DEADLINE:
        reg_type = reg_type.replace("early", "late")
    return PRICES[reg_type]
