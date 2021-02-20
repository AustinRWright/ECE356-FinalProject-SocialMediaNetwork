CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `monty`@`%` 
    SQL SECURITY DEFINER
VIEW `SocialNetworkDB`.`PersonPostView` AS
    SELECT 
        `SocialNetworkDB`.`PostTable`.`UserID` AS `UserID`,
        `SocialNetworkDB`.`PostTable`.`PostID` AS `PostID`,
        `SocialNetworkDB`.`PostTable`.`Text` AS `Text`,
        `SocialNetworkDB`.`PostTable`.`Date` AS `Date`,
        `SocialNetworkDB`.`PostTable`.`is_retweet` AS `is_retweet`,
        `SocialNetworkDB`.`PostTable`.`is_reply` AS `is_reply`,
        `SocialNetworkDB`.`PostTable`.`Original_PostID` AS `Original_PostID`,
        `SocialNetworkDB`.`PostTable`.`Original_Post_UserID` AS `Original_Post_UserID`,
        `SocialNetworkDB`.`PostTable`.`NumberOfLikes` AS `NumberOfLikes`,
        `SocialNetworkDB`.`PostTable`.`NumberOfReposts` AS `NumberOfReposts`,
        `X`.`First_Name` AS `First_Name`,
        `X`.`Last_Name` AS `Last_Name`,
        `X`.`CreationDate` AS `CreationDate`,
        `X`.`BirthDay` AS `BirthDay`,
        `X`.`BirthMonth` AS `BirthMonth`,
        `X`.`BirthYear` AS `BirthYear`,
        `X`.`Gender` AS `Gender`,
        `X`.`Description` AS `Description`,
        `X`.`NumberOfFollowers` AS `NumberOfFollowers`,
        `X`.`Handle` AS `Handle`
    FROM
        (`SocialNetworkDB`.`PostTable`
        JOIN (SELECT 
            `SocialNetworkDB`.`PersonTable`.`UserID` AS `UserID`,
                `SocialNetworkDB`.`PersonTable`.`First_Name` AS `First_Name`,
                `SocialNetworkDB`.`PersonTable`.`Last_Name` AS `Last_Name`,
                `SocialNetworkDB`.`PersonTable`.`CreationDate` AS `CreationDate`,
                `SocialNetworkDB`.`PersonTable`.`BirthDay` AS `BirthDay`,
                `SocialNetworkDB`.`PersonTable`.`BirthMonth` AS `BirthMonth`,
                `SocialNetworkDB`.`PersonTable`.`BirthYear` AS `BirthYear`,
                `SocialNetworkDB`.`PersonTable`.`Gender` AS `Gender`,
                `SocialNetworkDB`.`PersonTable`.`Description` AS `Description`,
                `SocialNetworkDB`.`PersonTable`.`NumberOfFollowers` AS `NumberOfFollowers`,
                `SocialNetworkDB`.`PersonHandleTable`.`Handle` AS `Handle`
        FROM
            (`SocialNetworkDB`.`PersonTable`
        JOIN `SocialNetworkDB`.`PersonHandleTable` ON ((`SocialNetworkDB`.`PersonTable`.`UserID` = `SocialNetworkDB`.`PersonHandleTable`.`UserID`)))) `X` ON ((`SocialNetworkDB`.`PostTable`.`UserID` = `X`.`UserID`)))
    GROUP BY `SocialNetworkDB`.`PostTable`.`PostID`