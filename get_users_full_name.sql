CREATE DEFINER=`monty`@`%` PROCEDURE `get_users_full_name`(IN `userID` BIGINT)
BEGIN
	SELECT First_Name, Last_Name FROM PersonTable WHERE PersonTable.UserID = `userID`;
END