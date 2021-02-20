CREATE DEFINER=`monty`@`%` PROCEDURE `next_UserID`()
BEGIN # Return the ID value of the next entry to be input into the specified table (PersonTable or PostTable)
	SELECT Max(UserID) AS UserID FROM PersonTable;
END