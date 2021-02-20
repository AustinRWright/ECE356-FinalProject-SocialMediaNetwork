CREATE DEFINER=`monty`@`%` PROCEDURE `add_mention_to_post`(IN postID BIGINT, IN mentionNumber INT, IN userID BIGINT)
BEGIN
	INSERT INTO PostPeopleTaggedTable(PostID, Tag_Number, UserID) VALUES (postID, mentionNumber, userID);
END