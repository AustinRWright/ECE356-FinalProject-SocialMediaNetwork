import mysql.connector
# NOTE: This file is to be used for displaying the login page to a user.

# Create a class which will run the login portion of the code and return the UserID of the user who has logged in.
class loginPage():
    def __init__(self, mysqlConnector):
        self.mysqlConnector = mysqlConnector
    
    # Function to determine if a string represents an integer
    def RepresentsInt(self,s):
        try:
            value = int(s)
            return True
        except ValueError:
            return False
    
    def run(self):
        # STEP 1: Output welcome message to the user:
        print("\n --------  WELCCOME  --------\n\n")
        # 2: Provide options to the user regarding what they can do from here and what they should input. (Continue looping until a valid option is entered, or there have been 10 failed attempts. If there have been 10 failed attemtps, exit the program!!!)
        variable = None
        loop_counter = 0
        while(loop_counter < 10):
            # Prompt the user for input
            variable = input("\nThe following options are available:\n    1. If you are an existing user, type \"Login\"\n    2. If you are a new user, type \"Create Account\"\n    3. If you wish to leave, type \"Exit\"\n\n    ")
            # 3. Implement a switch statement to determine which option was chosen
            if variable == "Exit":
                return -1
            elif variable == "Login":
                userID = self.login_user()
                return userID
            elif variable == "Create Account":
                is_newUserCreated = self.create_new_user()  # Prompt the user to create an account
                if is_newUserCreated == False:
                    return -1
                else:
                    userID = self.login_user()                # Bring the user to the login page so that they can attempt to login!
                    return userID
            else:
                loop_counter = loop_counter + 1
                print("\nThe option which you entered[\"" + variable + "\"] is invalid. You have " + str(10-loop_counter) + " remaining attempts.\n")

        # 4. If no valid options were entered, inform the user and then exit the program (AKA return -1)
        if (loop_counter == 10):
            print("\nNo valid options were entered after 10 attempts. Closing the application now.\n")
            return -1
    
    def login_user(self):       # Returns the UserID of the user who is logging in if a successful login was encountered, otherwise it returns -1 for the program to know to shutdown.
        # 1. Print a welcome message to inform the user that they are on the login page.
        for blank_line in range (50):   # Clear the screen
            print("\n")
        print("--------  WELCOME TO THE LOGIN PAGE --------\n\n")
        # 2. Provide the user with what options are available to them from this point. 
        variable = None
        loop_counter = 0
        while (loop_counter < 10):
            # Prompt the user for input
            variable = input("\nThe following options are available:\n    1. Enter a valid username\n    2. Enter nothing and the program will close\n\n")
            # 3. If the user wishes to exit, return -1
            if variable == '':
                return -1
                break
            # 4. If the user has entered a possible username, verify that the username is valid.
            else:
                # Execute a query here to determine if the username is a valid username.
                cursor = self.mysqlConnector.cursor(buffered=True, dictionary=True) # "Dictionary In Cursor" from https://stackoverflow.com/questions/10195139/how-to-retrieve-sql-result-column-value-using-column-name-in-python/56209874#56209874
                args = [variable]
                cursor.callproc("get_userID_from_handle",args)
                userID = []
                for result in cursor.stored_results():
                    userID = result.fetchall()

                if len(userID) == 0: # If there is no user with that name, notify the user and prompt them to attempt to login again.
                    loop_counter = loop_counter + 1
                    print("\nThe username you entered [\"" + str(variable) + "\"] does not correspond to any valid user. Please try again. You have " + str(10-loop_counter) + " remaining attempts.\n")
                # 5. If there is a user with that name, display a message "Welcome Back! Logging you in..." to the user and return their userID
                else: 
                    print("\n\n\nWelcome back user " + str(variable) + ". Logging you in now...\n\n\n")
                    return int(userID[0][0])
                    break
        # 6. If no valid options were entered, inform the user and then exit the program (AKA return -1)
        if (loop_counter == 10):
            print("\nNo valid usernames were entered after 10 attempts. Closing the application now.\n")
            return -1
    
    def create_new_user(self):      # Returns True if a new user was successfully created, returns false otherwise.
        # 1. Print a welcome message to inform the user that they are on the "Create New Account Page"
        for blank_line in range (50):   # Clear the screen
            print("\n")
        print("--------  WELCOME TO THE CREATE NEW ACCOUNT PAGE --------\n\n")       
        print("\n        Please note that all fields with an asterisk beside them are REQUIRED fields\n")
        # 2. Prompt the user for their first name
        var_firstName = ''
        while(True):
            var_firstName = input("\nPlease enter your first name between 1 and 30 characters.* (Note: if you are a company or entity which does not have a \"Last Name\", the last name field is not required)\n")
            if (len(var_firstName) == 0) or (len(var_firstName) > 30):
                print("\nYou have entered a value which has a length not between 1 and 30 characters, try again.\n")
            else:
                var_firstName = "'" + var_firstName + "'" 
                break
        
        # 3. Prompt the user for their last name (indicate that this is not a required field)
        var_lastName = ''
        while(True):
            var_lastName = input("\nPlease enter your last name between 1 and 30 characters. (Note: if you are a company or entity which does not have a \"Last Name\", the last name field is not required)\n")
            if (len(var_lastName) > 30):
                print("\nYou have entered a value which has a length not between 0 and 30 characters, try again.\n")
            else:
                if len(var_lastName) == 0:
                    var_lastName = "NULL" 
                else:
                    var_lastName = "'" + var_lastName + "'"
                break

        # 4. Prompt the user to create a username for themselves (AKA a handle) [Check that this handle is valid and not already in use before continuing]
        var_userName = ""
        while (True):
            var_userName = input("\nPlease enter a username between 1 and 100 characters long.* This will be how other users identify you: \n")
            cursor = self.mysqlConnector.cursor(buffered=True, dictionary=True) # "Dictionary In Cursor" from https://stackoverflow.com/questions/10195139/how-to-retrieve-sql-result-column-value-using-column-name-in-python/56209874#56209874
            args = [var_userName]
            cursor.callproc("get_userID_from_handle",args)
            userID = []
            for result in cursor.stored_results():
                userID = result.fetchall()
            
            # If the username entered is not within the specified bounds, notify the user of their error and to try again
            if (len(var_userName) < 4 or (len(var_userName) > 100)) and len(userID) == 0:
                print("\nYou have entered a value which has a length not between 4 and 100 characters, try again.\n")
            # If the username entered is already in use, notify the current user to please attempt again
            elif len(userID) != 0:
                print("\nThe username you have entered [\"" + var_userName + "\"] is already in use, please try another one.\n")
            # If the username is not currently in use and is valid, continue
            else: 
                break
        cursor.close()
        
        # 5. Prompt the user for the day of the month when they were born
        var_birthDay =""
        while(True):
            var_birthDay = input("\nPlease enter the numerical day of the month when you were born*: \n")
            if (self.RepresentsInt(var_birthDay) and (int(var_birthDay) <= 31 and int(var_birthDay) >= 1)):
                break
            else:
                print("\nThe day you have entered is invalid, please try again.")

        # 6. Prompt the user for the month of the year when they were born (January, March, April, May, June, July, August, September, October, November, or December)
        var_birthMonth =""
        while(True):
            var_birthMonth = input("\nPlease enter the month when you were born. (i.e., January, February, March, April, May, June, July, August, September, October, November, or December)*: \n")
            if var_birthMonth in ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]:
                break
            else:
                print("\nThe month you have entered is invalid, please try again.")

        # 7. Prompt the user for the year when they were born
        var_birthYear = ""
        while(True):
            var_birthYear = input("\nPlease enter the year when you were born. (Between 1900 and 2020)*: \n")
            if (self.RepresentsInt(var_birthYear) and (int(var_birthYear) > 1900 and int(var_birthYear) < 2020)):
                break
            else:
                print("\nThe year you have entered is invalid, please try again.")

        # 8. Prompt the user for their Gender (Either Male, Female, or Other)
        var_Gender = ""
        while(True):
            var_Gender = input("\nPlease enter your gender from one of Male, Female, or Other: \n")
            if len(var_Gender) == 0 or var_Gender in ["Male", "Female", "Other"]:
                if len(var_Gender) == 0:
                    var_Gender = None
                break
            else:
                print("\nThe gender you have entered is invalid, please try again.")
        
        # 9. Prompt the user to add a description of themselves (Verify that it is under 250 characters)
        var_Description = ""
        while(True):
            var_Description = input("\nPlease enter a description of yourself. (Limit 250 characters): \n")
            if len(var_Description) <= 250:
                if len(var_Description) == 0:
                    var_Description = "DEFAULT"
                else:
                    var_Description = "'" + var_Description + "'"
                break
            else:
                print("\nThe description you have entered is too long, please try again.")

        # 10. Execute the SQL command to create a new user in the PersonTable
        cursor = self.mysqlConnector.cursor(buffered=True, dictionary=True)
        try:
            args = [var_firstName, var_lastName, var_birthDay, var_birthMonth, var_birthYear, var_Gender, var_Description]
            cursor.callproc("create_new_user", args)
            self.mysqlConnector.commit()
        except:
            self.mysqlConnector.rollback()
            print("CREATING NEW USER FAILED")
        # 11. Execute the SQL command to get the value of the maximum userID from the PersonTable because this will be the value of the user's userID
        cursor.callproc("next_UserID")
        userID = []
        for result in cursor.stored_results():
            userID = result.fetchall()

        currentUserID = userID[0][0]

        try:
            args = [currentUserID, var_userName]
            cursor.callproc("create_new_userHandle", args)
            self.mysqlConnector.commit()
        except:
            self.mysqlConnector.rollback()
            print("CREATING NEW USER HANDLE ENTRY FAILED")
        cursor.close()
        return True


    