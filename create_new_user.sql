CREATE DEFINER=`monty`@`%` PROCEDURE `create_new_user`(
IN firstName VARCHAR(100),
IN lastName VARCHAR(100),
IN birthday INT,
IN birthmonth ENUM('January','February','March','April','May','June','July','August','September','October','November','December'),
IN birthyear INT,
IN gender VARCHAR(100),
IN description VARCHAR(250))
BEGIN
START TRANSACTION;
# Create an entry in the Person Table and then an entry in the PersonHandleTable
INSERT INTO PersonTable(UserID, First_Name, Last_Name, CreationDate, BirthDay, BirthMonth, BirthYear, Gender, Description, NumberOfFollowers) VALUES (DEFAULT, firstName, lastName, DEFAULT, birthday, birthmonth, birthyear, gender, description, 0);
COMMIT;
END