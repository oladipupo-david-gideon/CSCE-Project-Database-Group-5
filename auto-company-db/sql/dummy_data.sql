-- CLEAR EXISTING DATA (If re-running)
TRUNCATE TABLE Vehicle_Part, Plant_Model, Plant_Part, Model_Part, Dealer_Brand, Customer_Inquiry, Sale, Inventory, Vehicle, Part, Model, Brand, Options, Plant, Supplier, Customer, Dealer, Company RESTART IDENTITY CASCADE;

-- ==========================================
-- 1. INDEPENDENT ENTITIES
-- ==========================================

INSERT INTO Company (name, hq_address) VALUES 
('Apex Motor Group', '100 Apex Way, Detroit, MI'),
('Nova Dynamics', '500 Innovation Blvd, Austin, TX'),
('Horizon Automotive', '777 Skyline Dr, Seattle, WA');

INSERT INTO Dealer (name, address, city, state, phone) VALUES 
('Fort Worth Auto Hub', '123 Texas Trail', 'Fort Worth', 'TX', '817-555-0199'),
('Dallas Elite Motors', '888 Commerce St', 'Dallas', 'TX', '214-555-0288'),
('Sunset Drives', '404 Ocean Ave', 'Los Angeles', 'CA', '310-555-0377'),
('Windy City Autos', '500 Lake Shore Dr', 'Chicago', 'IL', '312-555-0455'),
('Miami Sun Motors', '100 Biscayne Blvd', 'Miami', 'FL', '305-555-0677'),
('Seattle Eco Cars', '200 Pike St', 'Seattle', 'WA', '206-555-0899');

INSERT INTO Customer (first_name, last_name, address, phone, gender, annual_income) VALUES 
('Alice', 'Johnson', '789 Pine Ln, Fort Worth, TX', '817-555-9911', 'F', 85000.00),
('Bob', 'Smith', '456 Oak Dr, Dallas, TX', '214-555-8822', 'M', 110000.00),
('Charlie', 'Davis', '123 Maple Blvd, LA, CA', '310-555-7733', 'M', 75000.00),
('Diana', 'Prince', '999 Amazon Way, NY, NY', '212-555-1234', 'F', 150000.00),
('Evan', 'Wright', '444 Loop St, Chicago, IL', '312-555-5678', 'M', 62000.00),
('Fiona', 'Gallagher', '555 South Side, Chicago, IL', '312-555-9876', 'F', 54000.00),
('George', 'Miller', '111 Beach Rd, Miami, FL', '305-555-4321', 'M', 95000.00),
('Hannah', 'Abbott', '222 Rain Ave, Seattle, WA', '206-555-8765', 'F', 120000.00);

INSERT INTO Supplier (name, address, contact_phone) VALUES 
('Getrag Transmissions', '1 Autobahn, Munich, Germany', '+49-123-456'),
('Bosch Electronics', '5 Tech Park, Berlin, Germany', '+49-987-654'),
('Apex Internal Parts', '200 Apex Way, Detroit, MI', '313-555-0000'),
('Takata Safety Systems', '100 Minato, Tokyo, Japan', '+81-333-444'),
('Michelin Tires', '1 Clermont-Ferrand, France', '+33-111-222');

INSERT INTO Plant (supplier_id, name, address, city, state, plant_type) VALUES 
(1, 'Getrag Munich Facility', '1 Autobahn', 'Munich', 'Bavaria', 'parts-manufacturing'),
(2, 'Bosch ECU Plant', '5 Tech Park', 'Berlin', 'Berlin', 'parts-manufacturing'),
(4, 'Takata Global Assembly', '100 Minato', 'Tokyo', 'Tokyo', 'parts-manufacturing'),
(NULL, 'Apex Assembly Line A', '300 Apex Way', 'Detroit', 'MI', 'final-assembly'),
(NULL, 'Nova EV Factory', '1000 Tesla Rd', 'Austin', 'TX', 'final-assembly'),
(NULL, 'Horizon West Coast Plant', '700 Skyline Dr', 'Seattle', 'WA', 'final-assembly');

