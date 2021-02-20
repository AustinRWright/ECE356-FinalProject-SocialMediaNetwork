CREATE DEFINER=`monty`@`%` PROCEDURE `get_post_links`(
IN `postID` BIGINT
)
BEGIN
	SELECT Link_URL, Link_Number FROM PostLinksTable WHERE PostLinksTable.PostID = `postID`;
END