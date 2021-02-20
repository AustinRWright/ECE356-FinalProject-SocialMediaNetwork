CREATE DEFINER=`monty`@`%` PROCEDURE `mark_post_as_read`(
IN `userID` BIGINT,
IN `postID` BIGINT
)
BEGIN
	INSERT INTO ReadPostTable(PostID, UserID) VALUES (`postID`, `userID`);
END