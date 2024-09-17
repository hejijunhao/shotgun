from reservations.models import Restaurant, Table, Administrator, Guest, OpeningSchedule, Reservation, MergedTable
from datetime import datetime, timedelta


def test_models():
    # Create a new restaurant
    gourmet_delight = Restaurant("Gourmet Delight", "123 Foodie St")

    # Add tables to the restaurant
    gourmet_delight.add_table(Table(1, 2))
    gourmet_delight.add_table(Table(2, 4, mergable=True))
    gourmet_delight.add_table(Table(3, 6))

    # Print restaurant info
    print(gourmet_delight)
    
    # Print all tables
    for table in gourmet_delight.get_tables():
        print(table)

    # Test available tables for different party sizes
    print("Available tables for 2 people:", [str(t) for t in gourmet_delight.get_available_tables(2)])
    print("Available tables for 5 people:", [str(t) for t in gourmet_delight.get_available_tables(5)])

def test_administrator():
    # Create a new administrator
    admin = Administrator("admin_user", "secure_password")

    # Test string representation
    print(admin)

    # Test password checking
    print("Correct password check:", admin.check_password("secure_password"))
    print("Incorrect password check:", admin.check_password("wrong_password"))

def test_guest():
    # Create a new guest
    guest = Guest("John Doe", "+1234567890", "john.doe@example.com")

    # Test string representation
    print(guest)

    # Test invalid phone number
    try:
        Guest("Jane Doe", "invalid_phone", "jane.doe@example.com")
    except ValueError as e:
        print("Invalid phone test passed:", str(e))

    # Test invalid email
    try:
        Guest("Bob Smith", "+1987654321", "invalid_email")
    except ValueError as e:
        print("Invalid email test passed:", str(e))

def test_opening_schedule():
    restaurant = Restaurant("Gourmet Delight", "123 Foodie St")

    # Add multiple sessions for Monday
    restaurant.add_opening_session("Monday", "09:00", "14:00")
    restaurant.add_opening_session("Monday", "17:00", "23:00")

    # Add a single session for Tuesday
    restaurant.add_opening_session("Tuesday", "11:00", "22:00")

    # Print the restaurant info (including schedule)
    print(restaurant)

    # Test if the restaurant is open
    print("Is open Monday at 10:00:", restaurant.is_open("Monday", "10:00"))
    print("Is open Monday at 15:00:", restaurant.is_open("Monday", "15:00"))
    print("Is open Monday at 20:00:", restaurant.is_open("Monday", "20:00"))
    print("Is open Tuesday at 12:00:", restaurant.is_open("Tuesday", "12:00"))

def test_reservation():
    # Create a guest
    guest = Guest("John Doe", "+1234567890", "john.doe@example.com")

    # Create a table
    table = Table("A", 4)

    # Create a reservation
    start_datetime = datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)  # 6:00 PM today
    reservation = Reservation(guest, 4, start_datetime, table)

    # Print reservation details
    print(reservation)

    # Test updating duration
    reservation.update_duration(timedelta(hours=3))
    print(f"Updated end time: {reservation.end_datetime.strftime('%H:%M')}")

    # Test updating tables
    new_table = Table("B", 6)
    reservation.update_tables(new_table)
    print(f"Updated table: {reservation.tables[0].id}")

    # Test to_dict method
    print(reservation.to_dict())

def test_table_merging_and_reservation():
    # Create tables
    table_a = Table("A", 2, mergable=False)
    table_b = Table("B", 2, mergable=False)
    table_c = Table("C", 2, mergable=True)
    table_d = Table("D", 2, mergable=True)

    # Attempt to merge non-mergable tables
    print(f"Attempt to merge A and B: {table_a.merge_with(table_b)}")

    # Merge mergable tables
    print(f"Merge C and D: {table_c.merge_with(table_d)}")

    # Create a merged table
    merged_cd = MergedTable(table_c, table_d)
    print(merged_cd)

    # Create a guest and a reservation with the merged table
    guest = Guest("John Doe", "+1234567890", "john.doe@example.com")
    start_datetime = datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)
    reservation = Reservation(guest, 4, start_datetime, merged_cd)
    print(reservation)

    # Unmerge tables after reservation
    merged_cd.unmerge()
    print(f"Table C status after unmerge: {table_c}")
    print(f"Table D status after unmerge: {table_d}")


if __name__ == "__main__":
    test_models()
    test_administrator()
    test_guest()
    test_opening_schedule()
    test_reservation()
    test_table_merging_and_reservation()