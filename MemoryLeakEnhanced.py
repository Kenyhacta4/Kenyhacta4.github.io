import time
import logging
import uuid

# Configure logging
logging.basicConfig(
    filename="application.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Function to validate inputs
def is_safe_input(user_input):
    """
    Check if the input contains unsafe SQL characters.
    Returns True if input is safe, False otherwise.
    """
    if ";" in user_input or "'" in user_input:
        logging.warning("Potential SQL injection attempt detected.")
        return False
    if not user_input.isdigit() or int(user_input) <= 0:
        logging.warning("Invalid input detected. Input must be a positive integer.")
        return False
    return True

# Function to allocate memory
def allocate_memory(size):
    if size <= 0:
        logging.error("Error: Invalid memory size requested.")
        print("Error: Invalid memory size.")
        return None
    try:
        start_time = time.time()  # Start logging time
        data = [0] * size  # Simulate memory allocation
        data[0] = 1  # Use the allocated memory
        end_time = time.time()  # End logging time
        logging.info(f"Memory allocation successful for size: {size}. Time taken: {end_time - start_time:.5f} seconds.")
        print(f"Memory allocation successful for size: {size}")
        print(f"Time taken for allocation: {end_time - start_time:.5f} seconds.")
        return data
    except MemoryError:
        logging.error("Error: Memory allocation failed.")
        print("Error: Memory allocation failed.")
        return None

# Function to authenticate user session
def generate_session_token():
    """
    Generate a unique session token to validate user session.
    """
    return str(uuid.uuid4())

# Main logic
MAX_RETRIES = 3  # Define the maximum number of retries
retry_counter = 0
session_token = generate_session_token()
logging.info(f"New session started with token: {session_token}")

while retry_counter < MAX_RETRIES:
    try:
        user_input = input("Enter the memory size to allocate (positive number): ")
        if is_safe_input(user_input):  # Validate input against SQL injection
            size = int(user_input)  # Convert to integer
            if allocate_memory(size):  # Check memory allocation
                logging.info(f"Operation completed successfully in session {session_token}.")
                print("Operation completed successfully.")
                break
        else:
            logging.warning(f"Unsafe input detected in session {session_token}.")
            print("Potential SQL injection detected. Please enter a valid number.")
    except ValueError as e:
        logging.error(f"Invalid input encountered: {e}.")
        print("Error: Please enter a valid integer.")
    retry_counter += 1
    if retry_counter == MAX_RETRIES:
        logging.warning(f"Max retries reached for session {session_token}. Exiting.")
        print("Max retries reached. Exiting.")

logging.info(f"Session {session_token} ended.")

    #This is the file that contains the first category enhancements
    #I chose to enhance the retry limits, memory allocation handling, and SQL injection prevention.
    #I also chose to add logging, performance, authentication, input validation, and retry limits. 
    
    #File also contains second category enhancment.
    #Logs the time taken for memory allocation.