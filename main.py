import unittest

from pyee import cls
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestEdTechPlatform(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Initialise the browser driver once for the test suite."""
        print("Setting up the browser session...")
        # Automatically downloads and sets up the correct ChromeDriver version
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        cls.base_url = "https://guvi.in"
        cls.wait = WebDriverWait(cls.driver, 10)

    def test_01_url_validation(self):
        """Test Case 1: Verify whether the URL is valid or not."""
        print("\nExecuting Test Case 1: URL Validation")
        self.driver.get(self.base_url)

        # Verify the current URL matches or contains the expected base URL
        current_url = self.driver.current_url
        self.assertIn("guvi.in", current_url, f"Failed to load the web application. Current URL: {current_url}")
        print("PASS: Web application loaded successfully.")

    def test_02_page_title_validation(self):
        """Test Case 2: Verify whether the title of the webpage is correct."""
        print("\nExecuting Test Case 2: Page Title Validation")
        self.driver.get(self.base_url)

        expected_title = "GUVI | Learn to code in your native language"
        actual_title = self.driver.title

        self.assertEqual(actual_title, expected_title, f"Title mismatch! Found: '{actual_title}'")
        print(f"PASS: Title matches exactly -> '{actual_title}'")

    def test_03_login_button_visibility_and_clickability(self):
        """Test Case 3: Verify visibility and clickability of the Login button."""
        print("\nExecuting Test Case 3: Login Button Validation")
        self.driver.get(self.base_url)

        # Adjust selector according to the real webpage structure (e.g., LINK_TEXT, XPATH, or ID)
        login_button = self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Login")))
        self.assertTrue(login_button.is_displayed(), "Login button is not visible.")

        clickable_button = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login")))
        clickable_button.click()

        # Validate navigation to the login page
        self.wait.until(EC.url_contains("sign-in") or EC.url_contains("login"))
        self.assertIn("login", self.driver.current_url.lower(), "Did not navigate to the login page.")
        print("PASS: Login button is visible, clickable, and navigates successfully.")

    def test_04_signup_button_visibility_and_clickability(self):
        """Test Case 4: Verify visibility and clickability of the Sign-Up button."""
        print("\nExecuting Test Case 4: Sign-Up Button Validation")
        self.driver.get(self.base_url)

        signup_button = self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Sign up")))
        self.assertTrue(signup_button.is_displayed(), "Sign-Up button is not visible.")

        clickable_button = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign up")))
        clickable_button.click()

        # Expected redirect URL verification
        expected_register_url = "https://guvi.in/register/"
        self.wait.until(EC.url_to_be(expected_register_url))
        self.assertEqual(self.driver.current_url, expected_register_url, "Redirect URL mismatch for Sign-Up.")
        print("PASS: Sign-Up button is visible, clickable, and redirects correctly.")

    def test_05_navigation_to_signin_via_signup(self):
        """Test Case 5: Verify navigation to the Sign-In page via the Sign-Up button."""
        print("\nExecuting Test Case 5: Navigation via Sign-Up Button")
        self.driver.get(self.base_url)

        signup_button = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign up")))
        signup_button.click()

        expected_url = "https://guvi.in/register/"
        self.wait.until(EC.url_to_be(expected_url))
        self.assertEqual(self.driver.current_url, expected_url, "Failed to load registration page properly.")
        print("PASS: Redirected URL loaded properly.")

    def test_06_login_with_valid_credentials(self):
        """Test Case 6: Verify login functionality with valid credentials."""
        print("\nExecuting Test Case 6: Valid Login Functionality")
        # Direct navigation to the login page route
        self.driver.get(f"{self.base_url}/sign-in/")

        try:
            # Locate input boxes and log in
            email_field = self.wait.until(EC.presence_of_element_located((By.ID, "login_email")))
            password_field = self.driver.find_element(By.ID, "login_password")
            login_submit = self.driver.find_element(By.ID, "login_button")

            email_field.send_keys("valid_user@example.com")  # Replace with valid test data
            password_field.send_keys("ValidPassword123")  # Replace with valid test data
            login_submit.click()

            # Verify redirection to profile/dashboard page
            self.wait.until(EC.url_contains("dashboard"))
            self.assertIn("dashboard", self.driver.current_url, "User was not redirected to the dashboard.")
            print("PASS: User logged in and redirected to profile/dashboard successfully.")
        except Exception as e:
            self.fail(f"Test case failed due to exception: {str(e)}")

    def test_07_login_with_invalid_credentials(self):
        """Test Case 7: Verify login with invalid credentials."""
        print("\nExecuting Test Case 7: Invalid Login Functionality")
        self.driver.get(f"{self.base_url}/sign-in/")

        try:
            email_field = self.wait.until(EC.presence_of_element_located((By.ID, "login_email")))
            password_field = self.driver.find_element(By.ID, "login_password")
            login_submit = self.driver.find_element(By.ID, "login_button")

            email_field.send_keys("invalid_user@example.com")
            password_field.send_keys("WrongPassword!")
            login_submit.click()

            # Validate that login fails (URL should still be login/sign-in page)
            self.assertIn("sign-in", self.driver.current_url)

            # Validate presence of error message alert element
            error_message = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "error-toast")))
            self.assertTrue(error_message.is_displayed(), "Error message was not displayed.")
            print(f"PASS: Login failed dynamically. Error message caught: '{error_message.text}'")
        except Exception as e:
            self.fail(f"Test case failed due to exception: {str(e)}")

    def test_08_homepage_menu_items_visibility(self):
        """Test Case 8: Verify that menu items like "Courses", "LIVE Classes", and "Practice" are displayed."""
        print("\nExecuting Test Case 8: Menu Items Visibility")
        self.driver.get(self.base_url)

        menu_items = ["Courses", "LIVE Classes", "Practice"]

        for item in menu_items:
            # Validates that elements containing the exact menu text are visible on the navigation layout
            element = self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//*[contains(text(), '{item}')]")))
            self.assertTrue(element.is_displayed(), f"Menu item '{item}' is missing or not visible.")
            print(f"Verified: Menu item '{item}' is visible and accessible.")

        print("PASS: All key menu elements are perfectly accessible.")

    def test_09_dobby_assistant_widget_presence(self):
        """Test Case 9: Validate that the Dobby Guvi Assistant is present on the page."""
        print("\nExecuting Test Case 9: Dobby Assistant Presence")
        self.driver.get(self.base_url)

        # Update the selector identifier (ID/Class) depending on the live widget implementation layout
        try:
            dobby_widget = self.wait.until(EC.presence_of_element_located((By.ID, "dobby-assistant-widget")))
            self.assertTrue(dobby_widget.is_displayed(), "Dobby Assistant widget is present in DOM but hidden.")
            print("PASS: Dobby Guvi Assistant widget is clearly visible on the page interface.")
        except Exception:
            self.fail("FAIL: Dobby Guvi Assistant chatbot widget could not be located.")

    def test_10_logout_functionality(self):
        """Test Case 10: Validate logout functionality."""
        print("\nExecuting Test Case 10: Logout Functionality")

        # Step A: Perform valid login sequence context setup
        self.test_06_login_with_valid_credentials()

        try:
            # Step B: Locate user profile settings or direct logout action button
            logout_button = self.wait.until(EC.element_to_be_clickable((By.ID, "logout-btn")))
            logout_button.click()

            # Step C: Expect redirect back to landing base page or login portal form area
            self.wait.until(EC.url_to_be(self.base_url) or EC.url_contains("sign-in"))
            print("PASS: User logged out successfully and redirected back to landing views.")
        except Exception as e:
            self.fail(f"Test case failed during logging out procedure: {str(e)}")

    @classmethod
    def tearDownClass(cls):
        """Safely destroy and close the browser instance window contexts."""
        print("\nTerminating test execution environment...")
        if cls.driver:
            cls.driver.quit()
            print("Browser closed cleanly. Test process completed.")
            from dis import name
            if name == "main":
                unittest.main()