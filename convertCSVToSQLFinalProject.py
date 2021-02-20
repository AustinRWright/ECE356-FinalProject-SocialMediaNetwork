import csv
from datetime import datetime
# ENSURE THAT THE TABLES ARE CREATED BEFORE THE SCRIPT IS RUN, OR ALTERNATIVELY, CREATE THE TABLES IN THIS SCRIPT!!!

# Default information for a new user account:
#UserID, First_Name, Last_Name, CreationDate, BirthDay, BirthMonth, BirthYear, Gender, Description, NumberOfFollowers
now = datetime.now() # current date and time
default_CreationDate = now.strftime("%Y-%m-%d %H:%M:%S") # FROM https://www.programiz.com/python-programming/datetime/strftime
default_Birthday = 4
default_BirthMonth = "July"
default_BirthYear = 2000
default_Gender = "Other"
default_Description = "This is a default description of myself. #Yay #Awesome."
default_NumberOfFollowers = 0
default_FirstName = "John"
default_LastName = "'Smith'"

def extractSubstringFromEntities(substringIdentifier, startSearchIndex, stringToSearch): 
    val = -1
    for n in range(0, startSearchIndex+1): 
        val = entities.find(substringIdentifier, val + 1) 
    first_substring = stringToSearch[val + len(substringIdentifier):len(stringToSearch)]
    endIndex = first_substring.find("'")
    returnString = first_substring[0:endIndex]
    return returnString

# STEP 1: CREATE FILE TO WRITE TO! - Done!
sql_file = open("SocialNetworkDB.sql", "w+", encoding="utf-8")

# STEP 2: WRITE THE SETUP SQL COMMANDS TO THE FILE. - Should be done!
sql_file.write("DROP DATABASE IF EXISTS `SocialNetworkDB`;\n")
sql_file.write("CREATE DATABASE  IF NOT EXISTS `SocialNetworkDB` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;\n") # Sets the DB up to be able to accept Emojis, etc
sql_file.write("USE `SocialNetworkDB`;\n")
sql_file.write("\nSET NAMES utf8mb4;\n")
sql_file.write("\nSET FOREIGN_KEY_CHECKS=0;\n") # Turn off foreign key checks until after all of the tables are created

