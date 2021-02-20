CREATE DEFINER=`monty`@`%` PROCEDURE `display_all_followed_people`(IN `userID` BIGINT)
BEGIN
	SELECT Handle, First_Name, Last_Name, PersonTable.UserID, NumberOfFollowers FROM (PersonTable Natural Join PersonHandleTable) WHERE PersonTable.UserID IN (SELECT Following_UserID FROM FollowsPersonTable WHERE FollowedBy_UserID = `userID` );
END