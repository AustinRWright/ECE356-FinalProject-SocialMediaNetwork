CREATE DEFINER=`monty`@`%` PROCEDURE `unfollow_person`(IN followingID BIGINT, IN followedByID BIGINT)
BEGIN
	DELETE FROM FollowsPersonTable WHERE Following_UserID = followingID AND FollowedBy_UserID=followedByID;
    UPDATE PersonTable SET NumberOfFollowers = NumberOfFollowers - 1 WHERE UserID = followingID;
END