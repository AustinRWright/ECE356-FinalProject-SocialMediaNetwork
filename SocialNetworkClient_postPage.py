import mysql.connector
import SocialNetworkClient_followEntityPage

# A file for creating a new post/ Maybe deleting posts?
# Create a class which will provide functions to display all available entities to follow and all of the entities which you are currently following
class postPage():
    def __init__(self, mysqlConnector):
        self.mysqlConnector = mysqlConnector
    
    # Function to determine if a string represents an integer
    def RepresentsInt(self,s):
        try:
            value = int(s)
            return True
        except ValueError:
            return False

    # Create a new post ----- NOTE: Also leveraged for a response post.
    def createNewPost(self, userID, originalPostID):
        # 1. Welcome the user to the Post page and prompt for input
        print("\n---------- Welcome to the Post Page ----------\n")
        postText = None
        while(True):
            postText = input("Please enter the text of your post below (Between 1 and 250 characters)*: ")
            if len(postText) == 0 or len(postText) > 250:
                print("Invalid length of text, please try again.")
            else:
                break
        postLinks = []
        while(len(postLinks) < 5):
            postLinkText = input("Links: To add a URL to your post, enter them one by one below, pressing enter after each one (Maximum of 5). If you wish to skip this, just press enter: ")
            if len(postLinkText) > 250:
                print("Invalid length of text, please try again.")
            elif len(postLinkText) == 0:
                break
            else:
                postLinks.append(postLinkText)
        postTopics = []
        while(len(postTopics) < 5):
            postTopicText = input("Topics: To add a Topic to your post, enter them one by one below, pressing enter after each one (Maximum of 5). If you wish to skip this, just press enter: ")
            if len(postTopicText) > 100:
                print("Invalid length of text, please try again.")
            elif len(postTopicText) == 0:
                break
            else:
                postTopics.append(postTopicText)
        postMedia = []
        while(len(postMedia) < 5):
            postMediaText = input("Media: To add an image or video to your post, enter them one by one below (filename or URL), pressing enter after each one (Maximum of 5). If you wish to skip this, just press enter: ")
            if len(postMediaText) > 250:
                print("Invalid length of text, please try again.")
            elif len(postMediaText) == 0:
                break
            else:
                postMedia.append(postMediaText)
        # List all of the users which can be mentioned in your post
        followEntityPage = SocialNetworkClient_followEntityPage.followEntityPage(self.mysqlConnector)
        followEntityPage.displayAllPeople(userID)

        postMentions = []
        numberOfAllowedPostMentions = 5
        originalPostUserID = None # Used in the command to create the post.
        is_reply = 0
        if originalPostID is not None:
        # If this is a post replying to another post, automatically include the original poster's userID in the mentions list.
            numberOfAllowedPostMentions = 4
            is_reply = 1
            postContentsList = self.getValuesFromPost(originalPostID, "get_post_contents")
            for post in postContentsList:
                originalPostUserID = post[3]
                postMentions.append(originalPostUserID)
        while(len(postMentions) < 5):
            postMentionsUserID = input("Tag People: To tag people in your post, enter their UserIDs one by one below, pressing enter after each one (Maximum of "+ str(numberOfAllowedPostMentions)+"). If you wish to skip this, just press enter: ")
            if len(postMentionsUserID) > 250:
                print("Invalid length of text, please try again.")
            elif len(postMentionsUserID) == 0:
                break
            else:
                # Need to check that the userID added is valid.
                args = [postMentionsUserID]
                cursor = self.mysqlConnector.cursor(buffered=True, dictionary=True)
                cursor.callproc("get_handle_from_userID", args)
                userIDEntryList = None
                for result in cursor.stored_results():
                    userIDEntryList = result.fetchall() # Store the results of the query in a list
                if userIDEntryList is not None:
                    postMentions.append(postMentionsUserID)
                else:
                    print("Invalid UserID, please try again.")
        
        # Create the entry for the postTable!
        is_repost = 0 # This post is not being reposted
        try:
            args = [userID, postText, is_repost, is_reply, originalPostID, originalPostUserID]
            cursor = self.mysqlConnector.cursor(buffered=True, dictionary=True)
            cursor.callproc("create_new_post", args)
            self.mysqlConnector.commit()
        except:
            self.mysqlConnector.rollback()
            print("FAILED TO CREATE A NEW POST")
            return

        # GET THE POST ID
        cursor = self.mysqlConnector.cursor(buffered=True, dictionary=True)
        cursor.callproc("next_PostID")
        postID = []
        for result in cursor.stored_results():
            postID = result.fetchall()
        currentPostID = postID[0][0]

        if len(postLinks) > 0:
            for i in range(len(postLinks)):
                args = [currentPostID, i+1, postLinks[i]]
                try:
                    cursor.callproc("add_link_to_post", args)
                    self.mysqlConnector.commit()
                except:
                    self.mysqlConnector.rollback()
                    print("FAILED TO ADD LINK TO POST")
                    return

        if len(postMedia) > 0:
            for i in range(len(postMedia)):
                args = [currentPostID, i+1, postMedia[i]]
                try:
                    cursor.callproc("add_media_to_post", args)
                    self.mysqlConnector.commit()
                except:
                    self.mysqlConnector.rollback()
                    print("FAILED TO ADD MEDIA TO POST")
                    return

        if len(postMentions) > 0:
            for i in range(len(postMentions)):
                args = [currentPostID, i+1, postMentions[i]]
                try:
                    cursor.callproc("add_mention_to_post", args)
                    self.mysqlConnector.commit()
                except:
                    self.mysqlConnector.rollback()
                    print("FAILED TO ADD MENTION TO POST")
                    return

        if len(postTopics) > 0:
            for i in range(len(postTopics)):
                # IF THE TOPIC DOES NOT YET EXIST, FIRST CREATE THE TOPIC AND THEN ADD THE TOPIC TO THE POST.
                args = [postTopics[i]]
                cursor.callproc("get_TopicID_entry", args)
                topicIDList = None
                for result in cursor.stored_results():
                    topicIDList = result.fetchall() # Store the results of the query in a list
                if len(topicIDList) == 0: # If there are no topics which already exist with that name
                    try:
                        cursor.callproc("create_new_topic", args)
                        self.mysqlConnector.commit()
                    except:
                        self.mysqlConnector.rollback()
                        print("FAILED TO CREATE NEW TOPIC")
                        return
                args = [currentPostID, i+1, postTopics[i]]
                try:
                    cursor.callproc("add_topic_to_post", args)
                    self.mysqlConnector.commit()
                except:
                    self.mysqlConnector.rollback()
                    print("FAILED TO ADD TOPIC TO POST")
                    return
        cursor.close()


    def createRepost(self, userID, originalPostID):
        # Essentially all I will be doing here is finding all of the entries for a post in its different tables, PostTable, PostMediaTable, PostPeopleTaggedTable, PostLinksTable, PostTopicsTable and duplicating almost all of the data there.
        cursor = self.mysqlConnector.cursor(buffered=True, dictionary=True)
        # 1. Get the post links
        args = [originalPostID]
        cursor.callproc("get_post_links", args)
        linksList = None
        for link in cursor.stored_results():
            linksList = link.fetchall()
        # 2. Get the post media
        args = [originalPostID]
        cursor.callproc("get_post_media", args)
        mediaList = None
        for media in cursor.stored_results():
            mediaList = media.fetchall()
        # 3. Get the people tagged in the post
        args = [originalPostID]
        cursor.callproc("get_post_people_tagged", args)
        peopleTaggedList = None
        for peopleTagged in cursor.stored_results():
            peopleTaggedList = peopleTagged.fetchall()
        # 4. Get the post topics
        args = [originalPostID]
        cursor.callproc("get_post_topics", args)
        topicsList = None
        for topic in cursor.stored_results():
            topicsList = topic.fetchall()
        # 5. Get the post contents
        args = [originalPostID]
        cursor.callproc("get_post_contents", args)
        postContentsList = None
        for result in cursor.stored_results():
            postContentsList = result.fetchall()
        
        # ---------- Now What I need to do is recreate all of these entries but for the current post!
        # 1. Create the new Post
        for postContents in postContentsList:
            PostID = postContents[0]# PostID = 10721
            PostText = postContents[1]# PostText = 'REUTERS ROLLING:  TRUMP 39%, CRUZ 14.5%, BUSH 10.6%, CARSON 9.6%, RUBIO 6.7%... MORE... https://t.co/nRhtbzcqP9'
            PostDateTime = postContents[2]# PostDateTime = datetime.datetime(2020, 4, 22, 16, 1, 17)
            PostUserID = postContents[3]# PosterUserID = 20
            isRepost = postContents[4]# isrepost = 0
            isReply = postContents[5]# isreply = 0
            OriginalPostID = postContents[6]# OriginalPostID = None
            OriginalPostUserID = postContents[7]# OriginalPostUserID = None
            NumberOfLikes = postContents[8]# NumberOfLikes = 0
            NumberOfReposts = postContents[9]# NumberOfReposts = 1

            # Create the entry for the postTable!
            try:
                args = [userID, PostText, 1, 0, originalPostID, PostUserID]
                cursor = self.mysqlConnector.cursor(buffered=True, dictionary=True)
                cursor.callproc("create_new_post", args)
                self.mysqlConnector.commit()
            except:
                self.mysqlConnector.rollback()
                print("FAILED TO CREATE A NEW POST")
                return

            # GET THE POST ID
            cursor = self.mysqlConnector.cursor(buffered=True, dictionary=True)
            cursor.callproc("next_PostID")
            postID = []
            for result in cursor.stored_results():
                postID = result.fetchall()
            currentPostID = postID[0][0]

            if len(linksList) > 0:
                for link in linksList:
                    args = [currentPostID, link[1], link[0]]
                    try:
                        cursor.callproc("add_link_to_post", args)
                        self.mysqlConnector.commit()
                    except:
                        self.mysqlConnector.rollback()
                        print("FAILED TO ADD LINK TO POST")
                        return

            if len(mediaList) > 0:
                for media in mediaList:
                    args = [currentPostID, media[1], media[0]]
                    try:
                        cursor.callproc("add_media_to_post", args)
                        self.mysqlConnector.commit()
                    except:
                        self.mysqlConnector.rollback()
                        print("FAILED TO ADD MEDIA TO POST")
                        return

            if len(peopleTaggedList) > 0:
                for mention in peopleTaggedList:
                    args = [currentPostID, mention[1], mention[0]]
                    try:
                        cursor.callproc("add_mention_to_post", args)
                        self.mysqlConnector.commit()
                    except:
                        self.mysqlConnector.rollback()
                        print("FAILED TO ADD MENTION TO POST")
                        return

            if len(topicsList) > 0:
                for topic in topicsList:
                    args = [currentPostID, topic[1], topic[0]]
                    try:
                        cursor.callproc("add_topic_to_post", args)
                        self.mysqlConnector.commit()
                    except:
                        self.mysqlConnector.rollback()
                        print("FAILED TO ADD TOPIC TO POST")
                        return
            try:
                args = [originalPostID]
                cursor.callproc("add_repost_to_post", args)
                self.mysqlConnector.commit()
            except:
                self.mysqlConnector.rollback()
                print("FAILED TO INCREMENT THE REPOST COUNTER ON THE ORIGINAL POST!")
            cursor.close()
            

    def likePost(self, userID, postID):
        # Essentially all I need to do is query the user for an input, verify that it is valid, and then create an entry in the LikesPostTable
        cursor = self.mysqlConnector.cursor(buffered=True, dictionary=True)
        try:
            args = [postID, userID]
            cursor.callproc("add_post_like", args)
            self.mysqlConnector.commit()
        except:
            self.mysqlConnector.rollback()
            print("FAILED TO INCREMENT THE LIKE COUNTER ON THE POST!")

    def getValuesFromPost(self, originalPostID, storedProcedureName):
        args = [originalPostID]
        cursor = self.mysqlConnector.cursor(buffered=True, dictionary=True)
        cursor.callproc(storedProcedureName, args)
        contentsList = None
        for result in cursor.stored_results():
            contentsList = result.fetchall()
        cursor.close()
        return contentsList