# --------------------------- Input Validation Function --------------------------- #
def is_valid_user_input(input_str):
    """
    Validates the user input for potential SQL injection attempts.

    Key Algorithmic Steps:
    - Checks for unsafe characters (`;` and `'`) commonly used in SQL injection attacks.
    - Returns a Boolean value indicating the safety of the input.

    Data Structure Efficiency:
    - The 'in' operator checks for characters in O(n) time, where n is the length of the string.
    - String validation prevents security vulnerabilities and enhances program reliability.

    Parameters:
    - input_str (str): The input string provided by the user.

    Returns:
    - bool: True if the input is safe; False otherwise.
    """
    return ";" not in input_str and "'" not in input_str


# --------------------------- Retry Mechanism Logic --------------------------- #
def main():
    """
    Main function to validate user input and implement a retry mechanism.
    
    Key Enhancements:
    - Input validation to detect SQL injection attempts.
    - Retry mechanism to cap the number of invalid input attempts to a defined maximum.
    - Security-focused error messages provide feedback without exposing system details.

    Algorithmic Steps:
    - Use a while loop to allow multiple input attempts.
    - Validate each input using `is_valid_user_input`.
    - Block attempts after reaching the retry limit to improve security.

    Data Structure Efficiency:
    - Retry logic uses a simple counter, which is O(1) in time and space complexity.
    """
    MAX_RETRIES = 3  # Define the maximum number of retries
    retry_counter = 0  # Initialize retry counter

    print("### User Input Validation Program ###")
    while retry_counter < MAX_RETRIES:
        # Step 1: Take user input
        user_input = input("Enter a username: ")

        # Step 2: Validate input
        if is_valid_user_input(user_input):
            print("Valid user input.")  # Successful input
            break
        else:
            retry_counter += 1  # Increment the retry counter
            print("SQL injection attempt blocked. Please try again.")

            # Step 3: Handle maximum retries
            if retry_counter == MAX_RETRIES:
                print("You've reached the maximum number of retries. Exiting now.")

    # Step 4: End of program
    print("Program has ended. Thank you for using the input validator.")


# --------------------------- Program Entry Point --------------------------- #
if __name__ == "__main__":
    """
    Execution starts here.
    - Manages input validation and retry logic.
    - Ensures user input is free from SQL injection attempts.
    """
    main()
    
#Contains category two enhancement
#Enhancement validates user input to prevent SQL injection attempts and includes a retry mechanism.
