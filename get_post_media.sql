CREATE DEFINER=`monty`@`%` PROCEDURE `get_post_media`(
IN `postID` BIGINT
)
BEGIN
	SELECT Media_URL, Media_Number FROM PostMediaTable WHERE PostMediaTable.PostID = `postID`;
END