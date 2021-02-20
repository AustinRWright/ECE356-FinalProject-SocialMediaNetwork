CREATE DEFINER=`monty`@`%` PROCEDURE `add_link_to_post`(IN postID BIGINT, IN linkNumber INT, IN linkText VARCHAR(250))
BEGIN
	INSERT INTO PostLinksTable(PostID, Link_Number, Link_URL) VALUES (postID, linkNumber, linkText);
END