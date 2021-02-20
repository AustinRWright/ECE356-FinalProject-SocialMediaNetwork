CREATE DEFINER=`monty`@`%` PROCEDURE `add_post_like`(IN `postID` BIGINT, IN userID BIGINT)
BEGIN
	INSERT INTO LikesPostTable(PostID, UserID) VALUES (`postID`, userID);
    UPDATE PostTable SET NumberOfLikes = NumberOfLikes + 1 WHERE PostTable.PostID = `postID`;
END