INSERT INTO Options (engine_type, transmission_type, color) VALUES 
('5.0L V8', '6-Speed Manual', 'Cherry Red'),
('2.0L Turbo 4-Cyl', '8-Speed Automatic', 'Midnight Blue'),
('Electric Motor', '1-Speed Direct Drive', 'Pearl White'),
('3.5L V6', '10-Speed Automatic', 'Shadow Black'),
('Electric Motor (Dual)', '1-Speed Direct Drive', 'Matte Grey'),
('2.5L Hybrid', 'CVT', 'Forest Green');

-- ==========================================
-- 2. DEPENDENT ENTITIES
-- ==========================================

INSERT INTO Brand (company_id, brand_name, country_of_origin) VALUES 
(1, 'Velocity', 'USA'),
(1, 'Titan', 'USA'),
(2, 'EcoDrive', 'USA'),
(3, 'Aero', 'USA');

INSERT INTO Model (brand_id, model_name, body_style, year) VALUES 
(1, 'V-Roadster', 'Convertible', 2024),
(1, 'V-Cruiser', 'Sedan', 2024),
(2, 'T-Hauler', 'Truck', 2025),
(2, 'T-Explorer', 'SUV', 2023),
(3, 'Volt-Hatch', 'Hatchback', 2023),
(3, 'Volt-Cabrio', 'Convertible', 2025),
(4, 'Zephyr', 'Sedan', 2025),
(4, 'Breeze', 'Convertible', 2024);

INSERT INTO Part (supplier_id, part_name, part_type) VALUES 
(1, 'Getrag 6MT-82', 'Transmission'),
(2, 'Bosch Engine Control Unit', 'Electronics'),
(3, 'V8 Block', 'Engine'),
(4, 'Takata Driver Airbag Module', 'Safety'),
(5, 'Pilot Sport 4S', 'Tires'),
(2, 'Bosch Battery Management System', 'Electronics');

INSERT INTO Vehicle (vin, model_id, options_id, manufacture_date, status) VALUES 
('VIN11111111111111', 1, 1, '2023-05-10', 'sold'),
('VIN22222222222222', 1, 1, '2024-01-15', 'available'),
('VIN33333333333333', 2, 2, '2023-08-20', 'sold'),
('VIN44444444444444', 5, 3, '2023-11-05', 'available'),
('VIN55555555555555', 3, 4, '2024-06-10', 'sold'),
('VIN66666666666666', 4, 2, '2023-01-15', 'sold'),
('VIN77777777777777', 6, 5, '2024-12-01', 'sold'),
('VIN88888888888888', 8, 6, '2024-02-20', 'sold'),
('VIN99999999999999', 7, 5, '2025-01-10', 'available'),
('VINA0000000000000', 3, 4, '2025-02-15', 'available'),
('VINB0000000000000', 6, 5, '2025-03-01', 'available'),
('VINC0000000000000', 1, 1, '2024-05-10', 'sold'),
('VIND0000000000000', 8, 6, '2024-06-15', 'sold');

-- ==========================================
-- 3. TRANSACTIONAL ENTITIES
-- ==========================================

INSERT INTO Inventory (dealer_id, vin, date_received, date_sold, price) VALUES 
(1, 'VIN11111111111111', '2023-05-15', '2023-06-01', 55000.00),
(1, 'VIN22222222222222', '2024-02-01', NULL, 56000.00),
(2, 'VIN33333333333333', '2023-09-01', '2023-09-10', 35000.00),
(3, 'VIN44444444444444', '2023-11-10', NULL, 42000.00),
(4, 'VIN55555555555555', '2024-06-15', '2024-07-05', 65000.00),
(1, 'VIN66666666666666', '2023-02-01', '2023-02-14', 48000.00),
(5, 'VIN77777777777777', '2024-12-10', '2025-01-05', 72000.00),
(6, 'VIN88888888888888', '2024-03-01', '2024-05-15', 51000.00),
(2, 'VIN99999999999999', '2025-02-01', NULL, 58000.00),
(1, 'VINA0000000000000', '2025-03-01', NULL, 66000.00),
(5, 'VINB0000000000000', '2025-03-10', NULL, 73000.00),
(3, 'VINC0000000000000', '2024-05-20', '2024-06-10', 55500.00),
(4, 'VIND0000000000000', '2024-07-01', '2024-07-20', 52000.00);

