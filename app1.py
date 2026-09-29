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

    def UpdateCar():
        print("Choose what to update.")
        print("1.Car Id\n2.Brand\n3.Model\n4.Year\n5.Color\n6.Fuel\n7.Transmission\n8.Price\n9.Stock")
        ch = int(input("Enter option"))
        id = int(input("Enter Car Id to update"))
        if ch == 1:
            new_id = int(input("Enter new Car Id: "))
            cursor.execute("UPDATE cars SET car_id = %s WHERE car_id = %s", (new_id, id))
        elif ch == 2:
            new_brand = input("Enter new Brand: ")
            cursor.execute("UPDATE cars SET brand = %s WHERE car_id = %s", (new_brand, id))
        elif ch == 3:
            new_model = input("Enter new Model: ")
            cursor.execute("UPDATE cars SET model = %s WHERE car_id = %s", (new_model, id))
        elif ch == 4:
            new_year = int(input("Enter new Year: "))
            cursor.execute("UPDATE cars SET year = %s WHERE car_id = %s", (new_year, id))
        elif ch == 5:
            new_color = input("Enter new Color: ")
            cursor.execute("UPDATE cars SET color = %s WHERE car_id = %s", (new_color, id))
        elif ch == 6:
            new_fuel = input("Enter new Fuel Type: ")
            cursor.execute("UPDATE cars SET fuel_type = %s WHERE car_id = %s", (new_fuel, id))
        elif ch == 7:
            new_transmission = input("Enter new Transmission: ")
            cursor.execute("UPDATE cars SET transmission = %s WHERE car_id = %s", (new_transmission, id))
        elif ch == 8:
            new_price = float(input("Enter new Price: "))
            cursor.execute("UPDATE cars SET price = %s WHERE car_id = %s", (new_price, id))
        elif ch == 9:
            new_stock = int(input("Enter new Stock: "))
            cursor.execute("UPDATE cars SET stock = %s WHERE car_id = %s", (new_stock, id))
        else:
            print("Invalid choice.")
            return

        conn.commit()
        print("Car updated successfully.")

    def DeleteCar():
        car_id = int(input("Enter Car ID to delete: "))
        cursor.execute("SELECT COUNT(*) FROM cars WHERE car_id = %s", (car_id,))
        if cursor.fetchone()[0] == 0:
            print("Car ID not found.")
            return

        cursor.execute("DELETE FROM cars WHERE car_id = %s", (car_id,))
        conn.commit()
        print("Car deleted successfully.")

    def SearchCars():
        term = input("Enter brand, model, or color to search: ").strip()
        cursor.execute(
            """SELECT * FROM cars
               WHERE brand LIKE %s OR model LIKE %s OR color LIKE %s""",
            (f"%{term}%", f"%{term}%", f"%{term}%")
        )
        cars = cursor.fetchall()
        if cars:
            headers = [description[0] for description in cursor.description]
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
            print("No matching cars found.")

    while True:
        print("Welcome to the Car Dealership Management System")
        print("1. View Cars")
        print("2. Add Car")
        print("3. Update Car")
        print("4. Delete Car")
        print("5. Search Cars")
        print("6. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            ViewCars()
        elif choice == '2':
            AddCar()
        elif choice == '3':
            UpdateCar()
        elif choice == '4':
            DeleteCar()
        elif choice == '5':
            SearchCars()
        elif choice == '6':
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please try again.")
    cursor.close()
    conn.close()
