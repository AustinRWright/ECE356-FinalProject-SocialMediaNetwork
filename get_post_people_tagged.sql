CREATE DEFINER=`monty`@`%` PROCEDURE `get_post_people_tagged`(
IN `postID` BIGINT
)
BEGIN
	SELECT UserID, Tag_Number FROM PostPeopleTaggedTable WHERE PostPeopleTaggedTable.PostID = `postID`;
END