# STEP 3: CREATE THE TABLES WHICH THE DATA WILL BE INSERTED INTO. - Should be done!
# A) Person Table
sql_file.write("\nCREATE TABLE PersonTable(\n    UserID    BIGINT NOT NULL UNIQUE AUTO_INCREMENT,\n    First_Name    VARCHAR(30) NOT NULL,\n    Last_Name    VARCHAR(30),\n    CreationDate    DATETIME DEFAULT CURRENT_TIMESTAMP,\n    BirthDay    INT,\n    BirthMonth    ENUM('January','February','March','April','May','June','July','August','September','October','November','December'),\n    BirthYear    INT,\n    Gender    ENUM('Male', 'Female', 'Other') DEFAULT 'Other',\n    Description    VARCHAR(250) DEFAULT NULL,\n    NumberOfFollowers    BIGINT DEFAULT 0,\n    PRIMARY KEY (UserID)\n) AUTO_INCREMENT = 1 ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci;\n")
# B) Post Table
sql_file.write("\nCREATE TABLE PostTable(\n    PostID    BIGINT NOT NULL UNIQUE AUTO_INCREMENT,\n    Text    VARCHAR(250) DEFAULT NULL,\n    Date    DATETIME DEFAULT CURRENT_TIMESTAMP,\n    UserID    BIGINT NOT NULL,\n    is_retweet    BOOL DEFAULT FALSE,\n    is_reply    BOOL DEFAULT FALSE,\n    Original_PostID    BIGINT DEFAULT NULL,\n    Original_Post_UserID    BIGINT DEFAULT NULL,\n    NumberOfLikes    BIGINT DEFAULT 0,\n    NumberOfReposts    BIGINT DEFAULT 0,\n    PRIMARY KEY (PostID),\n    FOREIGN KEY (UserID) REFERENCES PersonTable(UserID),\n    FOREIGN KEY (Original_PostID) REFERENCES PostTable(PostID),\n    FOREIGN KEY (Original_Post_UserID) REFERENCES PersonTable(UserID)\n) AUTO_INCREMENT = 1 ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci;\n")
# C) Topic Table
sql_file.write("\nCREATE TABLE TopicTable(\n    TopicID    VARCHAR(100) BINARY NOT NULL UNIQUE,\n    NumberOfFollowers    BIGINT NOT NULL,\n    CHECK(NumberOfFollowers >= 0),\n    PRIMARY KEY (TopicID)\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci;\n")
# D) Person Handle Table
sql_file.write("\nCREATE TABLE PersonHandleTable(\n    UserID    BIGINT NOT NULL UNIQUE,\n    Handle    VARCHAR(100) NOT NULL UNIQUE,\n    PRIMARY KEY(UserID),\n    FOREIGN KEY (UserID) REFERENCES PersonTable(UserID)\n);\n")
# E) Follows Person Table
sql_file.write("\nCREATE TABLE FollowsPersonTable(\n    Following_UserID    BIGINT NOT NULL,\n    FollowedBy_UserID    BIGINT NOT NULL,\n    CHECK(Following_UserID != FollowedBy_UserID),\n    PRIMARY KEY (Following_UserID, FollowedBy_UserID),\n    FOREIGN KEY (Following_UserID) REFERENCES PersonTable(UserID),\n    FOREIGN KEY (FollowedBy_UserID) REFERENCES PersonTable(UserID)\n);\n")
# F) Post Images Table
sql_file.write("\nCREATE TABLE PostMediaTable(\n    PostID    BIGINT NOT NULL,\n    Media_Number    INT NOT NULL,\n    Media_URL    VARCHAR(250) NOT NULL,\n    CHECK(Media_Number > 0),\n    PRIMARY KEY (PostID, Media_Number),\n    FOREIGN KEY (PostID) REFERENCES PostTable(PostID)\n);\n") # SHOULD FILENAME EVEN EXIST? SHOULD IT BE NULL?
# G) Post Links Table
sql_file.write("\nCREATE TABLE PostLinksTable(\n    PostID    BIGINT NOT NULL,\n    Link_Number    INT NOT NULL,\n    Link_URL    VARCHAR(250) NOT NULL,\n    CHECK(Link_Number > 0),\n    PRIMARY KEY (PostID, Link_Number),\n    FOREIGN KEY (PostID) REFERENCES PostTable(PostID)\n);\n")
# H) Post People Tagged Table
sql_file.write("\nCREATE TABLE PostPeopleTaggedTable(\n    PostID    BIGINT NOT NULL,\n    Tag_Number    INT NOT NULL,\n    UserID    BIGINT NOT NULL,\n    CHECK(Tag_Number > 0),\n    PRIMARY KEY (PostID, Tag_Number),\n    FOREIGN KEY (PostID) REFERENCES PostTable(PostID)\n);\n")
# I) Post Topics Table
sql_file.write("\nCREATE TABLE PostTopicsTable(\n    PostID    BIGINT NOT NULL,\n    Topic_Number    INT NOT NULL,\n    TopicID    VARCHAR(100) BINARY NOT NULL,\n    CHECK(Topic_Number > 0),\n    PRIMARY KEY (PostID, Topic_Number),\n    FOREIGN KEY (PostID) REFERENCES PostTable(PostID),\n    FOREIGN KEY (TopicID) REFERENCES TopicTable(TopicID)\n);\n")
# J) Likes Post Table
sql_file.write("\nCREATE TABLE LikesPostTable(\n    PostID    BIGINT NOT NULL,\n    UserID    BIGINT NOT NULL,\n    PRIMARY KEY (PostID, UserID),\n    FOREIGN KEY (PostID) REFERENCES PostTable(PostID),\n    FOREIGN KEY (UserID) REFERENCES PersonTable(UserID)\n);\n")
# K) Read Post Table
sql_file.write("\nCREATE TABLE ReadPostTable(\n    PostID    BIGINT NOT NULL,\n    UserID    BIGINT NOT NULL,\n    PRIMARY KEY (PostID, UserID),\n    FOREIGN KEY (PostID) REFERENCES PostTable(PostID),\n    FOREIGN KEY (UserID) REFERENCES PersonTable(UserID)\n);\n")
# L) Follows Topic Table
sql_file.write("\nCREATE TABLE FollowsTopicTable(\n    TopicID    VARCHAR(100) BINARY NOT NULL,\n    UserID    BIGINT NOT NULL,\n    PRIMARY KEY (TopicID, UserID),\n    FOREIGN KEY (TopicID) REFERENCES TopicTable(TopicID),\n    FOREIGN KEY (UserID) REFERENCES PersonTable(UserID)\n);\n")

# Add additional indices to the tables as needed:
sql_file.write("\nALTER TABLE `PostTable` ADD INDEX `Date`(`Date`);\n")
sql_file.write("\nALTER TABLE `PostTopicsTable` ADD INDEX `TopicID`(`TopicID`);\n")
sql_file.write("\nALTER TABLE `PostPeopleTaggedTable` ADD INDEX `UserID`(`UserID`);\n")



