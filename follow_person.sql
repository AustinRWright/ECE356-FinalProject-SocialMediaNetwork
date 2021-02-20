CREATE DEFINER=`monty`@`%` PROCEDURE `follow_person`(IN followingID BIGINT, IN followedByID BIGINT)
BEGIN
	INSERT INTO FollowsPersonTable(Following_UserID, FollowedBy_UserID) VALUES (followingID, followedByID);
    UPDATE PersonTable SET NumberOfFollowers = NumberOfFollowers + 1 WHERE UserID = followingID;
END