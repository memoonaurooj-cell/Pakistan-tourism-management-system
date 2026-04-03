CREATE DATABASE PTMS1;
GO

USE PTMS1;
GO
CREATE TABLE Tourists (
    TouristID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    ContactInfo VARCHAR(100) NOT NULL,
    Nationality VARCHAR(50) NOT NULL
);

CREATE TABLE TouristPackages (
    PackageID INT NOT NULL,
    PackageName VARCHAR(100) NOT NULL,
    Destination VARCHAR(100) NOT NULL,
    Price DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (PackageID, Destination)
);

CREATE TABLE Bookings (
    BookingID INT PRIMARY KEY,
    TouristID INT NOT NULL,
    PackageID INT NOT NULL,
    Destination VARCHAR(100) NOT NULL,
    TransportID INT NULL,
    BookingDate DATE NOT NULL,
    FOREIGN KEY (TouristID) REFERENCES Tourists(TouristID),
    FOREIGN KEY (PackageID, Destination) REFERENCES TouristPackages(PackageID, Destination)
);

CREATE TABLE PackagePricing (
    PackageID INT NOT NULL,
    Destination VARCHAR(100) NOT NULL,
    TotalAmount DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (PackageID, Destination),
    FOREIGN KEY (PackageID, Destination) REFERENCES TouristPackages(PackageID, Destination)
);

CREATE TABLE Destinations (
    DestinationID INT PRIMARY KEY,
    DestinationName VARCHAR(100) NOT NULL,
    Region VARCHAR(50) NOT NULL,
    TouristSpots VARCHAR(50) NOT NULL
);

CREATE TABLE Guides (
    GuideID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Experience VARCHAR(50) NOT NULL,
    Language VARCHAR(50) NOT NULL
);

CREATE TABLE GuideDestinations (
    DestinationID INT NOT NULL,
    GuideID INT NOT NULL,
    PRIMARY KEY (DestinationID, GuideID),
    FOREIGN KEY (DestinationID) REFERENCES Destinations(DestinationID),
    FOREIGN KEY (GuideID) REFERENCES Guides(GuideID)
);

CREATE TABLE Accommodations (
    AccommodationID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Location VARCHAR(100) NOT NULL,
    CostPerNight DECIMAL(10, 2) NOT NULL
);

CREATE TABLE TouristFeedback (
    FeedbackID INT PRIMARY KEY,
    TouristID INT NOT NULL,
    BookingID INT NOT NULL,
    FeedbackText VARCHAR(MAX) NOT NULL,
    FOREIGN KEY (TouristID) REFERENCES Tourists(TouristID),
    FOREIGN KEY (BookingID) REFERENCES Bookings(BookingID)
);

CREATE TABLE Transportation (
    TransportID INT PRIMARY KEY,
    Type VARCHAR(50) NOT NULL,
    CompanyName VARCHAR(100) NOT NULL,
    Cost DECIMAL(10, 2) NOT NULL
);

CREATE TABLE TouristPayments (
    PaymentID INT PRIMARY KEY,
    TouristID INT NOT NULL,
    BookingID INT NOT NULL,
    PaymentDate DATE NOT NULL,
    Amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (TouristID) REFERENCES Tourists(TouristID),
    FOREIGN KEY (BookingID) REFERENCES Bookings(BookingID)
);

CREATE TABLE CulturalEvents (
    EventID INT PRIMARY KEY,
    EventName VARCHAR(100) NOT NULL,
    Location VARCHAR(100) NOT NULL
);

CREATE TABLE EventCosts (
    EventID INT PRIMARY KEY,
    Cost DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (EventID) REFERENCES CulturalEvents(EventID)
);

CREATE TABLE EmergencyContacts (
    ContactID INT PRIMARY KEY,
    DestinationID INT NOT NULL,
    Phone VARCHAR(15) NOT NULL,
    FOREIGN KEY (DestinationID) REFERENCES Destinations(DestinationID)
);

CREATE TABLE ContactNames (
    DestinationID INT PRIMARY KEY,
    ContactName VARCHAR(100) NOT NULL,
    FOREIGN KEY (DestinationID) REFERENCES Destinations(DestinationID)
);

CREATE TABLE TouristGroups (
    GroupID INT PRIMARY KEY,
    TouristID INT NOT NULL,
    GroupName VARCHAR(100) NOT NULL,
    FOREIGN KEY (TouristID) REFERENCES Tourists(TouristID)
);

CREATE TABLE RoomBookings (
    RoomBookingID INT PRIMARY KEY,
    AccommodationID INT NOT NULL,
    TouristID INT NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    FOREIGN KEY (AccommodationID) REFERENCES Accommodations(AccommodationID),
    FOREIGN KEY (TouristID) REFERENCES Tourists(TouristID)
);
GO

-- ===============================
-- Insert Sample Data
-- ===============================
INSERT INTO Tourists VALUES
(1,'Ali Khan','ali.khan@example.com','Pakistani'),
(2,'John Smith','john.smith@example.com','British'),
(3,'Maria Lopez','maria.lopez@example.com','Spanish');

INSERT INTO TouristPackages VALUES
(1,'Northern Adventure','Hunza',20000),
(2,'Cultural Tour','Lahore',15000),
(3,'Beach Vacation','Karachi',18000);