# STEP 4: CREATE THE LISTS WHICH WILL BE USED TO STORE THE TUPLES OF DATA PARSED FROM THE SQL FILE IN STEP 5
UserList = []   # NOTE: This list will be used to keep track of the known users which have already been added to the database!
TopicList = []  # NOTE: This list will be used to keep track of the known topics which have already been added to the database!
PostList = []   # NOTE: This list will be used to keep track of the known topics which have already been added to the database!
PersonTableList = [] # UserID, First_Name, Last_Name, CreationDate, BirthDay, BirthMonth, BirthYear, Gender, Description, NumberOfFollowers
PersonHandleList = [] # UserID, Handle
FollowsPersonTableList = [] # Following_UserID, FollowedBy_UserID
PostTableList = [] # PostID, Text, Date, UserID, is_retweet, is_reply, Original_PostID, Original_Post_UserID, NumberOfLikes, NumberOfReposts
PostMediaTableList = [] # PostID, Media_Number, Media_URL
PostLinksTableList = [] # PostID, Link_Number, Link_URL
PostPeopleTaggedTableList = [] # PostID, TagIndex, UserID
PostTopicsTableList = [] # PostID, TopicIndex, TopicID
TopicTableList = [] # TopicID, NumberOfFollowers
FollowsTopicTableList = [] # TopicID, UserID
LikesPostTableList = [] # PostID, UserID
ReadPostTableList = [] # PostID, UserID

RepliedToUserHandle = [] # List used to keep track of the user handles which have been replied to in a post but their names are unknown

