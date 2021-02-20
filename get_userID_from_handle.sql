CREATE DEFINER=`monty`@`%` PROCEDURE `get_userID_from_handle`(IN userHandle VARCHAR(250))
BEGIN 
	SELECT UserID
    FROM PersonHandleTable
    WHERE Handle Like  userHandle;
END