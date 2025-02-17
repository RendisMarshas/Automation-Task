from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import time

# "Helper function to wait for and click elements with retries
def wait_and_click(driver, by, value, timeout=10, retries=3):
    for attempt in range(retries):
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(1)
            element.click()
            return True
        except Exception as e:
            print(f"Error clicking {value} on attempt {attempt + 1}: {e}")
            time.sleep(2)
    return False

# Helper function to wait for and input text into elements
def wait_and_send_keys(driver, by, value, keys, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        element.clear()
        element.send_keys(keys)
        return True
    except Exception as e:
        print(f"Error inputting text to {value}: {e}")
        return False

# Handle the account creation process with detailed logging
def create_new_account(driver):
    print("Starting account creation process...")
    
    # Wait for dashboard to load completely
    time.sleep(5)
    
    try:
        # Click Open New Account with retry logic
        for attempt in range(3):
            try:
                print(f"Attempting to click 'Open New Account' (attempt {attempt + 1}/3)")
                # Try to find the element first
                open_account_link = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.LINK_TEXT, "Open New Account"))
                )
                # Scroll it into view
                driver.execute_script("arguments[0].scrollIntoView(true);", open_account_link)
                time.sleep(2)  # Wait for scroll to complete
                
                # Check if element is visible
                if open_account_link.is_displayed():
                    open_account_link.click()
                    print("Successfully clicked 'Open New Account' link")
                    break
                else:
                    print("'Open New Account' link is not visible")
                    
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(3)
        
        # Wait for the account creation form
        print("Waiting for account type dropdown...")
        account_type = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "type"))
        )
        
        # Select account type
        print("Selecting account type...")
        Select(account_type).select_by_visible_text("SAVINGS")
        time.sleep(3)  # Wait for form update
        
        # Wait for the from account dropdown to be populated
        print("Waiting for 'fromAccountId' dropdown...")
        from_account = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "fromAccountId"))
        )
        
        # Ensure the dropdown has options
        select = Select(from_account)
        if len(select.options) > 0:
            select.select_by_index(0)
            print(f"Selected account from dropdown. Available options: {len(select.options)}")
        else:
            print("No accounts available in the dropdown")
        
        # Click the submit button
        print("Attempting to click 'Open New Account' button...")
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@value='Open New Account']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        time.sleep(2)
        submit_button.click()
        
        # Wait for success message or new account number
        print("Waiting for confirmation...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Account Opened!')]"))
        )
        print("Account created successfully!")
        return True
        
    except Exception as e:
        print(f"Error in create_new_account function: {e}")
        return False

# Detailed function for transferring funds
def transfer_funds(driver):
    print("Starting transfer funds process...")
    
    try:
        # Click Transfer Funds link
        print("Attempting to click 'Transfer Funds' link...")
        transfer_funds_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Transfer Funds"))
        )
        transfer_funds_link.click()
        print("Successfully clicked 'Transfer Funds' link")
        
        # Wait for the transfer form to load
        time.sleep(3)
        
        # Find and interact with the 'To Account' dropdown
        print("Locating 'To Account' dropdown...")
        try:
            to_account_dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "toAccountId"))
            )
            
            # Create Select object
            select_to_account = Select(to_account_dropdown)
            
            # Log available options
            print("Available 'To Account' options:")
            for option in select_to_account.options:
                print(f"- {option.text}")
            
            # Select the second account if available
            if len(select_to_account.options) > 1:
                select_to_account.select_by_index(1)
                print("Selected second account in dropdown")
            else:
                print("Only one account available")
        except Exception as e:
            print(f"Error with 'To Account' dropdown: {e}")
            return False
        
        # Enter transfer amount
        print("Entering transfer amount...")
        amount_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "amount"))
        )
        amount_field.clear()
        amount_field.send_keys("100")
        print("Entered transfer amount: 100")
        
        # Submit transfer
        print("Submitting transfer...")
        transfer_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@value='Transfer']"))
        )
        transfer_button.click()
        
        # Wait for transfer confirmation
        print("Waiting for transfer confirmation...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Transfer Complete!')]"))
        )
        
        print("Transfer completed successfully!")
        return True
    
    except Exception as e:
        print(f"Error during transfer funds process: {e}")
        return False

def main():
    # Set up Chrome driver with additional options
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Add this option to disable the TensorFlow warning
    options.add_argument("--disable-features=EnableTensorflowTensorrt")

    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Navigate to the website
        driver.get("https://parabank.parasoft.com/parabank/index.htm")
        
        # Click Register
        if not wait_and_click(driver, By.LINK_TEXT, "Register"):
            raise Exception("Could not click Register button")

        # Get user input
        registration_data = {
            "customer.firstName": input("Enter your first name: "),
            "customer.lastName": input("Enter your last name: "),
            "customer.address.street": input("Enter your address: "),
            "customer.address.city": input("Enter your city: "),
            "customer.address.state": input("Enter your state: "),
            "customer.address.zipCode": input("Enter your zip code: "),
            "customer.phoneNumber": input("Enter your phone number: "),
            "customer.ssn": input("Enter your SSN: "),
            "customer.username": input("Enter your username: "),
            "customer.password": input("Enter your password: ")
        }

        # Fill in registration form
        for field_id, value in registration_data.items():
            if not wait_and_send_keys(driver, By.ID, field_id, value):
                raise Exception(f"Could not fill in {field_id}")
        
        # Fill in repeated password
        if not wait_and_send_keys(driver, By.ID, "repeatedPassword", registration_data["customer.password"]):
            raise Exception("Could not fill in repeated password")

        # Submit registration
        if not wait_and_click(driver, By.XPATH, "//input[@value='Register']"):
            raise Exception("Could not submit registration form")

        print("Registration completed successfully")
        time.sleep(5)  # Extended wait after registration

        # Create new account with enhanced error handling
        if not create_new_account(driver):
            raise Exception("Account creation failed")

        # Wait after account creation
        time.sleep(5)

        # Transfer funds with detailed logging
        print("\n--- Starting Transfer Funds Process ---")
        if not transfer_funds(driver):
            raise Exception("Transfer funds failed")

        # Logout
        try:
            print("\n--- Logging Out ---")
            logout_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Log Out"))
            )
            logout_button.click()
            print("Successfully logged out")
        except Exception as e:
            print(f"Error during logout: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")
        # Take screenshot on error
        try:
            driver.save_screenshot("error_screenshot.png")
            print("Error screenshot saved as 'error_screenshot.png'")
        except:
            print("Could not save error screenshot")

    finally:
        time.sleep(5)
        driver.quit()

# Run the main function
if __name__ == "__main__":
    main()