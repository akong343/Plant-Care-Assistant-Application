def safe_input(prompt, type_func=str):
    while True:
        try:
            return type_func(input(prompt))
        except ValueError:
            print("Invalid input. Please try again.")

# Modify the main function calls for input validation
watering_frequency = safe_input("Enter watering frequency (days): ", int)
