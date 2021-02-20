CREATE DEFINER=`monty`@`%` PROCEDURE `next_PostID`()
BEGIN # Return the ID value of the next entry to be input into the specified table (PersonTable or PostTable)
	SELECT Max(PostID) FROM PostTable;
END