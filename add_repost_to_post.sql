CREATE DEFINER=`monty`@`%` PROCEDURE `add_repost_to_post`(IN `postID` BIGINT)
BEGIN
	UPDATE PostTable SET NumberOfReposts = NumberOfReposts + 1 WHERE PostTable.PostID = `postID`;
END