INSERT INTO Sale (vin, dealer_id, customer_id, sale_date, sale_price) VALUES 
('VIN11111111111111', 1, 1, '2023-06-01', 54500.00),
('VIN33333333333333', 2, 2, '2023-09-10', 34000.00),
('VIN55555555555555', 4, 5, '2024-07-05', 64000.00),
('VIN66666666666666', 1, 3, '2023-02-14', 47500.00),
('VIN77777777777777', 5, 7, '2025-01-05', 71000.00),
('VIN88888888888888', 6, 8, '2024-05-15', 50500.00),
('VINC0000000000000', 3, 3, '2024-06-10', 55000.00),
('VIND0000000000000', 4, 6, '2024-07-20', 51000.00);

INSERT INTO Customer_Inquiry (customer_id, dealer_id, model_id, inquiry_date, notes, status) VALUES 
(3, 1, 1, '2024-04-10', 'Wants a red convertible before summer, checking inventory.', 'Unfulfilled'),
(1, 2, 5, '2024-04-12', 'Curious about EV tax credits for the Volt-Hatch.', 'In Progress'),
(4, 5, 6, '2025-01-20', 'Looking for a Volt-Cabrio for spring break in Miami.', 'Unfulfilled'),
(8, 6, 8, '2025-02-05', 'Does the Breeze come in Forest Green?', 'Unfulfilled'),
(5, 4, 3, '2025-03-01', 'Need a heavy-duty truck for work, wanting to test drive the T-Hauler.', 'Resolved');

-- ==========================================
-- 4. JUNCTION TABLES
-- ==========================================

INSERT INTO Dealer_Brand (dealer_id, brand_id) VALUES 
(1, 1), (1, 2), (2, 1), (3, 2), (3, 3), (4, 1), (4, 4), (5, 3), (6, 4);

INSERT INTO Model_Part (model_id, part_id) VALUES 
(1, 1), (1, 3), (1, 4), (2, 2), (2, 4), (3, 3), (3, 5), (4, 2), (5, 6), (6, 6), (6, 4), (7, 6), (8, 2), (8, 5);

INSERT INTO Plant_Part (plant_id, part_id) VALUES 
(1, 1), (2, 2), (2, 6), (3, 4), (4, 3), (4, 5);

INSERT INTO Plant_Model (plant_id, model_id) VALUES 
(4, 1), (4, 2), (4, 3), (4, 4), (5, 5), (5, 6), (6, 7), (6, 8);

-- Linking defective parts (Getrag and Takata) for the DBA trace
INSERT INTO Vehicle_Part (vin, part_id, plant_id, manufacture_date) VALUES 
('VIN11111111111111', 1, 1, '2023-05-01'), -- Has Getrag
('VIN11111111111111', 4, 3, '2023-04-15'), -- Has Takata
('VIN22222222222222', 1, 1, '2024-01-05'), -- Has Getrag
('VIN33333333333333', 2, 2, '2023-08-10'),
('VIN44444444444444', 6, 2, '2023-10-25'),
('VIN55555555555555', 3, 4, '2024-06-01'),
('VIN66666666666666', 4, 3, '2022-12-10'), -- Has Takata
('VIN77777777777777', 6, 2, '2024-11-20'),
('VIN88888888888888', 5, 4, '2024-02-05'),
('VIN99999999999999', 6, 2, '2024-12-28'),
('VINA0000000000000', 3, 4, '2025-02-01'),
('VINB0000000000000', 4, 3, '2025-02-15'), -- Has Takata
('VINC0000000000000', 1, 1, '2024-04-20'), -- Has Getrag
('VIND0000000000000', 2, 2, '2024-06-01');