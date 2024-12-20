def is_valid_number(input_str):
    """
    Validates whether the input string contains only numeric characters.
    Key Algorithmic Step:
    - Uses Python's `str.isdigit()` method to check if all characters are digits.
    - This method ensures input contains only valid numeric values.

    Data Structure Efficiency:
    - `str.isdigit()` has a time complexity of O(n), where n is the length of the string.
    - It efficiently validates input without the need for additional loops or condition checks.

    Parameters:
    - input_str (str): The user input string to validate.

    Returns:
    - bool: True if the input is numeric, False otherwise.
    """
    return input_str.isdigit()


def main():
    """
    Main function that implements a retry mechanism for user input validation.
    Prompts the user to enter a numeric input and validates it up to a set retry limit.

    Key Algorithmic Steps:
    - The program prompts the user to enter a numeric value.
    - The input is validated using `is_valid_number()` function.
    - A retry mechanism ensures the program only allows a limited number of invalid attempts.
    
    Data Structure Efficiency:
    - A simple integer counter (O(1) space complexity) is used for retry tracking.
    - `str` is used for input validation, which avoids unnecessary resource allocation.
    """
    MAX_RETRIES = 3  # Maximum number of retries allowed for invalid input
    retry_counter = 0  # Initialize the retry counter to track attempts

    print("### Numeric Input Validation with Retry Mechanism ###")

    # Retry loop to validate input
    while retry_counter < MAX_RETRIES:
        user_input = input("Enter a number: ")

        # Step 1: Validate input
        if is_valid_number(user_input):
            print("Valid numeric input. Thank you!")
            break  # Exit the loop upon successful validation
        else:
            retry_counter += 1  # Increment the retry counter
            print(f"Invalid input. Retry {retry_counter} of {MAX_RETRIES}. Please enter only digits.")
            
            # Step 2: Check for retry limit
            if retry_counter == MAX_RETRIES:
                print("You've reached the maximum number of retries. Exiting now.")

    print("Program completed.")


# Program Entry Point
if __name__ == "__main__":
    """
    Execution begins here.
    - Handles user input validation with retry limits.
    - Ensures invalid attempts are capped for better control.
    """
    main()
    
    # This code is part of the category two enhancement
    # It adds a retry mechanism to limit invalid attempts.