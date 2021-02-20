CREATE DEFINER=`monty`@`%` PROCEDURE `does_person_follow_you`(IN `their_userID` BIGINT)
BEGIN
	SELECT * FROM FollowsPersonTable WHERE FollowedBy_UserID = `their_userID`;
END