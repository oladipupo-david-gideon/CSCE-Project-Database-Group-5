-- ============================================
-- PHASE 1: INDEPENDENT ENTITIES 
-- =============================================

CREATE TABLE Company (
    company_id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    hq_address VARCHAR(255)
);

CREATE TABLE Dealer (
    dealer_id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    phone VARCHAR(20)
);

CREATE TABLE Customer (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    address VARCHAR(255),
    phone VARCHAR(20),
    gender CHAR(1) CHECK (gender IN ('M', 'F', 'O', 'U')),
    annual_income NUMERIC(12, 2) CHECK (annual_income >= 0)
);

CREATE TABLE Supplier (
    supplier_id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    address VARCHAR(255),
    contact_phone VARCHAR(20)
);

CREATE TABLE Plant (
    plant_id SERIAL PRIMARY KEY,
    supplier_id INT, -- NULL if company-owned, populated if supplier-owned
    name VARCHAR(150) NOT NULL,
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    plant_type VARCHAR(50) CHECK (plant_type IN ('parts-manufacturing', 'final-assembly')),
    FOREIGN KEY (supplier_id) REFERENCES Supplier(supplier_id) ON DELETE SET NULL
);

CREATE TABLE Options (
    options_id SERIAL PRIMARY KEY,
    engine_type VARCHAR(100),
    transmission_type VARCHAR(100),
    color VARCHAR(50)
);

-- ======================================================
-- PHASE 2: DEPENDENT ENTITIES 
-- ======================================================

CREATE TABLE Brand (
    brand_id SERIAL PRIMARY KEY,
    company_id INT NOT NULL,
    brand_name VARCHAR(100) NOT NULL,
    country_of_origin VARCHAR(100),
    FOREIGN KEY (company_id) REFERENCES Company(company_id) ON DELETE CASCADE
);

CREATE TABLE Model (
    model_id SERIAL PRIMARY KEY,
    brand_id INT NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    body_style VARCHAR(50),
    year INT,
    FOREIGN KEY (brand_id) REFERENCES Brand(brand_id) ON DELETE CASCADE
);

CREATE TABLE Part (
    part_id SERIAL PRIMARY KEY,
    supplier_id INT NOT NULL,
    part_name VARCHAR(150) NOT NULL,
    part_type VARCHAR(100), 
    FOREIGN KEY (supplier_id) REFERENCES Supplier(supplier_id)
);

CREATE TABLE Vehicle (
    vin VARCHAR(17) PRIMARY KEY,
    model_id INT NOT NULL,
    options_id INT NOT NULL,
    manufacture_date DATE,
    status VARCHAR(20) CHECK (status IN ('available', 'sold')),
    FOREIGN KEY (model_id) REFERENCES Model(model_id),
    FOREIGN KEY (options_id) REFERENCES Options(options_id)
);

-- ==================================================
-- PHASE 3: TRANSACTIONAL ENTITIES 
-- ==================================================

CREATE TABLE Inventory (
    inventory_id SERIAL PRIMARY KEY,
    dealer_id INT NOT NULL,
    vin VARCHAR(17) UNIQUE NOT NULL, 
    date_received DATE NOT NULL,
    date_sold DATE,
    price NUMERIC(10, 2),
    FOREIGN KEY (dealer_id) REFERENCES Dealer(dealer_id),
    FOREIGN KEY (vin) REFERENCES Vehicle(vin) ON DELETE CASCADE
);

CREATE TABLE Sale (
    sale_id SERIAL PRIMARY KEY,
    vin VARCHAR(17) UNIQUE NOT NULL, 
    dealer_id INT NOT NULL,
    customer_id INT NOT NULL,
    sale_date DATE NOT NULL,
    sale_price NUMERIC(10, 2) NOT NULL CHECK (sale_price > 0),
    FOREIGN KEY (vin) REFERENCES Vehicle(vin),
    FOREIGN KEY (dealer_id) REFERENCES Dealer(dealer_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

CREATE TABLE Customer_Inquiry (
    inquiry_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    dealer_id INT NOT NULL,
    model_id INT, 
    inquiry_date DATE NOT NULL DEFAULT CURRENT_DATE,
    notes TEXT,
    status VARCHAR(20) NOT NULL CHECK (status IN ('Unfulfilled', 'In Progress', 'Resolved')) DEFAULT 'Unfulfilled',
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (dealer_id) REFERENCES Dealer(dealer_id) ON DELETE CASCADE,
    FOREIGN KEY (model_id) REFERENCES Model(model_id) ON DELETE SET NULL
);

-- ==============================================
-- PHASE 4: M:N JUNCTION TABLES
-- ==============================================

CREATE TABLE Dealer_Brand (
    dealer_id INT NOT NULL,
    brand_id INT NOT NULL,
    PRIMARY KEY (dealer_id, brand_id),
    FOREIGN KEY (dealer_id) REFERENCES Dealer(dealer_id) ON DELETE CASCADE,
    FOREIGN KEY (brand_id) REFERENCES Brand(brand_id) ON DELETE CASCADE
);

CREATE TABLE Model_Part (
    model_id INT NOT NULL,
    part_id INT NOT NULL,
    PRIMARY KEY (model_id, part_id),
    FOREIGN KEY (model_id) REFERENCES Model(model_id) ON DELETE CASCADE,
    FOREIGN KEY (part_id) REFERENCES Part(part_id) ON DELETE CASCADE
);

CREATE TABLE Plant_Part (
    plant_id INT NOT NULL,
    part_id INT NOT NULL,
    PRIMARY KEY (plant_id, part_id),
    FOREIGN KEY (plant_id) REFERENCES Plant(plant_id) ON DELETE CASCADE,
    FOREIGN KEY (part_id) REFERENCES Part(part_id) ON DELETE CASCADE
);

CREATE TABLE Plant_Model (
    plant_id INT NOT NULL,
    model_id INT NOT NULL,
    PRIMARY KEY (plant_id, model_id),
    FOREIGN KEY (plant_id) REFERENCES Plant(plant_id) ON DELETE CASCADE,
    FOREIGN KEY (model_id) REFERENCES Model(model_id) ON DELETE CASCADE
);

CREATE TABLE Vehicle_Part (
    vin VARCHAR(17) NOT NULL,
    part_id INT NOT NULL,
    plant_id INT, 
    manufacture_date DATE,
    PRIMARY KEY (vin, part_id),
    FOREIGN KEY (vin) REFERENCES Vehicle(vin) ON DELETE CASCADE,
    FOREIGN KEY (part_id) REFERENCES Part(part_id) ON DELETE CASCADE,
    FOREIGN KEY (plant_id) REFERENCES Plant(plant_id) ON DELETE SET NULL
);