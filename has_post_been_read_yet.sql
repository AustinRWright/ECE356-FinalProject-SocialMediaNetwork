CREATE DEFINER=`monty`@`%` PROCEDURE `has_post_been_read_yet`(
IN `userID` BIGINT,
IN `previousPostID` BIGINT
)
BEGIN
	SELECT PostID FROM ReadPostTable Where ReadPostTable.UserID=`userID` and PostID=`previousPostID`;
END