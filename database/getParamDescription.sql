USE [LocalGovOp]
GO
/****** Object:  StoredProcedure [dbo].[GetParamDescription]    Script Date: 8/19/2024 9:01:50 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROCEDURE [dbo].[GetParamDescription]
    @NoticeId NVARCHAR(50), 
    @Param NVARCHAR(256)
AS 
BEGIN 
SET NOCOUNT ON; 
	IF @NoticeId IS NULL
		BEGIN
			RAISERROR('NoticeId cannot be NULL', 16, 1)
			RETURN
		END

	IF @Param IS NULL 
		BEGIN 
			RAISERROR('Param cannot be NULL', 16, 1)
			RETURN
		END

	--Get values 
	DECLARE @sql NVARCHAR(MAX) 
	SET @sql = 'SELECT ' + @Param + ' FROM SamInternalId WHERE NoticeId = @NoticeId'
	EXEC sp_executesql @sql, N'@NoticeId NVARCHAR(50)', @NoticeId

	--Get Description
	SET @sql = 'SELECT Description FROM SamInternalIdDescriptions WHERE NoticeId = @NoticeId AND DescriptionParam = @Param'
	EXEC sp_executesql @sql, N'@NoticeId NVARCHAR(50), @Param NVARCHAR(256)', @NoticeId, @Param

END 
