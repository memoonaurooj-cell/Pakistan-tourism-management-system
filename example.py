import tkinter as tk
from tkinter import messagebox, ttk
import pyodbc

# ---------------- DATABASE CONNECTION ----------------
def get_connection():
    try:
        conn = pyodbc.connect(
            "DRIVER={SQL Server};"
            "SERVER=DESKTOP-AQ913RF\SQLEXPRESS;"
            "DATABASE=PTMS1;"
            "Trusted_Connection=yes;"
        )
        return conn
    except pyodbc.Error as e:
        messagebox.showerror("Connection Error", f"Database connection failed: {str(e)}")
        return None

# ---------------- CHECK DATABASE STRUCTURE ----------------
def check_database_structure():
    try:
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            
            # Check what columns exist in Tourists table
            cursor.execute("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'Tourists'
            """)
            tourist_columns = [row[0] for row in cursor.fetchall()]
            print("Tourist table columns:", tourist_columns)
            
            # Check Bookings table
            cursor.execute("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'Bookings'
            """)
            booking_columns = [row[0] for row in cursor.fetchall()]
            print("Booking table columns:", booking_columns)
            
            # Check Packages table
            cursor.execute("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'Packages'
            """)
            package_columns = [row[0] for row in cursor.fetchall()]
            print("Package table columns:", package_columns)
            
            conn.close()
            return tourist_columns, booking_columns, package_columns
    except Exception as e:
        print(f"Error checking database structure: {str(e)}")
        return None, None, None

# ---------------- CREATE MISSING TABLES/COLUMNS ----------------
def update_database_structure():
    try:
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            
            # Check and create Tourists table if needed
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Tourists' AND xtype='U')
                CREATE TABLE Tourists (
                    TouristID INT IDENTITY(1,1) PRIMARY KEY,
                    Name VARCHAR(100) NOT NULL,
                    ContactInfo VARCHAR(20) NOT NULL,
                    Nationality VARCHAR(50) NOT NULL
                )
            """)
            
            # Add missing columns to Tourists if they don't exist
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS 
                              WHERE TABLE_NAME = 'Tourists' AND COLUMN_NAME = 'Email')
                ALTER TABLE Tourists ADD Email VARCHAR(100)
            """)
            
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS 
                              WHERE TABLE_NAME = 'Tourists' AND COLUMN_NAME = 'DateOfBirth')
                ALTER TABLE Tourists ADD DateOfBirth DATE
            """)
            
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS 
                              WHERE TABLE_NAME = 'Tourists' AND COLUMN_NAME = 'Gender')
                ALTER TABLE Tourists ADD Gender VARCHAR(10)
            """)
            
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS 
                              WHERE TABLE_NAME = 'Tourists' AND COLUMN_NAME = 'RegistrationDate')
                ALTER TABLE Tourists ADD RegistrationDate DATE DEFAULT GETDATE()
            """)
            
            # Check and create Packages table if needed
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Packages' AND xtype='U')
                CREATE TABLE Packages (
                    PackageID INT IDENTITY(1,1) PRIMARY KEY,
                    PackageName VARCHAR(100) NOT NULL,
                    Description TEXT,
                    Destination VARCHAR(100) NOT NULL,
                    Duration INT,
                    Price DECIMAL(10,2) NOT NULL,
                    AvailableSeats INT
                )
            """)
            
            # Check and create Bookings table if needed
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Bookings' AND xtype='U')
                CREATE TABLE Bookings (
                    BookingID INT IDENTITY(1,1) PRIMARY KEY,
                    TouristID INT NOT NULL,
                    PackageID INT NOT NULL,
                    Destination VARCHAR(100) NOT NULL,
                    BookingDate DATE DEFAULT GETDATE()
                )
            """)
            
            # Add missing columns to Bookings table
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS 
                              WHERE TABLE_NAME = 'Bookings' AND COLUMN_NAME = 'TravelDate')
                ALTER TABLE Bookings ADD TravelDate DATE
            """)
            
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS 
                              WHERE TABLE_NAME = 'Bookings' AND COLUMN_NAME = 'NumberOfPeople')
                ALTER TABLE Bookings ADD NumberOfPeople INT DEFAULT 1
            """)
            
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS 
                              WHERE TABLE_NAME = 'Bookings' AND COLUMN_NAME = 'TotalAmount')
                ALTER TABLE Bookings ADD TotalAmount DECIMAL(10,2)
            """)
            
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS 
                              WHERE TABLE_NAME = 'Bookings' AND COLUMN_NAME = 'PaymentStatus')
                ALTER TABLE Bookings ADD PaymentStatus VARCHAR(20) DEFAULT 'Pending'
            """)
            
            # Add sample packages if table is empty
            cursor.execute("SELECT COUNT(*) FROM Packages")
            if cursor.fetchone()[0] == 0:
                sample_packages = [
                    ('Northern Areas Tour', 'Explore Gilgit, Hunza, Skardu', 'Northern Pakistan', 7, 50000.00, 20),
                    ('Cultural Punjab', 'Historical sites of Lahore & Multan', 'Punjab', 5, 35000.00, 15),
                    ('Coastal Sindh', 'Karachi, Thatta, Makli', 'Sindh', 4, 25000.00, 25),
                    ('Mountain Adventure', 'K2 Base Camp Trekking', 'Karakoram', 14, 120000.00, 10)
                ]
                cursor.executemany(
                    "INSERT INTO Packages (PackageName, Description, Destination, Duration, Price, AvailableSeats) VALUES (?, ?, ?, ?, ?, ?)",
                    sample_packages
                )
            
            conn.commit()
            conn.close()
            print("Database structure updated successfully")
    except Exception as e:
        print(f"Error updating database structure: {str(e)}")

