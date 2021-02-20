CREATE DEFINER=`monty`@`%` PROCEDURE `follow_topic`(IN `topicID` VARCHAR(250), IN userID BIGINT)
BEGIN
	INSERT INTO FollowsTopicTable(TopicID, UserID) VALUES (`topicID`, userID);
    UPDATE TopicTable SET NumberOfFollowers = NumberOfFollowers + 1 WHERE TopicTable.TopicID=`topicID`;
END