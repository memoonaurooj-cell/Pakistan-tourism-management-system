CREATE DATABASE PTMS1_Denorm;
GO

USE PTMS1_Denorm;
GO

/* ===============================
   DENORMALIZED TABLE 1: TOURIST INFO
================================ */
CREATE TABLE TouristInfo (
    TouristID INT PRIMARY KEY,
    TouristName VARCHAR(100),
    ContactInfo VARCHAR(100),
    Nationality VARCHAR(50),
    
    BookingID INT,
    BookingDate DATE,
    
    PackageID INT,
    PackageName VARCHAR(100),
    Destination VARCHAR(100),
    PackagePrice DECIMAL(10,2),
    TotalAmount DECIMAL(10,2),
    
    TransportID INT,
    TransportType VARCHAR(50),
    TransportCompany VARCHAR(100),
    TransportCost DECIMAL(10,2),
    
    PaymentDate DATE,
    PaymentAmount DECIMAL(10,2)
);
GO

/* ===============================
   DENORMALIZED TABLE 2: DESTINATION INFO
================================ */
CREATE TABLE DestinationInfo (
    DestinationID INT PRIMARY KEY,
    DestinationName VARCHAR(100),
    Region VARCHAR(50),
    TouristSpots VARCHAR(50),
    
    AccommodationName VARCHAR(100),
    AccommodationLocation VARCHAR(100),
    AccommodationCostPerNight DECIMAL(10,2),
    
    GuideName VARCHAR(100),
    GuideExperience VARCHAR(50),
    GuideLanguage VARCHAR(50),
    
    EventName VARCHAR(100),
    EventCost DECIMAL(10,2)
);
GO

/* ===============================
   DENORMALIZED TABLE 3: FEEDBACK INFO
================================ */
CREATE TABLE FeedbackInfo (
    FeedbackID INT PRIMARY KEY,
    TouristID INT,
    BookingID INT,
    FeedbackText VARCHAR(MAX)
);
GO

/* ===============================
   INSERT SAMPLE DATA
================================ */
INSERT INTO TouristInfo VALUES
(1, 'Ali Khan', 'ali.khan@example.com', 'Pakistani',
 1, '2025-01-01', 1, 'Northern Adventure', 'Hunza', 20000, 25000,
 1, 'Bus', 'Northern Travels', 1500, '2025-01-02', 25000),
(2, 'John Smith', 'john.smith@example.com', 'British',
 2, '2025-01-05', 2, 'Cultural Tour', 'Lahore', 15000, 17000,
 2, 'Train', 'Pakistan Railways', 1000, '2025-01-06', 17000),
(3, 'Maria Lopez', 'maria.lopez@example.com', 'Spanish',
 3, '2025-01-10', 3, 'Beach Vacation', 'Karachi', 18000, 20000,
 3, 'Plane', 'PIA', 8000, '2025-01-11', 20000);

INSERT INTO DestinationInfo VALUES
(1, 'Hunza', 'Northern Pakistan', 'Mountains',
 'Hunza Inn', 'Hunza', 5000,
 'Ahmed Khan', '5 years', 'English',
 'Food Carnival', 3000),
(2, 'Lahore', 'Punjab', 'Historical Sites',
 'Lahore Hotel', 'Lahore', 4000,
 'Sara Ahmed', '3 years', 'English',
 'Music Festival', 5000),
(3, 'Karachi', 'Sindh', 'Beaches',
 'Karachi Resort', 'Karachi', 6000,
 'Ali Raza', '7 years', 'Spanish',
 'Art Exhibition', 4000);

INSERT INTO FeedbackInfo VALUES
(1, 1, 1, 'Amazing experience!'),
(2, 2, 2, 'Very enjoyable.'),
(3, 3, 3, 'Loved the beaches!');
GO

/* ===============================
   TEST
================================ */
SELECT * FROM TouristInfo;
SELECT * FROM DestinationInfo;
SELECT * FROM FeedbackInfo;

