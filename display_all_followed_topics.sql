CREATE DEFINER=`monty`@`%` PROCEDURE `display_all_followed_topics`(IN `userID` BIGINT)
BEGIN
	SELECT TopicID, NumberOfFollowers FROM FollowsTopicTable NATURAL JOIN TopicTable WHERE FollowsTopicTable.UserID = `userID`;
END