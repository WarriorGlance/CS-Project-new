import mysql.connector as MyS
Pass = input("Enter MYSQL password:")

if Pass:
     # Connect to MySQL server
    conn = MyS.connect(
        host="localhost",
        user="root",
        password=Pass
    )

    cursor = conn.cursor()

    # Create database if it doesn't exist
    cursor.execute(
        "CREATE DATABASE IF NOT EXISTS car_dealership"
    )

    cursor.close()
    conn.close()
    # Now connect to the database
    conn = MyS.connect(
        host="localhost",
        user="root",
        password=Pass,
        database="car_dealership"
    )
    cursor = conn.cursor()
    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            car_id INT PRIMARY KEY,
            brand VARCHAR(50),
            model VARCHAR(50),
            year INT,
            color VARCHAR(30),
            fuel_type VARCHAR(20),
            transmission VARCHAR(20),
            price DECIMAL(12,2),
            stock INT
        )
    """)
    conn.commit()
    # Insert starter rows only when the table is empty.
    cursor.execute("SELECT COUNT(*) FROM cars")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            """INSERT INTO cars
               (car_id, brand, model, year, color, fuel_type, transmission, price, stock)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);""",
            [
                (101, 'Toyota', 'Corolla', 2024, 'White', 'Petrol', 'Automatic', 2200000, 5),
                (102, 'Honda', 'City', 2023, 'Silver', 'Petrol', 'Manual', 1800000, 3),
                (103, 'Hyundai', 'Creta', 2024, 'Black', 'Diesel', 'Automatic', 2500000, 4),
                (104, 'Maruti Suzuki', 'Baleno', 2023, 'Blue', 'Petrol', 'Manual', 1100000, 7)
            ],
        )
    def ViewCars():
        cursor.execute("SELECT * FROM cars")
        cars = cursor.fetchall()
        headers = [description[0] for description in cursor.description]

        if cars:
            widths = [max(len(str(header)), *(len(str(row[i])) for row in cars))
                      for i, header in enumerate(headers)]
            separator = "+-" + "-+-".join("-" * width for width in widths) + "-+"
            print(separator)
            print("| " + " | ".join(str(header).ljust(width)
                                  for header, width in zip(headers, widths)) + " |")
            print(separator)
            for car in cars:
                print("| " + " | ".join(str(value).ljust(width)
                                      for value, width in zip(car, widths)) + " |")
            print(separator)
        else:
            print("No cars found.")

    def AddCar():
        n = int(input("Enter number of cars to add: "))
        for _ in range(n):
            car_id = int(input("Enter Car ID: "))
            brand = input("Enter Brand: ")
            model = input("Enter Model: ")
            year = int(input("Enter Year: "))
            color = input("Enter Color: ")
            fuel_type = input("Enter Fuel Type: ")
            transmission = input("Enter Transmission: ")
            price = float(input("Enter Price: "))
            stock = int(input("Enter Stock: "))
            cursor.execute(
                """INSERT INTO cars
                   (car_id, brand, model, year, color, fuel_type, transmission, price, stock)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);""",
                (car_id, brand, model, year, color, fuel_type, transmission, price, stock)
            )
        print("Cars suceessfully added!")

    conn.commit()

    while True:
        print("Welcome to the Car Dealership Management System")
        print("1. View Cars")
        print("2. Add Car")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            ViewCars()
        elif choice == '2':
            AddCar()
        elif choice == '3':
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please try again.")
    cursor.close()
    conn.close()
