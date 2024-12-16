def is_valid_number(input_str):
    """
    Check if the input contains only numeric characters.
    Returns True if input is valid, False otherwise.
    """
    return input_str.isdigit()

def main():
    MAX_RETRIES = 3  # Define the maximum number of retries
    retry_counter = 0  # Initialize the retry counter

    while retry_counter < MAX_RETRIES:
        user_input = input("Enter a number: ")

        if is_valid_number(user_input):
            print("Valid numeric input.")
            break  # Exit the loop if input is valid
        else:
            retry_counter += 1  # Increment the retry counter
            print("Invalid numeric input detected. Please enter only digits.")
            if retry_counter == MAX_RETRIES:
                print("You've reached the maximum number of retries. Exiting now.")

    # This code is part of the category two enhancement
    # It adds a retry mechanism to limit invalid attempts.