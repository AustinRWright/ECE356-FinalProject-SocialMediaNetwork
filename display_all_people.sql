CREATE DEFINER=`monty`@`%` PROCEDURE `display_all_people`(IN `userID` BIGINT)
BEGIN
	SELECT Handle, First_Name, Last_Name, PersonTable.UserID, NumberOfFollowers FROM (PersonTable Natural Join PersonHandleTable) WHERE PersonTable.UserID != `userID`;
END