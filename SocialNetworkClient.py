import mysql.connector
import SocialNetworkClient_loginPage
import SocialNetworkClient_dashboardPage
import SocialNetworkClient_followEntityPage
import SocialNetworkClient_postPage
import sys
# NOTE: Had to execute "python3 -m pip install mysql-connector-python" for this to work. (It downloaded the python3 mysql.connector library that I needed!)

mydb = mysql.connector.connect(
  host="192.168.56.103",
  user="monty",
  passwd="Mmmapples1.",
  database='SocialNetworkDB',
  auth_plugin='mysql_native_password'
)
cursor = mydb.cursor( buffered = True, dictionary=True) # "Dicitionary In Cursor" from https://stackoverflow.com/questions/10195139/how-to-retrieve-sql-result-column-value-using-column-name-in-python/56209874#56209874

firstPostID = None
lastPostID = None

def resetDashboard():
    dashboardPage = SocialNetworkClient_dashboardPage.dashboardPage(mydb)
    return dashboardPage.displayNextFivePosts(None, userID)

# 1. Create/Initialize a login page object with the database connector object
loginPage = SocialNetworkClient_loginPage.loginPage(mydb)
# 2. Execute the run function on the LoginPage
userID = loginPage.run()

# If the login page returns that it should exit, then exit the program with -1
if int(userID) == -1:
    sys.exit("Ending Program")

# 3. Create/Initialize a dashboard page object with the database connector object
dashboardPage = SocialNetworkClient_dashboardPage.dashboardPage(mydb)

# 4. Navigate the user to the dashboard page and display the first 5 posts.
firstAndLastPostID = resetDashboard()
firstPostID = firstAndLastPostID[0]
lastPostID = firstAndLastPostID[1]

postPage = SocialNetworkClient_postPage.postPage(mydb)
followEntityPage = SocialNetworkClient_followEntityPage.followEntityPage(mydb)
# 5. This is the main loop where all functions will be run once a user is logged in.
while(True):
    # A. Notify the user of their options from here.
    decision = input("\n------------ WELCOME TO THE DASHBOARD PAGE ----------\nTo navigate through the dashboard page, consult the controls below:\n1. To display the next five posts type \"Next\"\n2. To follow a new person type \"Follow Person\"\n3. To follow a new topic type \"Follow Topic\"\n4. To create a new post type \"Create Post\"\n5. To like a post on the screen type \"Like Post\"\n6. To repost a post type \"Repost\"\n7. To reply to a post type \"Reply\"\n8. To go to the most recent post type \"Refresh\"\n9. To exit type \"Exit\"\nPlease enter your command here: ")
    
    if decision == "Next":
        firstAndLastPostID = dashboardPage.displayNextFivePosts(lastPostID, userID)
        firstPostID = firstAndLastPostID[0]
        lastPostID = firstAndLastPostID[1]

    elif decision == "Follow Person":
        followEntityPage.displayAllPeople(userID)
        while(True):
            value = input("\nIf you would like to follow any of these people, type in their UserID. Otherwise, type \"Exit\":\n")
            if value != "Exit":
                args = [value]
                cursor.callproc("get_handle_from_userID", args)
                userIDEntryList = None
                for result in cursor.stored_results():
                    userIDEntryList = result.fetchall() # Store the results of the query in a list
                if userIDEntryList is not None:
                    followEntityPage.followPerson(value, userID)
                else:
                    print("Invalid entry, please try again.")
            else:
                break
        firstAndLastPostID = resetDashboard()
        firstPostID = firstAndLastPostID[0]
        lastPostID = firstAndLastPostID[1]

    elif decision == "Follow Topic":
        followEntityPage.displayAllTopics(userID)
        while(True):
            value = input("\nIf you would like to follow any of these topics, type in the name of the topic. Otherwise, type \"Exit\":\n")
            if value != "Exit":
                args = [value]
                cursor.callproc("get_TopicID_entry", args)
                topicIDEntryList = None
                for result in cursor.stored_results():
                    topicIDEntryList = result.fetchall() # Store the results of the query in a list
                if topicIDEntryList is not None:
                    followEntityPage.followTopic(value, userID)
                else:
                    print("Invalid entry, please try again.")
            else:
                break
        firstAndLastPostID = resetDashboard()
        firstPostID = firstAndLastPostID[0]
        lastPostID = firstAndLastPostID[1]

    elif decision == "Create Post":
        postPage.createNewPost(userID, None)
        resetDashboard()

    elif decision == "Like Post":
        while(True):
            value = input("Enter the PostID of the post which you like, if you want to back out, type \"Exit\": ")
            if value != "Exit":
                args = [value]
                cursor.callproc("get_post_contents", args)
                postContentsList = None
                for result in cursor.stored_results():
                    postContentsList = result.fetchall() # Store the results of the query in a list
                if len(postContentsList) != 0:
                    if postContentsList[0] is not None:
                        postPage.likePost(userID, value)
                else:
                    print("Invalid entry, please try again.")
            else:
                break
        firstAndLastPostID = resetDashboard()
        firstPostID = firstAndLastPostID[0]
        lastPostID = firstAndLastPostID[1]

    elif decision == "Repost":
        while(True):
            value = input("Enter the PostID of the post you would like to repost, if you want to back out, type \"Exit\": ")
            if value != "Exit":
                args = [value]
                cursor.callproc("get_post_contents", args)
                postContentsList = None
                for result in cursor.stored_results():
                    postContentsList = result.fetchall() # Store the results of the query in a list
                if len(postContentsList) != 0:
                    if postContentsList[0] is not None:
                        postPage.createRepost(userID, value)
                else:
                    print("Invalid entry, please try again.")
            else:
                break
        firstAndLastPostID = resetDashboard()
        firstPostID = firstAndLastPostID[0]
        lastPostID = firstAndLastPostID[1]

    elif decision == "Reply":
        while(True):
            value = input("Enter the PostID of the post you would like to reply to, if you want to back out, type \"Exit\": ")
            if value != "Exit":
                args = [value]
                cursor.callproc("get_post_contents", args)
                postContentsList = None
                for result in cursor.stored_results():
                    postContentsList = result.fetchall() # Store the results of the query in a list
                if len(postContentsList) != 0:
                    if postContentsList[0] is not None:
                        postPage.createNewPost(userID, value)
                else:
                    print("Invalid entry, please try again.")
            else:
                break
        firstAndLastPostID = resetDashboard()
        firstPostID = firstAndLastPostID[0]
        lastPostID = firstAndLastPostID[1]

    elif decision == "Refresh":
        firstAndLastPostID = resetDashboard()
        firstPostID = firstAndLastPostID[0]
        lastPostID = firstAndLastPostID[1]

    elif decision == "Exit":
        cursor.close()
        mydb.close()
        sys.exit("Exiting the Program")
        break

    else:
        print("\nNo valid entry was input, please try again\n")

# If I ever get outside of the program, end it.
mydb.close()
sys.exit("Exiting the Program")
