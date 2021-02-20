CREATE DEFINER=`monty`@`%` PROCEDURE `create_new_post`(
IN userID BIGINT,
IN postText VARCHAR(250),
IN isRepost BOOL,
IN isReply BOOL,
IN OriginalPostID BIGINT,
IN OriginalPostUserID BIGINT)
BEGIN
	INSERT INTO PostTable(PostID, Text, Date, UserID, is_retweet, is_reply, Original_PostID, Original_Post_UserID, NumberOfLikes, NumberOfReposts) VALUES (DEFAULT, postText, DEFAULT, userID, isRepost, isReply, OriginalPostID, OriginalPostUserID, DEFAULT, DEFAULT);
END