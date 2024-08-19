USE [LocalGovOp]
GO
/****** Object:  StoredProcedure [dbo].[InsertSearchData]    Script Date: 8/19/2024 9:00:49 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER PROCEDURE [dbo].[InsertSearchData]
    @NoticeId NVARCHAR(50), 
    @Param NVARCHAR(256),
    @Value NVARCHAR(256), 
	@Description NVARCHAR(MAX)
AS 
BEGIN 
    SET NOCOUNT ON;

    -- Check if NoticeId is NULL
    IF @NoticeId IS NULL
    BEGIN
        RAISERROR('NoticeId cannot be NULL', 16, 1)
        RETURN
    END

    -- Add NoticeId if not present
    IF (SELECT NoticeId FROM SamInternalId WHERE NoticeId = @NoticeId) IS NULL
    BEGIN
        INSERT INTO SamInternalId (NoticeId) VALUES (@NoticeId)
    END

    -- Check table for column
    DECLARE @Temp NVARCHAR(256)
    SET @Temp = CASE 
            WHEN @Param = 'NaicsCode' THEN (SELECT NaicsCode FROM SamInternalId WHERE NoticeId = @NoticeId)
            WHEN @Param = 'PSC' THEN (SELECT PSC FROM SamInternalId WHERE NoticeId = @NoticeId) 
            WHEN @Param = 'SocioEconomicProgram' THEN (SELECT SocioEconomicProgram FROM SamInternalId WHERE NoticeId = @NoticeId)
            WHEN @Param = 'PersonnelSecurityClearance' THEN (SELECT PersonnelSecurityClearance FROM SamInternalId WHERE NoticeId = @NoticeId)
            WHEN @Param = 'FacilitySecurityClearance' THEN (SELECT FacilitySecurityClearance FROM SamInternalId WHERE NoticeId = @NoticeId)
            WHEN @Param = 'PopStreetAddress' THEN (SELECT PopStreetAddress FROM SamInternalId WHERE NoticeId = @NoticeId) 
            WHEN @Param = 'PopCity' THEN (SELECT PopCity FROM SamInternalId WHERE NoticeId = @NoticeId)
            WHEN @Param = 'PopState' THEN (SELECT PopState FROM SamInternalId WHERE NoticeId = @NoticeId) 
            WHEN @Param = 'PopZip' THEN (SELECT PopZip FROM SamInternalId WHERE NoticeId = @NoticeId)
            WHEN @Param = 'PopCountry' THEN (SELECT PopCountry FROM SamInternalId WHERE NoticeId = @NoticeId)
            WHEN @Param = 'State' THEN (SELECT State FROM SamInternalId WHERE NoticeId = @NoticeId)
            WHEN @Param = 'City' THEN (SELECT City FROM SamInternalId WHERE NoticeId = @NoticeId)
            WHEN @Param = 'ZipCode' THEN (SELECT ZipCode FROM SamInternalId WHERE NoticeId = @NoticeId) 
            WHEN @Param = 'CountryCode' THEN (SELECT CountryCode FROM SamInternalId WHERE NoticeId = @NoticeId)
            WHEN @Param = 'AwardNumber' THEN (SELECT AwardNumber FROM SamInternalId WHERE NoticeId = @NoticeId)
            WHEN @Param = 'AwardDate' THEN (SELECT AwardDate FROM SamInternalId WHERE NoticeId = @NoticeId)
            WHEN @Param = 'AwardMoney' THEN (SELECT AwardMoney FROM SamInternalId WHERE NoticeId = @NoticeId) 
            WHEN @Param = 'Awardee' THEN (SELECT Awardee FROM SamInternalId WHERE NoticeId = @NoticeId)
            WHEN @Param = 'PrimaryContactTitle' THEN (SELECT PrimaryContactTitle FROM SamInternalId WHERE NoticeId = @NoticeId)
            WHEN @Param = 'PrimaryContactFullname' THEN (SELECT PrimaryContactFullname FROM SamInternalId WHERE NoticeId = @NoticeId)
            WHEN @Param = 'PrimaryContactEmail' THEN (SELECT PrimaryContactEmail FROM SamInternalId WHERE NoticeId = @NoticeId)
            WHEN @Param = 'PrimaryContactPhone' THEN (SELECT PrimaryContactPhone FROM SamInternalId WHERE NoticeId = @NoticeId)
            WHEN @Param = 'PrimaryContactFax' THEN (SELECT PrimaryContactFax FROM SamInternalId WHERE NoticeId = @NoticeId)
            WHEN @Param = 'SecondaryContactTitle' THEN (SELECT SecondaryContactTitle FROM SamInternalId WHERE NoticeId = @NoticeId)
            WHEN @Param = 'SecondaryContactFullname' THEN (SELECT SecondaryContactFullname FROM SamInternalId WHERE NoticeId = @NoticeId)
            WHEN @Param = 'SecondaryContactEmail' THEN (SELECT SecondaryContactEmail FROM SamInternalId WHERE NoticeId = @NoticeId)
            WHEN @Param = 'SecondaryContactPhone' THEN (SELECT SecondaryContactPhone FROM SamInternalId WHERE NoticeId = @NoticeId)
            WHEN @Param = 'SecondaryContactFax' THEN (SELECT SecondaryContactFax FROM SamInternalId WHERE NoticeId = @NoticeId)
        END; 

    -- Add value into correct column if it is NULL
	IF @Temp LIKE '%@Value%'
		BEGIN 
			RETURN 
		END;

    IF @Temp IS NULL 
		BEGIN 
			--Insert to SamInternalId
			DECLARE @sql NVARCHAR(MAX)
			SET @sql = 'UPDATE SamInternalId SET ' + @Param + ' = @Value WHERE NoticeId = @NoticeId'
			EXEC sp_executesql @sql, N'@Value NVARCHAR(256), @NoticeId NVARCHAR(50)', @Value, @NoticeId

			--Insert to SamInteralIdDescription
			SET @sql = 'INSERT INTO SamInternalIdDescriptions (NoticeId, DescriptionParam, Description) VALUES (@NoticeId, @Param, @Description)'
			EXEC sp_executesql @sql, N'@NoticeId NVARCHAR(50), @Param NVARCHAR(256), @Description NVARCHAR(MAX)', @NoticeId, @Param, @Description
		END;
	ELSE
		BEGIN 
			DECLARE @Concat NVARCHAR(MAX) 
			SET @Concat = CONCAT(@Value, '~', @Temp)
			PRINT @Concat;
			DECLARE @sql2 NVARCHAR(MAX) 
			SET @sql2 = 'UPDATE SamInternalId SET ' + @Param + ' = @Concat WHERE NoticeId = @NoticeId'
			EXEC sp_executesql @sql2, N'@NoticeId NVARCHAR(50), @Concat NVARCHAR(MAX)', @NoticeId, @Concat

			--Insert to SamInteralIdDescription
			SET @sql2 = 'INSERT INTO SamInternalIdDescriptions (NoticeId, DescriptionParam, Description) VALUES (@NoticeId, @Param, @Description)'
			EXEC sp_executesql @sql, N'@NoticeId NVARCHAR(50), @Param NVARCHAR(256), @Description NVARCHAR(MAX)', @NoticeId, @Param, @Description
		END;
END  
