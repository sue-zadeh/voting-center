

-- drop the User table
-- DROP TABLE IF EXISTS User;
-- DROP TABLE IF EXISTS Vote;
-- DROP TABLE IF EXISTS Competitor;
-- DROP TABLE IF EXISTS Competition;
-- DROP TABLE IF EXISTS Announcement;
--UPDATE Competitor SET Description = '';

-- DROP TABLE IF EXISTS User;

-- DELETE FROM Competitor 
-- WHERE Name NOT IN (
--     'Milford Track',
--     'Routeburn Track',
--     'Tongariro Alpine Crossing',
--     'Abel Tasman Coast Track',
--     'Heaphy Track',
--     'Kepler Track',
--     'Rakiura Track',
--     'Lake Waikaremoana Track',
--     'Whanganui Journey',
--     'Pinnacles Track'
-- );

-- User Table
CREATE TABLE IF NOT EXISTS User (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(255) UNIQUE NOT NULL,
    FirstName VARCHAR(255) NOT NULL,
    LastName VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Location VARCHAR(255),
    Image VARCHAR(255), -- Storing the file path or URL of the image
    Role ENUM('voter', 'scrutineer', 'admin') NOT NULL DEFAULT 'voter',
    Status ENUM('active', 'inactive') NOT NULL DEFAULT 'active'
);

-- Announcement Table
CREATE TABLE IF NOT EXISTS Announcement (
    AnnouncementID INT AUTO_INCREMENT PRIMARY KEY,
    CreatedBy INT NOT NULL,
    CreatedAt DATETIME NOT NULL,
    StartDate DATE NOT NULL,
    FinishDate DATE NOT NULL,
    Content TEXT NOT NULL,
    FOREIGN KEY (CreatedBy) REFERENCES User(UserID)
);

-- Competition Table
CREATE TABLE IF NOT EXISTS Competition (
    CompetitionID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Description TEXT,
    StartDate DATE NOT NULL,
    FinishDate DATE NOT NULL,
    CreatedBy INT NOT NULL,
    ApprovedBy INT,
    Status VARCHAR(50) NOT NULL,
    FOREIGN KEY (CreatedBy) REFERENCES User(UserID),
    FOREIGN KEY (ApprovedBy) REFERENCES User(UserID)
);

-- Competitor Table
CREATE TABLE IF NOT EXISTS Competitor (
    CompetitorID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Image VARCHAR(255), -- Storing the file path or URL of the image
    Description TEXT,
    CreatedBy INT NOT NULL,
    FOREIGN KEY (CreatedBy) REFERENCES User(UserID)
);

-- Junction Table for Competition and Competitor
CREATE TABLE IF NOT EXISTS CompetitionCompetitor (
    CompetitionID INT NOT NULL,
    CompetitorID INT NOT NULL,
    PRIMARY KEY (CompetitionID, CompetitorID),
    FOREIGN KEY (CompetitionID) REFERENCES Competition(CompetitionID) ON DELETE CASCADE,
    FOREIGN KEY (CompetitorID) REFERENCES Competitor(CompetitorID) ON DELETE CASCADE
);

-- Vote Table
CREATE TABLE IF NOT EXISTS Vote (
    VoteID INT AUTO_INCREMENT PRIMARY KEY,
    IPAddress VARCHAR(50) NOT NULL,
    CompetitionID INT NOT NULL,
    CompetitorID INT NOT NULL,
    Status VARCHAR(50) NOT NULL,
    VotedBy INT NOT NULL,
    VotedAt DATETIME NOT NULL,
    FOREIGN KEY (CompetitionID) REFERENCES Competition(CompetitionID),
    FOREIGN KEY (CompetitorID) REFERENCES Competitor(CompetitorID),
    FOREIGN KEY (VotedBy) REFERENCES User(UserID)
);