CREATE DEFINER=`monty`@`%` PROCEDURE `get_post_topics`(
IN `postID` BIGINT
)
BEGIN
	SELECT TopicID, Topic_Number FROM PostTopicsTable WHERE PostTopicsTable.PostID = `postID`;
END