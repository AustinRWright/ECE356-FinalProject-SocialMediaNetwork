CREATE DEFINER=`monty`@`%` PROCEDURE `get_TopicID_entry`(IN `topicID` VARCHAR(250))
BEGIN
	SELECT * FROM TopicTable WHERE TopicTable.TopicID = `topicID`;
END