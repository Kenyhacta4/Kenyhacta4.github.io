import time  # Import for performance tracking
import logging  # Import for security and error logging
import uuid  # Import for session management and token generation

# --------------------------- Logging Configuration --------------------------- #
logging.basicConfig(
    filename="application.log",
    level=logging.INFO,  # Log level: INFO for general logs, WARNING for alerts, ERROR for critical errors
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# --------------------------- Input Validation Function --------------------------- #
def is_safe_input(user_input):
    """
    Validates user input for safety and correctness.
    
    Key Algorithmic Steps:
    - Checks for SQL injection attempts by identifying unsafe characters (';' and "'").
    - Ensures the input consists of only positive integers using `isdigit()` and range validation.
    
    Data Structure Efficiency:
    - String checks (`in`) are O(n), where n is the length of the string.
    - Ensuring inputs are integers reduces security risks and program crashes.

    Parameters:
    - user_input (str): The input string entered by the user.

    Returns:
    - bool: True if input is safe and valid; False otherwise.
    """
    if ";" in user_input or "'" in user_input:  # Prevent SQL injection characters
        logging.warning("Potential SQL injection attempt detected.")
        return False
    if not user_input.isdigit() or int(user_input) <= 0:  # Validate positive integers
        logging.warning("Invalid input detected. Input must be a positive integer.")
        return False
    return True


# --------------------------- Memory Allocation Function --------------------------- #
def allocate_memory(size):
    """
    Simulates memory allocation for a given size and logs performance metrics.

    Key Algorithmic Steps:
    - Validates the size to ensure it is greater than zero.
    - Allocates memory by creating a list of zeroes to simulate memory consumption.
    - Logs the time taken for memory allocation to monitor performance.
    
    Data Structure Efficiency:
    - The list data structure (`[0] * size`) has O(n) time complexity for initialization.
    - Using exceptions (`MemoryError`) ensures safe failure handling for large inputs.

    Parameters:
    - size (int): The size of memory to allocate.

    Returns:
    - list: Simulated memory if allocation is successful; None otherwise.
    """
    if size <= 0:
        logging.error("Error: Invalid memory size requested.")
        print("Error: Invalid memory size.")
        return None
    try:
        start_time = time.time()  # Start performance logging
        data = [0] * size  # Simulate memory allocation
        data[0] = 1  # Simulate memory usage
        end_time = time.time()  # End performance logging
        logging.info(f"Memory allocation successful for size: {size}. "
                     f"Time taken: {end_time - start_time:.5f} seconds.")
        print(f"Memory allocation successful for size: {size}")
        print(f"Time taken for allocation: {end_time - start_time:.5f} seconds.")
        return data
    except MemoryError:
        logging.error("Error: Memory allocation failed due to insufficient memory.")
        print("Error: Memory allocation failed.")
        return None


# --------------------------- Session Authentication --------------------------- #
def generate_session_token():
    """
    Generates a unique session token for user authentication and logging.

    Key Algorithmic Steps:
    - Uses UUID4 to generate a unique token.
    - Provides a unique identifier for each program execution.

    Returns:
    - str: A string representation of the unique session token.
    """
    return str(uuid.uuid4())


# --------------------------- Main Logic --------------------------- #
def main():
    """
    Main function to manage user input, memory allocation, and logging.
    Includes:
    - Input validation with retry limits.
    - Memory allocation and performance logging.
    - Session authentication using unique tokens.

    Key Enhancements:
    - Retry mechanism limits invalid attempts to enhance program robustness.
    - Logging tracks security events, errors, and performance metrics.
    - Session tokens provide traceable and secure user identification.
    """
    MAX_RETRIES = 3  # Define maximum number of retries for invalid input
    retry_counter = 0  # Initialize retry counter
    session_token = generate_session_token()  # Start a session with a unique token

    logging.info(f"New session started with token: {session_token}")
    print("### Secure Memory Allocation Program ###")
    print(f"Session Token: {session_token}\n")

    while retry_counter < MAX_RETRIES:
        try:
            # Step 1: Take user input
            user_input = input("Enter the memory size to allocate (positive number): ")

            # Step 2: Validate input for safety and correctness
            if is_safe_input(user_input):
                size = int(user_input)  # Convert valid input to integer
                # Step 3: Attempt memory allocation
                if allocate_memory(size):
                    logging.info(f"Operation completed successfully in session {session_token}.")
                    print("Operation completed successfully.")
                    break
            else:
                logging.warning(f"Unsafe input detected in session {session_token}.")
                print("Potential SQL injection detected. Please enter a valid number.")
        
        except ValueError as e:
            logging.error(f"Invalid input encountered: {e}.")
            print("Error: Please enter a valid integer.")

        # Step 4: Retry logic for invalid inputs
        retry_counter += 1
        print(f"Retry {retry_counter} of {MAX_RETRIES}")
        if retry_counter == MAX_RETRIES:
            logging.warning(f"Max retries reached for session {session_token}. Exiting.")
            print("Max retries reached. Exiting.")

    # End the session
    logging.info(f"Session {session_token} ended.")
    print(f"Session {session_token} has ended. Thank you for using the program.")


# --------------------------- Program Entry Point --------------------------- #
if __name__ == "__main__":
    """
    Execution begins here.
    - Initializes session authentication.
    - Manages user input validation, memory allocation, and performance logging.
    """
    main()

    #This is the file that contains the first category enhancements
    #I chose to enhance the retry limits, memory allocation handling, and SQL injection prevention.
    #I also chose to add logging, performance, authentication, input validation, and retry limits. 
    
    #File also contains second category enhancment.
    #Logs the time taken for memory allocation.