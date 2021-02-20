CREATE DEFINER=`monty`@`%` PROCEDURE `create_new_userHandle`(
IN userID BIGINT,
IN userHandle VARCHAR(250)
)
BEGIN
START TRANSACTION;
INSERT INTO PersonHandleTable(UserID, Handle) VALUES (userID, userHandle);
COMMIT;
END