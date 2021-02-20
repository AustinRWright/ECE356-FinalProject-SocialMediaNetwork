CREATE DEFINER=`monty`@`%` PROCEDURE `add_topic_to_post`(IN postID BIGINT, IN topicNumber INT, IN TopicID VARCHAR(100))
BEGIN
	INSERT INTO PostTopicsTable(PostID, Topic_Number, TopicID) VALUES (postID, topicNumber, TopicID);
END