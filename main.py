import json  # Retains user input data
import time  # For sleeping to simulate reminders
from datetime import datetime, timedelta  # For tracking time

class User:
    def __init__(self, username, password, email):
        self.userID = None  # To be generated later
        self.username = username
        self.password = password
        self.email = email

    def create_profile(self):
        pass

    def authenticate(self, password):
        return self.password == password

    def logout(self):
        return True


class Plant:
    def __init__(self, species, watering_frequency, health_status, last_watered=None, plantID=None):
        self.plantID = plantID  # To be generated later or loaded from JSON
        self.species = species
        self.watering_frequency = watering_frequency
        self.health_status = health_status
        self.last_watered = last_watered or datetime.now()  # Keep track of last watering date

    def add_plant(self):
        pass

    def update_health(self, new_status):
        self.health_status = new_status

    def delete_plant(self):
        pass

    def needs_watering(self):
        """Check if the plant needs watering based on the frequency."""
        return (datetime.now() - self.last_watered) > timedelta(days=self.watering_frequency)

    def water_plant(self):
        """Water the plant and update the last watered date."""
        self.last_watered = datetime.now()


def load_data(filename):
    """Load data from a JSON file."""
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"users": [], "plants": []}


def save_data(filename, data):
    """Save data to a JSON file."""
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def main():
    data_file = 'plants_data.json'
    data = load_data(data_file)  # Load data at the start

    users = data["users"]
    plants = data["plants"]

    while True:
        print("Welcome to the Plant Care Assistant")
        choice = input("1. Register\n2. Login\n3. Exit\nChoose an option: ")

        if choice == '1':  # User Registration
            username = input("Enter username: ")
            password = input("Enter password: ")
            email = input("Enter email: ")
            new_user = User(username, password, email)
            users.append(new_user.__dict__)  # Store user as a dictionary
            print("User registered successfully!")
            save_data(data_file, {"users": users, "plants": plants})  # Save on registration

        elif choice == '2':  # User Login
            username = input("Enter username: ")
            password = input("Enter password: ")
            user = next((u for u in users if u['username'] == username), None)

            if user and user['password'] == password:
                print("Login successful!")
                while True:
                    plant_choice = input("1. Add Plant\n2. View Plants\n3. Edit Plant\n4. Remove Plant\n5. Check Reminders\n6. Exit\nChoose an option: ")
                    
                    if plant_choice == '1':  # Add Plant
                        species = input("Enter plant species: ")
                        watering_frequency = int(input("Enter watering frequency (days): "))
                        health_status = input("Enter health status: ")
                        new_plant = Plant(species, watering_frequency, health_status)
                        plants.append(new_plant.__dict__)
                        print("Plant added successfully!")
                        save_data(data_file, {"users": users, "plants": plants})  # Save on plant addition

                    elif plant_choice == '2':  # View Plants
                        if not plants:
                            print("No plants added yet.")
                        else:
                            print("Your plants:")
                            for index, plant in enumerate(plants):
                                print(f"{index + 1}. {plant['species']} - Water every {plant['watering_frequency']} days - Health: {plant['health_status']}")

                    elif plant_choice == '3':  # Edit Plant
                        if not plants:
                            print("No plants to edit.")
                        else:
                            plant_index = int(input("Enter the number of the plant to edit: ")) - 1
                            if 0 <= plant_index < len(plants):
                                species = input("Enter new plant species (leave blank to keep current): ")
                                watering_frequency = input("Enter new watering frequency (days, leave blank to keep current): ")
                                health_status = input("Enter new health status (leave blank to keep current): ")

                                # Update plant information if a new value is provided
                                if species:
                                    plants[plant_index]['species'] = species
                                if watering_frequency:
                                    plants[plant_index]['watering_frequency'] = int(watering_frequency)
                                if health_status:
                                    plants[plant_index]['health_status'] = health_status

                                print(f"{plants[plant_index]['species']} has been updated.")
                                save_data(data_file, {"users": users, "plants": plants})  # Save on plant edit
                            else:
                                print("Invalid plant selection.")

                    elif plant_choice == '4':  # Remove Plant
                        if not plants:
                            print("No plants to remove.")
                        else:
                            plant_index = int(input("Enter the number of the plant to remove: ")) - 1
                            if 0 <= plant_index < len(plants):
                                removed_plant = plants.pop(plant_index)
                                print(f"{removed_plant['species']} has been removed.")
                                save_data(data_file, {"users": users, "plants": plants})  # Save on plant removal
                            else:
                                print("Invalid plant selection.")

                    elif plant_choice == '5':  # Check Reminders
                        for index, plant in enumerate(plants):
                            p = Plant(**plant)  # Create a Plant object to use methods
                            if p.needs_watering():
                                print(f"{p.species} needs watering.")
                            else:
                                print(f"{p.species} is okay for now.")

                        # Simulate the reminder for watering action
                        time.sleep(5)  # Sleep for 5 seconds to simulate waiting for reminders
                        print("Reminders checked.")

                    elif plant_choice == '6':
                        break
                    else:
                        print("Invalid option.")

            else:
                print("Invalid username or password.")

        elif choice == '3':  # Exit
            print("Exiting...")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
