CREATE DEFINER=`monty`@`%` PROCEDURE `get_handle_from_userID`(IN `userID` BIGINT)
BEGIN
	SELECT Handle FROM PersonHandleTable WHERE PersonHandleTable.UserID = `userID`;
END