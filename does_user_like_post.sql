CREATE DEFINER=`monty`@`%` PROCEDURE `does_user_like_post`(IN `postID` BIGINT, IN `userID` BIGINT)
BEGIN
	SELECT * FROM LikesPostTable WHERE LikesPostTable.PostID = `postID` AND LikesPostTable.UserID = `userID`;
END