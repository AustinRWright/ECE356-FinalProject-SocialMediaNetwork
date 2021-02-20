CREATE DEFINER=`monty`@`%` PROCEDURE `create_new_topic`(IN topicID VARCHAR(100))
BEGIN
 INSERT INTO TopicTable(TopicID, NumberOfFollowers) VALUES (topicID, 0);
END