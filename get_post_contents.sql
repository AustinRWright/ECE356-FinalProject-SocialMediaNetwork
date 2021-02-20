CREATE DEFINER=`monty`@`%` PROCEDURE `get_post_contents`(IN `postID` BIGINT)
BEGIN
		SELECT * FROM PostTable WHERE PostTable.PostID=`postID`;
END