# NOTE: This is a placeholder value for the userID's! ---------------- This is a placeholder for the value which will be updated at the end of the script! The Auto Increment value will be updated at the end of the script so that all new users being added to the database from the CLI client will have unique userID's.
userID = 3 # Because 1 and 2 are taken by Trump and Clinton respectively
# NOTE: The auto increment value of the postID will be updated at the end of this script so that the postID's of all new posts will be greater than the greatest postID value from the data set used!
maxPostID = 1
retweeted_postID = 10000 # Start from here because there are only just over 5000 tweets in the dataset that I am using, so this makes my life a little easier because there won't be any overlap between the two. I doubt that I will manually generate over 5000 posts during my testing of the database... lol
# STEP 5:
# READ IN THE SQL FILE LINE BY LINE AND PARSE THE DATA AS NECESSARY!!
# EASIEST WAY TO DO THIS IS TO PARSE THE FILE LINE BY LINE AND PARSE THE DATA INTO THE APPROPRIATE LISTS WHICH WILL THEN BE USED TO CREATE THE INSERT STATEMENTS AND TABLES LATER ON
with open('clinton-trump-tweets/tweets.csv', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0 # Skip the first row as it contains the column descriptors.
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            line_count+=1
            # DO SOMETHING HERE TO EXTRACT THE DATA TO THE PROPER LOCATIONS!!!
            # Extract data from each line and populate data in the tables as necessary
            # WHAT WILL HAPPEN HERE IS CREATING THE INSERT STATEMENTS FOR EACH TABLE!
            # A) Extract each of the values from the row into their appropriate variables:
            postID = row[0]
            userHandle = row[1]
            postText = row[2]
            is_retweet = row[3]
            original_author = row[4]
            post_datetime = row[5]
            responding_to_Handle = row[6]
            responding_to_StatusID = row[7]
            responding_to_UserID = row[8]
            is_quote_status = row[9] # I think this means "Is this their tweet? or are they retweeting someone else?"
            language = row[10]
            retweet_count = row[11]
            favourite_count = row[12]
            entities = row[26]  # This is where all of the information about who is being tagged, what Links are in the post, and what photos/videos (AKA media) are being posted with the tweet (NOTE: The media URLs here are only links to the twitter page where they were posted, not the original source URL!)!!
            extended_entities = row[27] # This is where the non-twitter URLS of the media (Photos and Videos) are located!

            # HANDLE CHANGING TEXT OF TRUE AND FALSE TO BE THE APPROPRIATE MYSQL VALUES OF 1 OR 0 RESPECTIVELY
            # NOTE: I cannot get the original PostID from the datasets... So... I will just have to make up numbers for this! I guess that I should start at 10,000 and go from there!
            current_retweeted_postID = None
            is_retweet_int = 0 # AKA by default it is not a retweet of another person's post!
            if len(original_author) > 0:
                is_retweet_int = 1
                retweeted_postID += 1
                current_retweeted_postID = retweeted_postID
            is_reply_int = 0 # AKA by default it is not a reply to another person
            if len(responding_to_Handle) > 0:
                is_reply_int = 1

                #current_retweeted_postID = responding_to_StatusID Should not do this because we don't know the info of the original post, so why would I add the ID of that post to the table if it does not exist as a FK in the PostTable? Unless I want to parse things out and add that post? But I would rather not as that makes things much more complicated....
            # NOTE: I will need to add a function which adds the first and last name of both Donald J. Trump and Hillary Clinton because the only way to get the information about their names is if they were tagged in another user's tweet. Not the best way to do things but I'll deal with what I have!
            # NOTE: ROW 17 of the dataset includes a photo in the post, this would be how to see the photo and add it to the PostImagesTable! The PostImages and PostLinks tables were modified as appropriate to accomodate this. Note that images and links both have the displayed link and then the actual link which is signinficantly longer!
            # In the Entities portion of the dataset, this is where all hashtags, URLs, and photos included with the post are listed! This will make it significantly easier to extract the relevant data from the post rather than trying to find all of the data in the text portion.

            # HOW TO EXTRACT URL FROM A STRING: print(re.search("(?P<url>https?://[^\s]+)", myString).group("url"))   This came from https://stackoverflow.com/questions/839994/extracting-a-url-in-python
            
            # B) Create Person objects and Person handle objects if they are not yet created!
            tempUserID = 0
            # IF the person tweeting out is not a known user, or the User list is empty, then create a Person Tuple for them in the PersonTableList and then add them to the UserList
            if len(UserList) == 0 or userHandle not in UserList: # Posts in this db are only made by trump and clinton
                if "realDonaldTrump" in userHandle:
                    PersonTableList.append((1, "Donald J.", "'Trump'", "DEFAULT", 14, "June", 1946,"Male", "I AM THE BEST PRESIDENT EVER! #MAGA #POTUS #FAKENEWS #LOSERMEDIA", "DEFAULT"))
                    UserList.append(userHandle)
                    PersonHandleList.append((1, userHandle))
                    
                elif "HillaryClinton" in userHandle:
                    PersonTableList.append((2, "Hillary", "'Clinton'", "DEFAULT", 26, "October", 1947,"Female", "I WOULD HAVE BEEN THE BEST PRESIDENT EVER! #LoveTrumpsHate", "DEFAULT"))
                    UserList.append(userHandle)
                    PersonHandleList.append((2, userHandle))
                    
            # C) Create the Post Object now that we know the user is a user in our databasetempUserID = 0
            if "realDonaldTrump" in userHandle:
                tempUserID = 1
            elif "HillaryClinton" in userHandle:
                tempUserID = 2
            else:   # IN THIS DATABASE, WE ONLY HAVE 2 USERS ACTUALLY POSTING THINGS!
                print("\nERROR: UNKNOWN HANDLE: " + userHandle + " On line: " + str(line_count) + "\n")

            # D) Replace all instances of an apostrophe or quotation with a backslash infront of them to ensure that the SQL code will be valid!
            postText = postText.replace("'", "\\'")
            post_datetime = post_datetime.replace("T"," ")
            post_datetime = "'" + post_datetime + "'"

            # If the current PostID is greater than the current maximum post ID value, update the maximum postID value to be the current postID + 1. ------ Used for setting the Auto_Increment value of the PostTable at the end of this script! ------
            if int(postID) >= maxPostID:
                print("\n Current postID is: " + postID + "    The current Max post ID is: " + str(maxPostID) + "\n")
                maxPostID = int(postID) + 1 # Ensures that all postIDs are less than the maximum postID

            # ---------------- IF the current post is replying or retweeting a post which has already has been posted, I need to create a post entry for that post so that the current post doesn't come back with errors because the post it is referencing does not actually exist.
            # In the case of where the current post is a response to an original post, I can use mostly default values because we don't actually have information about those posts, all we know is that the user is responding to them!
            # QUESTION: How to handle users? All we have for response posts is that they have a userID.
            # ANSWER: Keep a list of all of the user handles which have been replied to, as I create user objects, check if the user object's handle matches a handle in this list. If they do match, remove the user handle from this list. At the end of the script, if there are still users here without user objects, create default user objects for them so that the post is valid!!!!
            default_PostText = "Oh what a lovely day to post on my favourite social media platform!"
            default_PostDateTime = "DEFAULT"
            default_is_retweet = "DEFAULT"
            default_is_reply = "DEFAULT"
            default_Retweeted_postID = "DEFAULT"
            default_originalAuthor = "DEFAULT"
            default_favouriteCount = 0
            default_retweetCount = 0
            original_postersUserID = 0
            if is_reply_int == 1:
                postersUserID = 0
                if responding_to_Handle not in UserList: # If the person doesn't exist
                    # CREATE A NEW USER ENTRY HERE!!!
                    PersonTableList.append((userID, default_FirstName, default_LastName, "DEFAULT", default_Birthday, default_BirthMonth, default_BirthYear,default_Gender, default_Description, "DEFAULT"))
                    PersonHandleList.append((userID, responding_to_Handle))
                    UserList.append(responding_to_Handle)
                    postersUserID = userID
                    userID += 1
                else:
                    # Search for the poster's userID!
                    for posterHandle in PersonHandleList:
                        if posterHandle[1] == responding_to_Handle:
                            postersUserID = posterHandle[0]
                            break

                if responding_to_StatusID == '':
                    print("\n ----- EMPTY POST ID BUT IS A RESPONSE: " + responding_to_Handle + "\n")

                # Create a post entry for this original post with default data!
                PostTableList.append((responding_to_StatusID, default_PostText, default_PostDateTime, postersUserID, 0, 0, "DEFAULT", "DEFAULT", 0, 0))
                PostList.append(float(responding_to_StatusID))
            elif is_retweet_int == 1:
                postersUserID = 0
                if original_author in UserList: # If the person already exists, get their userID
                    for posterHandle in PersonHandleList:
                        if posterHandle[1] == original_author:
                            postersUserID = posterHandle[0]
                            original_postersUserID = posterHandle[0]
                            break
                else:   # If the poster does NOT EXIST YET
                    postersUserID =  userID # The next user to be created will be this user, so I can set the postersUserID equal to the next user to be created userID (I KNOW THIS BECAUSE I LOOKED AT HOW MENTIONS ARE STRUCTURED AND THE ORDER IN WHICH THEY APPEAR, THE ORIGINAL POSTER'S NAME AND HANDLE ALWAYS APPEAR FIRST!!!)

                # Create a post entry for this original post with default data!
                PostTableList.append((current_retweeted_postID, postText, default_PostDateTime, postersUserID, 0, 0, "DEFAULT", "DEFAULT", 0, 1)) 
                PostList.append(float(current_retweeted_postID))


                # NOTE: For the case of retweets, I need to do some more work below, every mention and every link, media etc which is included in the current post must also be included in the original post which was retweeted!!!! Also, need to make sure that the user's name is properly parsed!!! ( I can do this because the user's name will be included in the User_Mentions portion of the entity column!!!!)
                # NOTE: -------- I THINK THIS PART IS DONE!!!! --------



            if len(original_author) == 0:
                original_postersUserID = "DEFAULT"
            elif original_author in UserList:
                for current_user in PersonHandleList:
                    if current_user[1] == original_author:
                        original_postersUserID = current_user[0]
                        break
            else:
                original_postersUserID = userID # The next user to be created will be this user, so I can set the postersUserID equal to the next user to be created userID (I KNOW THIS BECAUSE I LOOKED AT HOW MENTIONS ARE STRUCTURED AND THE ORDER IN WHICH THEY APPEAR, THE ORIGINAL POSTER'S NAME AND HANDLE ALWAYS APPEAR FIRST!!!)

            if current_retweeted_postID == None:
                current_retweeted_postID = "DEFAULT"

            # NOTE: ------ Now I need to check for if someone (such as Hillary Clinton) is replying to their previous post (The current post would be the post which has been responded to).
            #------ In this case, there will already be an entry for this post in the PostTable list, I need to check if it exists, if it does exist, remove the default entry from the postTableList and replace it with this entry.
            if float(postID) in PostList:
                entryToSearchFor = None
                # Search for the default entry:
                for defaultEntry in PostTableList:
                    if float(defaultEntry[0]) == float(postID):
                        print("\n-----FOUND THE ENTRY-----\n")
                        entryToSearchFor = defaultEntry
                        break
                print("\n The original Length of the list was: " + str(len(PostTableList)))
                PostTableList.remove(entryToSearchFor)
                print(" But after removing the duplicate default entry, the new length of the list is: " + str(len(PostTableList)) + "\n")

        
            
            PostTableList.append((postID, postText, post_datetime, tempUserID, is_retweet_int, is_reply_int, current_retweeted_postID, original_postersUserID, favourite_count, retweet_count))
            PostList.append(float(postID))

            # E) Next thing to do will be to parse out the tagged person, links, media (images/videos), etc NOTE: I possibly should add the ability to include the indices of the person being tagged, where the link it, where the media is, etc. NOTE: Not all people who are said to have been tagged in the entities column are actually tagged in the post! so I will need to double check this by seeing if that user's handle is included in the Text of the post before adding them to the tagged list!
            # E) i) Determine if there are any people which have been tagged in the post. Row 73 might be a good example of multiple tags! DONE!
            if "'user_mentions': [{" in entities:   # If there is at least one user who has been tagged (mentioned) in a post.
                numberOfMentions = entities.count("screen_name")    # The number of users mentioned in the post
                # Here I need to get the screen name and the name of each user mentioned! NOTE: A user who is being replied to counts as being mentioned!
                for i in range(numberOfMentions):
                    # Get the index of the first character of the nth user mentioned for both their name and their screen_name (AKA handle)
                    sub_str_name = "'name': '"
                    sub_str_handle = "'screen_name': '"
                    
                    userName = extractSubstringFromEntities(sub_str_name, i, entities)
                    
                    handle = extractSubstringFromEntities(sub_str_handle, i, entities)
                    
                    # If the user is a new user (AKA if their handle is not in the handle list), then create a new user account for them!
                    if handle not in UserList:
                        # Extract the person's first and last name!
                        # Part 1: Last name - To extract the last name, find the index of the last whitespace character in their name.
                        lastName_index = userName.rfind(" ")
                        lastName = userName[lastName_index+1:len(userName)] # This isn't perfect, it will say that some "people's" names are "News" or "Jr." (For donald trump Jr.), but it will work for my purposes!
                        firstName = None
                        if (len(lastName) == len(userName)):
                            firstName = lastName
                            lastName = "NULL"
                        else:
                            firstName = userName[0:lastName_index]
                            lastName = "'"+lastName+"'"
                        # Part 2: Create the new users!
                        PersonTableList.append((userID, firstName, lastName, "DEFAULT", default_Birthday, default_BirthMonth, default_BirthYear,default_Gender, default_Description, "DEFAULT"))
                        UserList.append(handle)
                        PersonHandleList.append((userID, handle))
                        # Increment the userID by one.
                        userID = userID + 1
                        
                    # Get the userID of the user which will be added to the PostPeopleTaggedTableList!
                    taggedUserID = None
                    for x in PersonHandleList:
                        if x[1] == handle:
                            taggedUserID = x[0]
                    if taggedUserID == None: # If there is no user corresponding to the current handle, print out an error message!
                        print("\n\n\n******\nERROR\n******\nInvalid UserID! Or there is no user in the PersonHandle list corresponding to the handle " + handle + "\n******\n\n\n")

                    # Now that we know that the current user mentioned is a valid user, entries in the PostPeopleTaggedTable can be created (PostID, TagIndex, UserID)
                    PostPeopleTaggedTableList.append((postID, i + 1, taggedUserID))
                    # IF THIS POST IS A RETWEETED POST, CREATING A CORRESPONDING ENTRY FOR THE ORIGINAL POST!!!
                    if is_retweet_int == 1 and handle != original_author: # If the mentioned user is not the author of the post, and the current post is retweeted, create an entry for the retweeted post as well. (First mention is always the original author, so we skip that one when dealing with indices, which is why we start from i and not i+1!)
                        PostPeopleTaggedTableList.append((current_retweeted_postID, i, taggedUserID))

            # E) ii) Determine if there are any links or media, if so, add an entry to the appropriate table - NOTE: Row 20 is good because it has a picture and it has a URL! - DONE.
            if "expanded_url" in entities:    # If there is at least one URL included in the post
                default_Vine_URL1 = "https://vine.co/"
                default_Vine_URL2 = "http://vine.co/"
                default_Twitter_URL = "//twitter.com/"
                default_Twitter_Photo = "/photo/"
                default_Twitter_Video = "/video/"
                numberOfLinks = entities.count("expanded_url")

                linkTableIndex = 1 # Variable to keep track of the actual links included in a post
                mediaTableIndex = 1 # Variable to keep track of the media links included in a post
                for i in range(numberOfLinks):
                    sub_str_url = "'expanded_url': '"
                    currentPostURL = extractSubstringFromEntities(sub_str_url, i, entities)
                    
                    if (default_Vine_URL1 in currentPostURL) or (default_Vine_URL2 in currentPostURL) or (default_Twitter_URL in currentPostURL and default_Twitter_Photo in currentPostURL) or (default_Twitter_URL in currentPostURL and default_Twitter_Video in currentPostURL):
                        # If the current URL is a form of media, add it to the PostMediaTableList!
                        PostMediaTableList.append((postID, mediaTableIndex, currentPostURL))
                        # IF the current post is a retweet, create a corresponding entry for the original post!
                        if is_retweet_int == 1:
                            PostMediaTableList.append((current_retweeted_postID, mediaTableIndex, currentPostURL))
                        mediaTableIndex = mediaTableIndex + 1
                    else:
                        # If the current URL is not a form of media, add it to the PostLinksTableList!
                        PostLinksTableList.append((postID, linkTableIndex, currentPostURL))
                        # IF the current post is a retweet, create a corresponding entry for the original post!
                        if is_retweet_int == 1:
                            PostLinksTableList.append((current_retweeted_postID, linkTableIndex, currentPostURL))
                        linkTableIndex = linkTableIndex + 1

            # E) iii) Determine if there are any topics linked to this post (AKA are there any hashtags?)
            if "'hashtags': [{" in entities:
                numberOfTopics = entities.count("'text':")
                topic_Name_Identifier = "'text': '"
                for i in range(numberOfTopics):
                    topicName = extractSubstringFromEntities(topic_Name_Identifier, i, entities)
                    #print("\nThe HashTag is: " + topicName + "\n")

                    if topicName not in TopicList: # If this is a new hashtag, create a new entry in the Topic Table List!
                        TopicTableList.append((topicName, default_NumberOfFollowers))
                        TopicList.append(topicName)
                    
                    # Now that the current topic has been created, add the topic to the posttopictablelist
                    PostTopicsTableList.append((postID, i + 1, topicName))
                    # IF the current post is a retweet, create a corresponding entry for the original post!
                    if is_retweet_int == 1:
                        PostTopicsTableList.append((current_retweeted_postID, i + 1, topicName))

                #{'media': [{'display_url': 'pic.twitter.com/R6lVvgLECG', 'expanded_url': 'https://twitter.com/HillaryClinton/status/780840847256453120/photo/1', 'sizes': {'medium': {'h': 512, 'resize': 'fit', 'w': 1024}, 'thumb': {'h': 150, 'resize': 'crop', 'w': 150}, 'large': {'h': 512, 'resize': 'fit', 'w': 1024}, 'small': {'h': 340, 'resize': 'fit', 'w': 680}}, 'id_str': '780840750967844864', 'indices': [95, 118], 'id': 780840750967844864, 'url': 'https://t.co/R6lVvgLECG', 'media_url_https': 'https://pbs.twimg.com/media/CtYahqOWcAAGMXX.jpg', 'type': 'photo', 'media_url': 'http://pbs.twimg.com/media/CtYahqOWcAAGMXX.jpg'}], 'user_mentions': [], 'symbols': [], 'urls': [{'display_url': 'IWillVote.com', 'expanded_url': 'http://IWillVote.com', 'indices': [71, 94], 'url': 'https://t.co/tTgeqxNqYm'}], 'hashtags': [{'text': 'NationalVoterRegistrationDay', 'indices': [5, 34]}]}

                #{'user_mentions': [{'id_str': '1707321486', 'name': 'Madeleine Albright', 'id': 1707321486, 'screen_name': 'madeleine', 'indices': [3, 13]}, {'id_str': '172858784', 'name': 'Senator Tim Kaine', 'id': 172858784, 'screen_name': 'timkaine', 'indices': [16, 25]}, {'id_str': '42889581', 'name': 'Wellesley College', 'id': 42889581, 'screen_name': 'Wellesley', 'indices': [41, 51]}, {'id_str': '1339835893', 'name': 'Hillary Clinton', 'id': 1339835893, 'screen_name': 'HillaryClinton', 'indices': [80, 95]}], 'symbols': [], 'urls': [], 'hashtags': []}

        
        print("Linecount is" + str(line_count))

# F) After all of the data has been extracted from the CSV file and parsed into the correct lists, create entries for the FollowsPersonTable, FollowsTopicTable, LikesPostTable, and ReadPostTable
# F) i) Create entries in the follows person table
FollowsPersonTableList.append((1,2))
FollowsPersonTableList.append((2,1))
# F) ii) Create entries in the follows topic table
TrumpList = [("MAGA", 1), ("Trump2016",1), ("Trump4President",1), ("VoteTrump", 1), ("GOPDebate",1), ("GOPdebate", 1), ("Obamacare", 1), ("POTUS", 1), ("MakeAmericaGreatAgain", 1), ("WeAreBernie", 1), ("FoxNews", 1), ("ImWithYou", 1), ("NationalVoterRegistrationDay", 1), ("LoveTrumpsHate",1),("StrongerTogether",1),("SheWon",1)]
HillaryList = [("MAGA", 2), ("Trump2016",2), ("Trump4President",2), ("VoteTrump", 2), ("GOPDebate",2), ("GOPdebate", 2), ("Obamacare", 2), ("POTUS", 2), ("MakeAmericaGreatAgain", 2), ("WeAreBernie", 2), ("FoxNews", 2), ("ImWithYou", 2), ("NationalVoterRegistrationDay", 2), ("LoveTrumpsHate",2),("StrongerTogether",2),("SheWon",2)]
for entry in TrumpList:
    FollowsTopicTableList.append(entry)
for entry in HillaryList:
    FollowsTopicTableList.append(entry)
# F) iii) Create entries for the LikesPostTable and ReadPostTable - Both Trump and Hillary like the first 10 of each other's posts in the posts list
countHillaryPost = 0
countTrumpPost = 0
for tPost in PostTableList:
    if tPost[3] == "HillaryClinton" and countHillaryPost < 9:
        LikesPostTableList.append((tPost[0], 1))
        ReadPostTableList.append((tPost[0],1))
        countHillaryPost = countHillaryPost + 1
    elif tPost[3] == "realDonaldTrump" and countTrumpPost < 9:
        LikesPostTableList.append((tPost[0], 2))
        ReadPostTableList.append((tPost[0],2))
        countTrumpPost = countTrumpPost + 1
    if countTrumpPost >= 9 and countHillaryPost >= 9:
        break


# STEP 5: CREATE THE SQL INSERT STATEMENTS AND WRITE THEM TO THE SQL FILE
# A) Create insert statements for the PersonTable
sql_file.write("\n\n") # Create a gap between the table creation statements and the insert statements
for person in PersonTableList:
    sql_file.write("INSERT INTO PersonTable(UserID, First_Name, Last_Name, CreationDate, BirthDay, BirthMonth, BirthYear, Gender, Description, NumberOfFollowers) VALUES ("+str(person[0])+", '"+person[1]+"', "+person[2]+", "+person[3]+", "+str(person[4])+", '"+person[5]+"', "+str(person[6])+", '"+person[7]+"', '"+person[8]+"', "+person[9]+");\n")
# B) Create insert statements for the PersonHandleTable
sql_file.write("\n")
for personHandle in PersonHandleList:
    sql_file.write("INSERT INTO PersonHandleTable(UserID, Handle) VALUES ("+str(personHandle[0])+", '"+personHandle[1]+"');\n")
# C) Create insert statements for the PostTable
sql_file.write("\n") # Create a gap between the table creation statements and the insert statements
for post in PostTableList:
    sql_file.write("INSERT INTO PostTable(PostID, Text, Date, UserID, is_retweet, is_reply, Original_PostID, Original_Post_UserID, NumberOfLikes, NumberOfReposts) VALUES ("+str(post[0])+", '"+post[1]+"', "+post[2]+", "+str(post[3])+", "+str(post[4])+", "+str(post[5])+", "+str(post[6])+", "+str(post[7])+", "+str(post[8])+", "+str(post[9])+");\n")
# D) Create insert statements for the TopicTable
sql_file.write("\n")
for topic in TopicTableList:
    sql_file.write("INSERT INTO TopicTable(TopicID, NumberOfFollowers) VALUES ('"+topic[0]+"', "+str(topic[1])+");\n")
# E) Create insert statements for the FollowsPersonTable
sql_file.write("\n")
for following in FollowsPersonTableList:
    sql_file.write("INSERT INTO FollowsPersonTable(Following_UserID, FollowedBy_UserID) VALUES ("+str(following[0])+", "+str(following[1])+");\n")
# F) Create insert statements for the PostMediaTable
sql_file.write("\n")
for media in PostMediaTableList:
    sql_file.write("INSERT INTO PostMediaTable(PostID, Media_Number, Media_URL) VALUES ("+str(media[0])+", "+str(media[1])+", '"+media[2]+"');\n")
# G) Create insert statements for the PostLinksTable
sql_file.write("\n")
for links in PostLinksTableList:
    sql_file.write("INSERT INTO PostLinksTable(PostID, Link_Number, Link_URL) VALUES ("+str(links[0])+", "+str(links[1])+", '"+links[2]+"');\n")
# H) Create insert statements for the PostTopicsTable
sql_file.write("\n")
for topics in PostTopicsTableList:
    sql_file.write("INSERT INTO PostTopicsTable(PostID, Topic_Number, TopicID) VALUES ("+str(topics[0])+", "+str(topics[1])+", '"+topics[2]+"');\n")
# I) Create insert statements for the PostPeopleTaggedTable
sql_file.write("\n")
for tagged in PostPeopleTaggedTableList:
    sql_file.write("INSERT INTO PostPeopleTaggedTable(PostID, Tag_Number, UserID) VALUES ("+str(tagged[0])+", "+str(tagged[1])+", "+str(tagged[2])+");\n")
# J) Create insert statements for the LikesPostTable
sql_file.write("\n")
for likes in LikesPostTableList:
    sql_file.write("INSERT INTO LikesPostTable(PostID, UserID) VALUES ("+str(likes[0])+", "+str(likes[1])+");\n")
# K) Create insert statements for the ReadPostTable
sql_file.write("\n")
for reads in ReadPostTableList:
    sql_file.write("INSERT INTO ReadPostTable(PostID, UserID) VALUES ("+str(reads[0])+", "+str(reads[1])+");\n")
# L) Create insert statements for the FollowsTopicTable
sql_file.write("\n")
for follows in FollowsTopicTableList:
    sql_file.write("INSERT INTO FollowsTopicTable(TopicID, UserID) VALUES ('" + follows[0] + "', " + str(follows[1]) + ");\n")


# STEP 6: UPDATE THE AUTO_INCREMENT FIELDS FOR THE USERID AND POSTID FIELDS TO REFLECT THE PROPER STARTING VALUE WHICH THEY SHOULD USE WHICH ARE THE LOCAL VARIABLES userID and maxPostID + 1!!!
#ALTER TABLE table_name AUTO_INCREMENT = start_value;
sql_file.write("\nALTER TABLE PersonTable AUTO_INCREMENT = " + str(userID) + ";\n")
sql_file.write("\nALTER TABLE PostTable AUTO_INCREMENT = " + str(maxPostID) + ";\n")
# STEP 7: TURN ON THE FOREIGN KEY CHECKS!

sql_file.write("\nSET FOREIGN_KEY_CHECKS=1;\n") # Turn on foreign key checks once all of the tables have been created and data has been inserted into them!

# STEP 8: CLOSE THE SQL FILE!
sql_file.close()
