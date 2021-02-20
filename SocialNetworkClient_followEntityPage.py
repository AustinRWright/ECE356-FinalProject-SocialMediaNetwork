import mysql.connector

# A file for displaying all available topics/users to follow and which ones you are already following
# Create a class which will provide functions to display all available entities to follow and all of the entities which you are currently following
class followEntityPage():
    def __init__(self, mysqlConnector):
        self.mysqlConnector = mysqlConnector
    
    # Function to determine if a string represents an integer
    def RepresentsInt(self,s):
        try:
            value = int(s)
            return True
        except ValueError:
            return False

    # Display all of the possible topics to follow
    def displayAllTopics(self, userID):
        cursor = self.mysqlConnector.cursor(buffered=True, dictionary=True) # "Dictionary In Cursor" from https://stackoverflow.com/questions/10195139/how-to-retrieve-sql-result-column-value-using-column-name-in-python/56209874#56209874
        cursor.callproc("display_all_topics")
        allTopicsList = None
        for result in cursor.stored_results():
            allTopicsList = result.fetchall() # Store the results of the query in a list
        
        args=[userID]
        cursor.callproc("display_all_followed_topics",args)
        followedTopicsList = None
        for result in cursor.stored_results():
            followedTopicsList = result.fetchall()
        
        # Print the list of topics which can be followed, along with if the current user is following the topic already.
        print("\n---------- Welcome To The Topic List Page ----------\n\n")
        for topic in allTopicsList:
            if topic in followedTopicsList:
                print(" - " + topic[0] + "    Followers:" + str(topic[1]) + "    (Following)\n")
            else:
                print(" - " + topic[0] + "    Followers:" + str(topic[1]) + "\n")

    # Display all of the possible people to follow
    def displayAllPeople(self, userID):
        cursor = self.mysqlConnector.cursor(buffered=True, dictionary=True) # "Dictionary In Cursor" from https://stackoverflow.com/questions/10195139/how-to-retrieve-sql-result-column-value-using-column-name-in-python/56209874#56209874
        args = [userID]
        cursor.callproc("display_all_people", args)
        allPeopleList = None
        for result in cursor.stored_results():
            allPeopleList = result.fetchall() # Store the results of the query in a list
        
        args=[userID]
        cursor.callproc("display_all_followed_people",args)
        followedPeopleList = None
        for result in cursor.stored_results():
            followedPeopleList = result.fetchall()

        args = [userID]
        cursor.callproc("display_all_following_you", args)
        peopleFollowingYouList = None
        for result in cursor.stored_results():
            peopleFollowingYouList = result.fetchall()
            print(peopleFollowingYouList)
        
        # Print the list of topics which can be followed, along with if the current user is following the topic already.
        print("\n---------- Welcome To The People List Page ----------\n\n")
        for person in allPeopleList:
            personString = " - "
            if person[2] is None:
                personString = personString + person[1] + " (UserName: " + person[0] + ")    ID:" + str(person[3]) +  "    Followers:" + str(person[4])
            else:
                personString = personString + person[1] + " " + person[2] + " (UserName: " + person[0] + ")    ID:" + str(person[3]) + "    Followers:" + str(person[4])

            if person in followedPeopleList:
                personString = personString + "    (Following)"
            for followerID in peopleFollowingYouList:
                if followerID[0] == person[3]:
                    personString = personString + "    (They Follow You)"
            print(personString + "\n")

    # Follow a topic
    def followTopic(self, topicID, userID):
        try:
            cursor = self.mysqlConnector.cursor(buffered=True, dictionary=True) # "Dictionary In Cursor" from https://stackoverflow.com/questions/10195139/how-to-retrieve-sql-result-column-value-using-column-name-in-python/56209874#56209874
            args=[topicID, userID]
            cursor.callproc("follow_topic",args)
            self.mysqlConnector.commit()
            followedTopicsList = None
            for result in cursor.stored_results():
                followedTopicsList = result.fetchall()
            print("You are now following topic:" + topicID + "\n")
        except:
            self.mysqlConnector.rollback()
            print("The Topic Name [\"" + topicID + "\"] does not exist.\n")

    # Follow a user
    def followPerson(self, following_userID, followedBy_userID):
        try:
            cursor = self.mysqlConnector.cursor(buffered=True, dictionary=True) # "Dictionary In Cursor" from https://stackoverflow.com/questions/10195139/how-to-retrieve-sql-result-column-value-using-column-name-in-python/56209874#56209874
            args=[following_userID, followedBy_userID]
            cursor.callproc("follow_person",args)
            self.mysqlConnector.commit()
            followedPeopleList = None
            for result in cursor.stored_results():
                followedPeopleList = result.fetchall()
            print("You are now following user:" + str(following_userID) + "\n")
        except:
            self.mysqlConnector.rollback()
            print("FOLLOW PERSON ATTEMPT FAILED!")

    # Unfollow a topic
    def unfollowTopic(self, topicID, userID): # Could be implemented but due to lack of time it was skipped. To implement this I would copy the code to follow and modify it slightly so that it unfollows instead. The stored procedure is created.
        raise NotImplementedError

    # Unfollow a person
    def unfollowPerson(self, following_userID, followedBy_userID): # Could be implemented but due to lack of time it was skipped. To implement this I would copy the code to follow and modify it slightly so that it unfollows instead. The stored procedure is created.
        raise NotImplementedError