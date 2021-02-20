CREATE DEFINER=`monty`@`%` PROCEDURE `add_media_to_post`(IN postID BIGINT, IN mediaNumber INT, IN mediaText VARCHAR(250))
BEGIN
	INSERT INTO PostMediaTable(PostID, Media_Number, Media_URL) VALUES (postID, mediaNumber, mediaText);
END