# ---------------- VALIDATION FUNCTIONS ----------------
def validate_date(date_str):
    try:
        from datetime import datetime
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_phone(phone):
    return phone.isdigit() and len(phone) >= 10

# ---------------- TOURIST MANAGEMENT ----------------
def add_tourist():
    name = name_entry.get().strip()
    contact = contact_entry.get().strip()
    nationality = nationality_entry.get().strip()
    email = email_entry.get().strip()
    dob = dob_entry.get().strip()
    gender = gender_var.get()

    if not all([name, contact, nationality]):
        messagebox.showerror("Error", "Name, Contact, and Nationality are required")
        return
    
    if not validate_phone(contact):
        messagebox.showerror("Error", "Contact must be at least 10 digits")
        return
    
    if dob and not validate_date(dob):
        messagebox.showerror("Error", "Date of Birth must be in YYYY-MM-DD format")
        return

    try:
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            
            # Check which columns exist in the table
            cursor.execute("""
                INSERT INTO Tourists (Name, ContactInfo, Nationality, Email, DateOfBirth, Gender) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, contact, nationality, 
                  email if email else None, 
                  dob if dob else None, 
                  gender if gender else None))
            
            conn.commit()
            
            # Get the auto-generated ID
            cursor.execute("SELECT SCOPE_IDENTITY()")
            tourist_id = cursor.fetchone()[0]
            
            conn.close()
            messagebox.showinfo("Success", f"Tourist added successfully!\nTourist ID: {tourist_id}")
            clear_tourist_fields()
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred: {str(e)}")

def view_tourists():
    try:
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            
            # Try to get all columns, but handle missing ones
            try:
                cursor.execute("""
                    SELECT TouristID, Name, ContactInfo, Nationality, 
                           ISNULL(Email, 'N/A'), 
                           ISNULL(CONVERT(VARCHAR(10), DateOfBirth, 120), 'N/A'),
                           ISNULL(Gender, 'N/A'),
                           ISNULL(CONVERT(VARCHAR(10), RegistrationDate, 120), 'N/A')
                    FROM Tourists 
                    ORDER BY TouristID
                """)
                rows = cursor.fetchall()
                columns = ["ID", "Name", "Contact", "Nationality", "Email", "DOB", "Gender", "Reg Date"]
            except:
                # Fall back to basic columns if extended ones don't exist
                cursor.execute("SELECT TouristID, Name, ContactInfo, Nationality FROM Tourists ORDER BY TouristID")
                rows = cursor.fetchall()
                columns = ["ID", "Name", "Contact", "Nationality"]
            
            conn.close()
            
            if not rows:
                messagebox.showinfo("No Data", "No tourists found in the database.")
                return
            
            # Create display window
            display_window = tk.Toplevel(root)
            display_window.title("Tourist Records")
            display_window.geometry("900x500")
            
            # Create frame for treeview
            tree_frame = tk.Frame(display_window)
            tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Create scrollbars
            vsb = ttk.Scrollbar(tree_frame, orient="vertical")
            vsb.pack(side="right", fill="y")
            
            hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
            hsb.pack(side="bottom", fill="x")
            
            # Create treeview
            tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                               yscrollcommand=vsb.set, xscrollcommand=hsb.set)
            
            # Configure scrollbars
            vsb.config(command=tree.yview)
            hsb.config(command=tree.xview)
            
            # Define headings
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100, minwidth=80)
            
            # Adjust column widths
            if "Name" in columns:
                tree.column("Name", width=120)
            if "Email" in columns:
                tree.column("Email", width=150)
            
            # Insert data
            for row in rows:
                tree.insert("", "end", values=row)
            
            tree.pack(fill="both", expand=True)
            
            # Add count label
            count_label = tk.Label(display_window, text=f"Total Tourists: {len(rows)}", 
                                   font=("Arial", 10, "bold"))
            count_label.pack(pady=5)
            
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load tourists: {str(e)}")

# ---------------- PACKAGE MANAGEMENT ----------------
def view_packages():
    try:
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT PackageID, PackageName, Destination, 
                       ISNULL(Duration, 'N/A'),
                       CONVERT(VARCHAR, ISNULL(Price, 0)) + ' Rs', 
                       ISNULL(AvailableSeats, 0),
                       ISNULL(Description, 'No description')
                FROM Packages 
                ORDER BY PackageID
            """)
            rows = cursor.fetchall()
            conn.close()
            
            if not rows:
                messagebox.showinfo("No Data", "No packages found in the database.")
                return
            
            # Create display window
            display_window = tk.Toplevel(root)
            display_window.title("Tour Packages")
            display_window.geometry("1000x400")
            
            # Create frame for treeview
            tree_frame = tk.Frame(display_window)
            tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Create scrollbars
            vsb = ttk.Scrollbar(tree_frame, orient="vertical")
            vsb.pack(side="right", fill="y")
            
            hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
            hsb.pack(side="bottom", fill="x")
            
            # Create treeview
            columns = ("ID", "Package Name", "Destination", "Duration", "Price", "Available Seats", "Description")
            tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                               yscrollcommand=vsb.set, xscrollcommand=hsb.set)
            
            # Configure scrollbars
            vsb.config(command=tree.yview)
            hsb.config(command=tree.xview)
            
            # Define headings
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100, minwidth=80)
            
            # Adjust column widths
            tree.column("Package Name", width=150)
            tree.column("Description", width=200)
            tree.column("Destination", width=120)
            
            # Insert data
            for row in rows:
                tree.insert("", "end", values=row)
            
            tree.pack(fill="both", expand=True)
            
            # Add count label
            count_label = tk.Label(display_window, text=f"Total Packages: {len(rows)}", 
                                   font=("Arial", 10, "bold"))
            count_label.pack(pady=5)
            
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load packages: {str(e)}")

