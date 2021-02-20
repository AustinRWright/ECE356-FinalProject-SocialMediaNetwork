CREATE PROCEDURE `is_userhandle_available` (IN userHandle VARCHAR(250))
BEGIN
	SELECT Handle
    FROM PersonHandleTable
    WHERE Handle Like userHandle;
END
