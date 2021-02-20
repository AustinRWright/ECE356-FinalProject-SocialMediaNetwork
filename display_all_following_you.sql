CREATE DEFINER=`monty`@`%` PROCEDURE `display_all_following_you`(IN `userID` BIGINT)
BEGIN
	SELECT FollowedBy_UserID FROM FollowsPersonTable WHERE Following_UserID = `userID`;
END