INSERT INTO Bookings VALUES
(1,1,1,'Hunza',1,'2025-01-01'),
(2,2,2,'Lahore',2,'2025-01-05'),
(3,3,3,'Karachi',3,'2025-01-10');

INSERT INTO PackagePricing VALUES
(1,'Hunza',25000),
(2,'Lahore',17000),
(3,'Karachi',20000);

INSERT INTO Destinations VALUES
(1,'Hunza','Northern Pakistan','Mountains'),
(2,'Lahore','Punjab','Historical Sites'),
(3,'Karachi','Sindh','Beaches');

INSERT INTO Guides VALUES
(1,'Ahmed Ali','5 Years','Urdu'),
(2,'James Brown','3 Years','English'),
(3,'Sofia Garcia','7 Years','Spanish');

INSERT INTO GuideDestinations VALUES
(1,1),
(2,2),
(3,3);

INSERT INTO Accommodations VALUES
(1,'Hunza Hotel','Hunza',5000),
(2,'Lahore Inn','Lahore',3000),
(3,'Beach Resort','Karachi',4000);

INSERT INTO TouristFeedback VALUES
(1,1,1,'Amazing experience in Hunza!'),
(2,2,2,'Loved the cultural tour in Lahore.'),
(3,3,3,'Beach vacation was relaxing.');

INSERT INTO Transportation VALUES
(1,'Bus','Northern Travels',1500),
(2,'Train','Pakistan Railways',1000),
(3,'Plane','PIA',8000);

INSERT INTO TouristPayments VALUES
(1,1,1,'2025-01-02',25000),
(2,2,2,'2025-01-06',17000),
(3,3,3,'2025-01-11',20000);

INSERT INTO CulturalEvents VALUES
(1,'Music Festival','Lahore'),
(2,'Art Exhibition','Karachi'),
(3,'Food Carnival','Hunza');

INSERT INTO EventCosts VALUES
(1,5000),(2,4000),(3,3000);

INSERT INTO EmergencyContacts VALUES
(1,1,'0345-1234567'),
(2,2,'0300-9876543'),
(3,3,'0321-5678901');

INSERT INTO ContactNames VALUES
(1,'Zahid Ali'),
(2,'Ayesha Khan'),
(3,'Bilal Ahmed');

INSERT INTO TouristGroups VALUES
(1,1,'Northern Explorers'),
(2,2,'Cultural Enthusiasts'),
(3,3,'Beach Lovers');

INSERT INTO RoomBookings VALUES
(1,1,1,'2025-01-01','2025-01-03'),
(2,2,2,'2025-01-05','2025-01-07'),
(3,3,3,'2025-01-10','2025-01-12');
GO

-- ===============================
-- Create Full Tourism View
-- ===============================
CREATE VIEW FullTourismView AS
SELECT  
    t.TouristID,  
    t.Name AS TouristName,  
    t.ContactInfo,  
    t.Nationality,  
    tp.PackageName,  
    tp.Destination,  
    tp.Price AS PackagePrice,  
    b.BookingDate,  
    p.TotalAmount AS PackageTotalAmount,  
    d.DestinationName,  
    d.Region,  
    d.TouristSpots,  
    a.Name AS AccommodationName,  
    a.Location AS AccommodationLocation,  
    a.CostPerNight,  
    g.Name AS GuideName,  
    g.Experience AS GuideExperience,  
    g.Language AS GuideLanguage,  
    tf.FeedbackText AS TouristFeedback,  
    tr.Type AS TransportType,  
    tr.CompanyName AS TransportCompany,  
    tr.Cost AS TransportCost,  
    pmt.PaymentDate,  
    pmt.Amount AS PaymentAmount,  
    ce.EventName AS CulturalEventName,  
    ec.Cost AS EventCost,  
    em.Phone AS EmergencyContactPhone,  
    cn.ContactName AS EmergencyContactName,  
    tg.GroupName AS TouristGroupName,  
    rb.StartDate AS RoomBookingStart,  
    rb.EndDate AS RoomBookingEnd
FROM Tourists t
JOIN Bookings b ON t.TouristID = b.TouristID
JOIN TouristPackages tp ON b.PackageID = tp.PackageID AND b.Destination = tp.Destination
JOIN PackagePricing p ON tp.PackageID = p.PackageID AND tp.Destination = p.Destination
JOIN Destinations d ON tp.Destination = d.DestinationName
LEFT JOIN Accommodations a ON d.DestinationName = a.Location
LEFT JOIN GuideDestinations gd ON d.DestinationID = gd.DestinationID
LEFT JOIN Guides g ON gd.GuideID = g.GuideID
LEFT JOIN TouristFeedback tf ON b.BookingID = tf.BookingID
LEFT JOIN Transportation tr ON b.TransportID = tr.TransportID
LEFT JOIN TouristPayments pmt ON b.BookingID = pmt.BookingID
LEFT JOIN CulturalEvents ce ON ce.Location = d.DestinationName
LEFT JOIN EventCosts ec ON ce.EventID = ec.EventID
LEFT JOIN EmergencyContacts em ON d.DestinationID = em.DestinationID
LEFT JOIN ContactNames cn ON d.DestinationID = cn.DestinationID
LEFT JOIN TouristGroups tg ON t.TouristID = tg.TouristID
LEFT JOIN RoomBookings rb ON t.TouristID = rb.TouristID;
GO

-- Query the view
SELECT * FROM FullTourismView;
