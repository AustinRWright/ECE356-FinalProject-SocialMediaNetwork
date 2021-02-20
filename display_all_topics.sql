CREATE DEFINER=`monty`@`%` PROCEDURE `display_all_topics`()
BEGIN
	SELECT TopicID, NumberOfFollowers FROM TopicTable;
END