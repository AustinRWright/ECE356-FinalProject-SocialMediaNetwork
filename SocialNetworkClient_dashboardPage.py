import mysql.connector

# This file will be used to display posts to the user. - Will need to check for the cases where not all 5 posts returned by the query are populated (maybe because you have read through all available posts. Could be the last 4,3,2,1 and should never be 0 but it is possible!)

# Create a class which will provide functions to retrieve the next 5 posts for the specific user!
class dashboardPage():
    def __init__(self, mysqlConnector):
        self.mysqlConnector = mysqlConnector
    
    # Function to determine if a string represents an integer
    def RepresentsInt(self,s):
        try:
            value = int(s)
            return True
        except ValueError:
            return False

    # If the postID is null, then display the most recent 5 posts relevant to the user. If the postID is not null, then display the next five posts where the date when they were posted is less than the date when the post specified by postID was posted
    def displayNextFivePosts(self, postID, userID): # Returns the oldest and newest postIDs of the 5 most recent posts to be displayed. 
        if postID is None:
            # Get the first 5 posts for this user.
            cursor = self.mysqlConnector.cursor(buffered=True, dictionary=True) # "Dictionary In Cursor" from https://stackoverflow.com/questions/10195139/how-to-retrieve-sql-result-column-value-using-column-name-in-python/56209874#56209874
            args = [userID]
            cursor.callproc("get_most_recent_posts", args)
            postList = None
            for result in cursor.stored_results():
                postList = result.fetchall() # Store the results of the query in a list
            firstPostID = None
            lastPostID = None
            for x in range(5):
                print("\n")
            if len(postList) != 0:
                firstPostID = postList[0][0]
                lastPostID = postList[0][0]
                for post in postList: # Need to check if the current post is None
                    if post is not None:
                        self.printPostContents(post, userID)
                        lastPostID = post[0]
                return [firstPostID, lastPostID]
            else:
                print("\n\n\nNo Posts To Show\n\n\n")
                return [None, None]
        else:
            # Get the next 5 posts for this user.
            cursor = self.mysqlConnector.cursor(buffered=True, dictionary=True) # "Dictionary In Cursor" from https://stackoverflow.com/questions/10195139/how-to-retrieve-sql-result-column-value-using-column-name-in-python/56209874#56209874
            args = [userID, postID]
            cursor.callproc("get_next_5_posts", args)
            postList = None
            for result in cursor.stored_results():
                postList = result.fetchall() # Store the results of the query in a list
            firstPostID = None
            lastPostID = None
            for x in range(5):
                print("\n")
            if len(postList) != 0:
                firstPostID = postList[0][0]
                lastPostID = postList[0][0]
                for post in postList: # Need to check if the current post is None
                    if post is not None:
                        self.printPostContents(post, userID)
                        lastPostID = post[0]
                return [firstPostID, lastPostID]
            else:
                print("\n\n\nNo Posts To Show\n\n\nTo Change This You Can Do One Of The Following:\n - Follow A Topic\n - Follow A Person\n - Create Your Own Post\n\n\n")
                return [None, None]

    # THIS FUNCTION WILL BE CALLED BY OTHER FUNCTIONS TO DISPLAY THE CONTENTS OF THE POST OBJECT PASSED IN, IT SHOULD INDICATE IF A POST IS read, liked, who posted it, if it is a repost, if it is a reply, who the original author is, when it was posted, the text, the images, the links, the people tagged (Mentioned), and the number of likes and the number of reposts
    def printPostContents(self, postObjectList, userID): # Calls self.hasPostBeenRead before diplaying the contents to tell if the post has been read or not by the user. IF IT HASNT BEEN READ YET, display it as unread BUT update the ReadPostTable to include the entry that the user has now read  the post
        cursor = self.mysqlConnector.cursor(buffered=True, dictionary=True)
        # Each list has the following structure (10721, 'REUTERS ROLLING:  TRUMP 39%, CRUZ 14.5%, BUSH 10.6%, CARSON 9.6%, RUBIO 6.7%... MORE... https://t.co/nRhtbzcqP9', datetime.datetime(2020, 4, 22, 16, 1, 17), 20, 0, 0, None, None, 0, 1)
        # THESE VALUES CORRESPOND TO:
        PostID = postObjectList[0]# PostID = 10721
        PostText = postObjectList[1]# PostText = 'REUTERS ROLLING:  TRUMP 39%, CRUZ 14.5%, BUSH 10.6%, CARSON 9.6%, RUBIO 6.7%... MORE... https://t.co/nRhtbzcqP9'
        PostDateTime = postObjectList[2]# PostDateTime = datetime.datetime(2020, 4, 22, 16, 1, 17)
        PostUserID = postObjectList[3]# PosterUserID = 20
        isRepost = postObjectList[4]# isrepost = 0
        isReply = postObjectList[5]# isreply = 0
        OriginalPostID = postObjectList[6]# OriginalPostID = None
        OriginalPostUserID = postObjectList[7]# OriginalPostUserID = None
        NumberOfLikes = postObjectList[8]# NumberOfLikes = 0
        NumberOfReposts = postObjectList[9]# NumberOfReposts = 1

        # 1. Get the post links
        args = [PostID]
        cursor.callproc("get_post_links", args)
        linksList = None
        for link in cursor.stored_results():
            linksList = link.fetchall()
        # 2. Get the post media
        args = [PostID]
        cursor.callproc("get_post_media", args)
        mediaList = None
        for media in cursor.stored_results():
            mediaList = media.fetchall()
        # 3. Get the people tagged in the post
        args = [PostID]
        cursor.callproc("get_post_people_tagged", args)
        peopleTaggedList = None
        for peopleTagged in cursor.stored_results():
            peopleTaggedList = peopleTagged.fetchall()
        # 4. Get the post topics
        args = [PostID]
        cursor.callproc("get_post_topics", args)
        topicsList = None
        for topic in cursor.stored_results():
            topicsList = topic.fetchall()
        # 5. Get if the post has been read by the user or not
        args = [userID, PostID]
        cursor.callproc("has_post_been_read_yet", args)
        readList = None
        for read in cursor.stored_results():
            readList = read.fetchall()
            #print(readList)

        hasBeenRead = False
        if len(readList) != 0 and readList is not None:
            if readList[0][0] == PostID: # If there is an entry in the read list, therefore this current post has been read by the user
                hasBeenRead = True
        else: # The current post has not been read previously by the user, so create a new entry in the read table to indicate that the user has now read the post
            args = [userID, PostID]
            try:
                cursor.callproc("mark_post_as_read", args) # NOTE: Uncomment this line when I actually want to be making permanent entries like this!!!! -------------------------------------------------------------------
                self.mysqlConnector.commit()
            except:
                self.mysqlConnector.rollback()
                print("FAILED TO MARK POST AS READ")

        # 6. Determine if you "LIKE" This post or not
        args = [PostID, userID]
        cursor.callproc("does_user_like_post", args)
        likeList = None
        for read in cursor.stored_results():
            likeList = read.fetchall()
        is_liked = False
        if len(likeList) != 0 and likeList is not None:
            if likeList[0][0] == PostID: # If there is an entry in the read list, therefore this current post has been read by the user
                is_liked = True

        print("\n----------------------------------------\n") # 40 dashes
        if hasBeenRead:
            print("READ\n")
        else:
            print("NOT READ\n")
        #1. Print the Post ID:
        print("PostID: " + str(PostID) + "\n")
        
        #2. Print the text of the post
        print("Text: " + PostText + "\n")

        #3. Print the User First Name (Last Name if it exists) and their UserName/handle, AND THE DATE WHEN IT WAS POSTED, And if it was a response or a retweet of a different post
        args = [PostUserID]
        cursor.callproc("get_users_full_name", args)
        fullNameList = None
        for fullName in cursor.stored_results():
            fullNameList = fullName.fetchall()
        fullNameString = None
        if fullNameList[0][1] is None:  # if there is no last name, just include the first name in the full name string
            fullNameString = fullNameList[0][0]
        else: # If there is a last name, include it in the fullName string
            fullNameString = fullNameList[0][0] + " " + fullNameList[0][1]

        cursor.callproc("get_handle_from_userID", args)
        handleList = None
        for handle in cursor.stored_results():
            handleList = handle.fetchall()
        handleString = handleList[0][0]

        currentTimeString = PostDateTime.strftime("%Y-%m-%d %H:%M:%S")

        # Check here for if the post was a reply or repost.
        if OriginalPostUserID is not None:
            firstString = None
            secondString = None
            originalFullNameString = None
            if isRepost == 1:
                firstString = "Reposted By: "
                secondString = " Originally Posted By: "
            elif isReply == 1:
                firstString = "Posted By: "
                secondString = " In Response To: "
            else: raise NotImplementedError("If there is an original userID, it should either be a repost or a response/rely. IT SHOULD NEVER GET TO THIS POINT")
            # Retrieve the mentioned/reposted user's full name and handle
            args = [OriginalPostUserID]
            cursor.callproc("get_users_full_name", args)
            originalFullNameList = None
            for fullName in cursor.stored_results():
                originalFullNameList = fullName.fetchall()
            if originalFullNameList[0][1] is None:  # if there is no last name, just include the first name in the full name string
                originalFullNameString = originalFullNameList[0][0]
            else: # If there is a last name, include it in the fullName string
                originalFullNameString = originalFullNameList[0][0] + " " + originalFullNameList[0][1]

            cursor.callproc("get_handle_from_userID", args)
            originalHandleList = None
            for handle in cursor.stored_results():
                originalHandleList = handle.fetchall()
            originalHandleString = originalHandleList[0][0]
            
            print(firstString + fullNameString + " (UserName: " + handleString + ") On " + currentTimeString + secondString + originalFullNameString + " (UserName: " + originalHandleString + ") Original PostID: " + str(OriginalPostID) + "\n")
        else:
            # Print the actual line
            print("Posted by: " + fullNameString + " (UserName: " + handleString + ") On " + currentTimeString + "\n")
        
        #4. Print the post topics
        topicListString = None
        if len(topicsList) > 0:
            topicListString = "Post Topics: "
            for currentTopic in topicsList: 
                if int(currentTopic[1]) == 1:
                    topicListString = topicListString + currentTopic[0]
                else:
                    topicListString = topicListString + ", " + currentTopic[0]
            print(topicListString + "\n")
        
        #5. Print the people mentioned
        # This one will involve the same work as above for getting the poster's name and username
        taggedListString = None
        if len(peopleTaggedList) > 0:
            taggedListString = "People Tagged: "
            for currentPerson in peopleTaggedList:
                args = [currentPerson[0]]
                cursor.callproc("get_users_full_name", args)
                tempFullNameList = None
                for fullName in cursor.stored_results():
                    tempFullNameList = fullName.fetchall()
                tempFullNameString = None
                if tempFullNameList[0][1] is None:  # if there is no last name, just include the first name in the full name string
                    tempFullNameString = tempFullNameList[0][0]
                else: # If there is a last name, include it in the fullName string
                    tempFullNameString = tempFullNameList[0][0] + " " + tempFullNameList[0][1]

                cursor.callproc("get_handle_from_userID", args)
                tempHandleList = None
                for handle in cursor.stored_results():
                    tempHandleList = handle.fetchall()
                tempHandleString = tempHandleList[0][0]

                if int(currentPerson[1]) == 1: # If this is the first person who was tagged in the post
                    taggedListString = taggedListString + tempFullNameString + " (UserName: " + tempHandleString + ")"
                else:
                    taggedListString = taggedListString + ", " + tempFullNameString + " (UserName: " + tempHandleString + ")"
            print(taggedListString + "\n")

        #6. Print the post media file names/URLs 
        taggedMediaList = None
        if len(mediaList) > 0:
            postMediaString = "Media: "
            for currentMedia in mediaList:
                if int(currentMedia[1]) == 1:
                    postMediaString = postMediaString + currentMedia[0]
                else:
                    postMediaString = postMediaString + ", " + currentMedia[0]
            print(postMediaString + "\n")

        #7. Print the post link URLs
        taggedLinksList = None
        if len(linksList) > 0:
            postLinksString = "Links: "
            for currentLink in linksList:
                if int(currentLink[1]) == 1:
                    postLinksString = postLinksString + currentLink[0]
                else:
                    postLinksString = postLinksString + ", " + currentLink[0]
            print(postLinksString + "\n")
        
        #8. Print the number of Likes and Reposts
        print("Number Of Likes: " + str(NumberOfLikes) + " Number Of Reposts: " + str(NumberOfReposts) + "\n")

        #9. Indicate if you like this post
        if (is_liked):
            print("You \"LIKE\" this post.\n")