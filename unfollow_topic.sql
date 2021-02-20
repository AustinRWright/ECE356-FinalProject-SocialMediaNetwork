CREATE DEFINER=`monty`@`%` PROCEDURE `unfollow_topic`(IN topicID VARCHAR(250), IN userID BIGINT)
BEGIN
	DELETE FROM FollowsTopicTable WHERE TopicID=topicID AND UserID=userID;
    UPDATE TopicTable SET NumberOfFollowers = NumberOfFollowers - 1 WHERE TopicID=topicID;
END