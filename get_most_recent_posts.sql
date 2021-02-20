CREATE DEFINER=`monty`@`%` PROCEDURE `get_most_recent_posts`(
IN `userID` BIGINT)
BEGIN
# NOT DONE YET... STILL HAVEN'T DETERMINED WHICH POSTS HAVE BEEN READ BY THE USER YET
	SELECT * FROM PostTable 
	WHERE PostID IN (SELECT PostID FROM PostTopicsTable WHERE TopicID IN(SELECT TopicID FROM FollowsTopicTable WHERE FollowsTopicTable.UserID=`userID`)) 
	OR PostID IN (SELECT PostID FROM PostPeopleTaggedTable WHERE PostPeopleTaggedTable.UserID IN (SELECT Following_UserID FROM FollowsPersonTable WHERE FollowedBy_UserID=`userID`))
    OR PostTable.UserID IN (SELECT Following_UserID FROM FollowsPersonTable WHERE FollowedBy_UserID=`userID` and Following_UserID = PostTable.UserID)
	OR PostTable.UserID = `userID`
	OR PostID IN (SELECT PostID FROM PostPeopleTaggedTable WHERE PostPeopleTaggedTable.UserID=`userID`) ORDER BY Date DESC LIMIT 5;
END