# ---------------- BOOKING MANAGEMENT ----------------
def add_booking():
    tourist_id = b_tourist_id_entry.get().strip()
    package_id = b_package_id_entry.get().strip()
    travel_date = travel_date_entry.get().strip()
    num_people = num_people_entry.get().strip()

    if not all([tourist_id, package_id, travel_date, num_people]):
        messagebox.showerror("Error", "All fields are required")
        return
    
    try:
        tourist_id = int(tourist_id)
        package_id = int(package_id)
        num_people = int(num_people)
    except ValueError:
        messagebox.showerror("Error", "Tourist ID, Package ID, and Number of People must be valid numbers")
        return
    
    if num_people <= 0:
        messagebox.showerror("Error", "Number of people must be positive")
        return
    
    if not validate_date(travel_date):
        messagebox.showerror("Error", "Travel date must be in YYYY-MM-DD format")
        return

    try:
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            
            # Check if tourist exists
            cursor.execute("SELECT Name FROM Tourists WHERE TouristID = ?", (tourist_id,))
            tourist = cursor.fetchone()
            if not tourist:
                messagebox.showerror("Error", f"Tourist ID {tourist_id} does not exist")
                conn.close()
                return
            
            # Check if package exists and has enough seats
            cursor.execute("SELECT PackageName, Price, AvailableSeats FROM Packages WHERE PackageID = ?", (package_id,))
            package = cursor.fetchone()
            if not package:
                messagebox.showerror("Error", f"Package ID {package_id} does not exist")
                conn.close()
                return
            
            package_name, price, available_seats = package
            if num_people > available_seats:
                messagebox.showerror("Error", f"Only {available_seats} seats available for '{package_name}'")
                conn.close()
                return
            
            total_amount = price * num_people
            
            # Get destination from package
            cursor.execute("SELECT Destination FROM Packages WHERE PackageID = ?", (package_id,))
            destination = cursor.fetchone()[0]
            
            # Create booking (using the original structure)
            try:
                # Try with extended columns first
                cursor.execute("""
                    INSERT INTO Bookings (TouristID, PackageID, Destination, TravelDate, NumberOfPeople, TotalAmount) 
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (tourist_id, package_id, destination, travel_date, num_people, total_amount))
            except:
                # Fall back to basic insert
                cursor.execute("""
                    INSERT INTO Bookings (TouristID, PackageID, Destination, BookingDate) 
                    VALUES (?, ?, ?, GETDATE())
                """, (tourist_id, package_id, destination))
            
            # Update available seats
            cursor.execute("""
                UPDATE Packages 
                SET AvailableSeats = AvailableSeats - ? 
                WHERE PackageID = ?
            """, (num_people, package_id))
            
            conn.commit()
            
            # Get the booking ID
            cursor.execute("SELECT SCOPE_IDENTITY()")
            booking_id = cursor.fetchone()[0]
            
            conn.close()
            
            messagebox.showinfo("Success", 
                f"Booking created successfully!\n"
                f"Booking ID: {booking_id}\n"
                f"Tourist: {tourist[0]}\n"
                f"Package: {package_name}\n"
                f"Travel Date: {travel_date}\n"
                f"Total Amount: Rs. {total_amount:,.2f}")
            
            clear_booking_fields()
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred: {str(e)}")

def view_bookings():
    try:
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            
            # Try to get all booking columns
            try:
                cursor.execute("""
                    SELECT 
                        b.BookingID,
                        t.Name,
                        p.PackageName,
                        CONVERT(VARCHAR(10), b.BookingDate, 120),
                        b.Destination,
                        ISNULL(CONVERT(VARCHAR(10), b.TravelDate, 120), 'N/A'),
                        ISNULL(b.NumberOfPeople, 1),
                        ISNULL(CONVERT(VARCHAR, b.TotalAmount), 'N/A') + ' Rs',
                        ISNULL(b.PaymentStatus, 'Pending')
                    FROM Bookings b
                    JOIN Tourists t ON b.TouristID = t.TouristID
                    JOIN Packages p ON b.PackageID = p.PackageID
                    ORDER BY b.BookingDate DESC
                """)
                rows = cursor.fetchall()
                columns = ("Booking ID", "Tourist Name", "Package", "Booking Date", "Destination", 
                          "Travel Date", "People", "Total Amount", "Payment Status")
            except:
                # Fall back to basic booking info
                cursor.execute("""
                    SELECT 
                        b.BookingID,
                        t.Name,
                        p.PackageName,
                        CONVERT(VARCHAR(10), b.BookingDate, 120),
                        b.Destination
                    FROM Bookings b
                    JOIN Tourists t ON b.TouristID = t.TouristID
                    JOIN Packages p ON b.PackageID = p.PackageID
                    ORDER BY b.BookingDate DESC
                """)
                rows = cursor.fetchall()
                columns = ("Booking ID", "Tourist Name", "Package", "Booking Date", "Destination")
            
            conn.close()
            
            if not rows:
                messagebox.showinfo("No Data", "No bookings found in the database.")
                return
            
            # Create display window
            display_window = tk.Toplevel(root)
            display_window.title("Booking Records")
            display_window.geometry("1000x500")
            
            # Create frame for treeview
            tree_frame = tk.Frame(display_window)
            tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Create scrollbars
            vsb = ttk.Scrollbar(tree_frame, orient="vertical")
            vsb.pack(side="right", fill="y")
            
            hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
            hsb.pack(side="bottom", fill="x")
            
            # Create treeview
            tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                               yscrollcommand=vsb.set, xscrollcommand=hsb.set)
            
            # Configure scrollbars
            vsb.config(command=tree.yview)
            hsb.config(command=tree.xview)
            
            # Define headings
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100, minwidth=80)
            
            # Adjust column widths
            if "Tourist Name" in columns:
                tree.column("Tourist Name", width=120)
            if "Package" in columns:
                tree.column("Package", width=150)
            
            # Insert data
            for row in rows:
                tree.insert("", "end", values=row)
            
            tree.pack(fill="both", expand=True)
            
            # Add count label
            count_label = tk.Label(display_window, text=f"Total Bookings: {len(rows)}", 
                                   font=("Arial", 10, "bold"))
            count_label.pack(pady=5)
            
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load bookings: {str(e)}")

# ---------------- CLEAR FUNCTIONS ----------------
def clear_tourist_fields():
    if 'name_entry' in globals():
        name_entry.delete(0, tk.END)
        contact_entry.delete(0, tk.END)
        nationality_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        dob_entry.delete(0, tk.END)
        gender_var.set("")

def clear_booking_fields():
    if 'b_tourist_id_entry' in globals():
        b_tourist_id_entry.delete(0, tk.END)
        b_package_id_entry.delete(0, tk.END)
        travel_date_entry.delete(0, tk.END)
        num_people_entry.delete(0, tk.END)

# ---------------- SIMPLE GUI ----------------
def create_simple_gui():
    global root, name_entry, contact_entry, nationality_entry, email_entry, dob_entry, gender_var
    global b_tourist_id_entry, b_package_id_entry, travel_date_entry, num_people_entry
    
    root = tk.Tk()
    root.title("Pakistan Tourism Management System")
    root.geometry("1000x700")
    root.configure(bg="#f0f0f0")
    
    # Title
    title_frame = tk.Frame(root, bg="#2c3e50", height=80)
    title_frame.pack(fill="x")
    title_frame.pack_propagate(False)
    
    tk.Label(
        title_frame,
        text="Pakistan Tourism Management System",
        font=("Arial", 24, "bold"),
        fg="white",
        bg="#2c3e50"
    ).pack(pady=20)
    
    # Main notebook (tabs)
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Tab 1: Dashboard
    dashboard_tab = tk.Frame(notebook, bg="#f0f0f0")
    notebook.add(dashboard_tab, text="🏠 Dashboard")
    
    tk.Label(
        dashboard_tab,
        text="Welcome to PTMS",
        font=("Arial", 20, "bold"),
        bg="#f0f0f0",
        fg="#2c3e50"
    ).pack(pady=20)
    
    # Quick stats
    try:
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM Tourists")
            tourist_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM Bookings")
            booking_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM Packages")
            package_count = cursor.fetchone()[0]
            
            try:
                cursor.execute("SELECT ISNULL(SUM(TotalAmount), 0) FROM Bookings")
                revenue = cursor.fetchone()[0]
            except:
                revenue = 0
            
            conn.close()
            
            stats_frame = tk.Frame(dashboard_tab, bg="#f0f0f0")
            stats_frame.pack(pady=20)
            
            stats = [
                ("Total Tourists", tourist_count, "#3498db"),
                ("Total Bookings", booking_count, "#2ecc71"),
                ("Available Packages", package_count, "#e74c3c"),
                ("Total Revenue", f"Rs. {revenue:,.2f}", "#f39c12")
            ]
            
            for i, (title, value, color) in enumerate(stats):
                stat_frame = tk.Frame(stats_frame, bg=color, relief="raised", borderwidth=2)
                stat_frame.grid(row=i//2, column=i%2, padx=15, pady=15, ipadx=20, ipady=15)
                
                tk.Label(
                    stat_frame,
                    text=title,
                    font=("Arial", 12, "bold"),
                    bg=color,
                    fg="white"
                ).pack()
                
                tk.Label(
                    stat_frame,
                    text=str(value),
                    font=("Arial", 16, "bold"),
                    bg=color,
                    fg="white"
                ).pack(pady=5)
    except:
        pass
    
    # Tab 2: Tourist Management
    tourist_tab = tk.Frame(notebook, bg="#f0f0f0")
    notebook.add(tourist_tab, text="👥 Tourist Management")
    
    # Tourist form
    form_frame = tk.Frame(tourist_tab, bg="#f0f0f0")
    form_frame.pack(pady=20)
    
    # Create form fields (basic required ones first)
    basic_fields = [
        ("Name *:", "name_entry"),
        ("Contact Info *:", "contact_entry"),
        ("Nationality *:", "nationality_entry"),
    ]
    
    for i, (label, var_name) in enumerate(basic_fields):
        tk.Label(
            form_frame,
            text=label,
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#2c3e50"
        ).grid(row=i, column=0, sticky="w", pady=10, padx=(0, 10))
        
        entry = tk.Entry(form_frame, width=30, font=("Arial", 12))
        entry.grid(row=i, column=1, pady=10)
        
        # Assign to global variables
        if var_name == "name_entry":
            name_entry = entry
        elif var_name == "contact_entry":
            contact_entry = entry
        elif var_name == "nationality_entry":
            nationality_entry = entry
    
    # Optional fields
    optional_fields = [
        ("Email:", "email_entry"),
        ("Date of Birth (YYYY-MM-DD):", "dob_entry"),
    ]
    
    for i, (label, var_name) in enumerate(optional_fields, start=len(basic_fields)):
        tk.Label(
            form_frame,
            text=label,
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#2c3e50"
        ).grid(row=i, column=0, sticky="w", pady=10, padx=(0, 10))
        
        entry = tk.Entry(form_frame, width=30, font=("Arial", 12))
        entry.grid(row=i, column=1, pady=10)
        
        # Assign to global variables
        if var_name == "email_entry":
            email_entry = entry
        elif var_name == "dob_entry":
            dob_entry = entry
    
    # Gender selection
    tk.Label(
        form_frame,
        text="Gender:",
        font=("Arial", 12),
        bg="#f0f0f0",
        fg="#2c3e50"
    ).grid(row=len(basic_fields)+len(optional_fields), column=0, sticky="w", pady=10, padx=(0, 10))
    
    gender_frame = tk.Frame(form_frame, bg="#f0f0f0")
    gender_frame.grid(row=len(basic_fields)+len(optional_fields), column=1, sticky="w", pady=10)
    
    gender_var = tk.StringVar()
    tk.Radiobutton(
        gender_frame,
        text="Male",
        variable=gender_var,
        value="Male",
        bg="#f0f0f0"
    ).pack(side="left", padx=5)
    
    tk.Radiobutton(
        gender_frame,
        text="Female",
        variable=gender_var,
        value="Female",
        bg="#f0f0f0"
    ).pack(side="left", padx=5)
    
    tk.Radiobutton(
        gender_frame,
        text="Other",
        variable=gender_var,
        value="Other",
        bg="#f0f0f0"
    ).pack(side="left", padx=5)
    
    # Buttons for tourist tab
    button_frame = tk.Frame(tourist_tab, bg="#f0f0f0")
    button_frame.pack(pady=20)
    
    tk.Button(
        button_frame,
        text="Add Tourist",
        command=add_tourist,
        bg="#27ae60",
        fg="white",
        font=("Arial", 12, "bold"),
        width=15,
        pady=10
    ).pack(side="left", padx=10)
    
    tk.Button(
        button_frame,
        text="Clear Form",
        command=clear_tourist_fields,
        bg="#e74c3c",
        fg="white",
        font=("Arial", 12),
        width=15,
        pady=10
    ).pack(side="left", padx=10)
    
    tk.Button(
        button_frame,
        text="View All Tourists",
        command=view_tourists,
        bg="#3498db",
        fg="white",
        font=("Arial", 12),
        width=15,
        pady=10
    ).pack(side="left", padx=10)
    
    # Tab 3: Booking Management
    booking_tab = tk.Frame(notebook, bg="#f0f0f0")
    notebook.add(booking_tab, text="📅 Booking Management")
    
    # Booking form
    booking_form_frame = tk.Frame(booking_tab, bg="#f0f0f0")
    booking_form_frame.pack(pady=20)
    
    # Create booking form fields
    booking_fields = [
        ("Tourist ID *:", "b_tourist_id_entry"),
        ("Package ID *:", "b_package_id_entry"),
        ("Travel Date (YYYY-MM-DD) *:", "travel_date_entry"),
        ("Number of People *:", "num_people_entry")
    ]
    
    for i, (label, var_name) in enumerate(booking_fields):
        tk.Label(
            booking_form_frame,
            text=label,
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#2c3e50"
        ).grid(row=i, column=0, sticky="w", pady=10, padx=(0, 10))
        
        entry = tk.Entry(booking_form_frame, width=30, font=("Arial", 12))
        entry.grid(row=i, column=1, pady=10)
        
        # Assign to global variables
        if var_name == "b_tourist_id_entry":
            b_tourist_id_entry = entry
        elif var_name == "b_package_id_entry":
            b_package_id_entry = entry
        elif var_name == "travel_date_entry":
            travel_date_entry = entry
        elif var_name == "num_people_entry":
            num_people_entry = entry
    
    # Info label
    info_label = tk.Label(
        booking_tab,
        text="Note: View packages to get Package IDs. Tourist IDs are auto-generated when adding tourists.",
        font=("Arial", 10, "italic"),
        bg="#f0f0f0",
        fg="#e74c3c"
    )
    info_label.pack(pady=10)
    
    # Buttons for booking tab
    booking_button_frame = tk.Frame(booking_tab, bg="#f0f0f0")
    booking_button_frame.pack(pady=20)
    
    tk.Button(
        booking_button_frame,
        text="Create Booking",
        command=add_booking,
        bg="#27ae60",
        fg="white",
        font=("Arial", 12, "bold"),
        width=15,
        pady=10
    ).pack(side="left", padx=10)
    
    tk.Button(
        booking_button_frame,
        text="Clear Form",
        command=clear_booking_fields,
        bg="#e74c3c",
        fg="white",
        font=("Arial", 12),
        width=15,
        pady=10
    ).pack(side="left", padx=10)
    
    tk.Button(
        booking_button_frame,
        text="View Packages",
        command=view_packages,
        bg="#3498db",
        fg="white",
        font=("Arial", 12),
        width=15,
        pady=10
    ).pack(side="left", padx=10)
    
    tk.Button(
        booking_button_frame,
        text="View Bookings",
        command=view_bookings,
        bg="#9b59b6",
        fg="white",
        font=("Arial", 12),
        width=15,
        pady=10
    ).pack(side="left", padx=10)
    
    # Tab 4: View Data
    view_tab = tk.Frame(notebook, bg="#f0f0f0")
    notebook.add(view_tab, text="📊 View Data")
    
    view_button_frame = tk.Frame(view_tab, bg="#f0f0f0")
    view_button_frame.pack(pady=50)
    
    tk.Button(
        view_button_frame,
        text="View All Tourists",
        command=view_tourists,
        bg="#3498db",
        fg="white",
        font=("Arial", 14),
        width=25,
        pady=15
    ).pack(pady=10)
    
    tk.Button(
        view_button_frame,
        text="View All Packages",
        command=view_packages,
        bg="#2ecc71",
        fg="white",
        font=("Arial", 14),
        width=25,
        pady=15
    ).pack(pady=10)
    
    tk.Button(
        view_button_frame,
        text="View All Bookings",
        command=view_bookings,
        bg="#9b59b6",
        fg="white",
        font=("Arial", 14),
        width=25,
        pady=15
    ).pack(pady=10)
    
    # Footer
    footer_frame = tk.Frame(root, bg="#2c3e50", height=40)
    footer_frame.pack(fill="x", side="bottom")
    footer_frame.pack_propagate(False)
    
    tk.Label(
        footer_frame,
        text="© 2024 Pakistan Tourism Management System | Database: PTMS1",
        font=("Arial", 10),
        fg="white",
        bg="#2c3e50"
    ).pack(pady=10)
    
    return root

# ---------------- MAIN EXECUTION ----------------
if __name__ == "__main__":
    print("Checking database structure...")
    check_database_structure()
    print("Updating database structure if needed...")
    update_database_structure()
    print("Creating GUI...")
    root = create_simple_gui()
    print("Application started successfully!")
    root.mainloop()