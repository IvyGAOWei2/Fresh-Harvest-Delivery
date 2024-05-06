DROP SCHEMA IF EXISTS freshHarvestDelivery;
CREATE SCHEMA freshHarvestDelivery;
USE freshHarvestDelivery;


CREATE TABLE Depots (
    depot_id TINYINT PRIMARY KEY AUTO_INCREMENT,
    location VARCHAR(30)
);

CREATE TABLE Users (
    user_id SMALLINT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(64) NOT NULL,
	type ENUM('Consumer', 'Staff', 'Local_Manager', 'National_Manager', 'Placeholder1', 'Placeholder2', 'Placeholder3') NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_deleted BOOLEAN DEFAULT FALSE,
	depot_id TINYINT,
	FOREIGN KEY (depot_id) REFERENCES Depots(depot_id)
);

CREATE TABLE Subscription (
    subscription_id SMALLINT PRIMARY KEY AUTO_INCREMENT,
    user_id SMALLINT UNIQUE NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    type ENUM('Weekly', 'Fortnightly', 'Monthly', 'Placeholder1', 'Placeholder2', 'Placeholder3') NOT NULL,
    CHECK (start_date < end_date),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Consumer (
    user_id SMALLINT PRIMARY KEY,
    given_name VARCHAR(35),
    family_name VARCHAR(35) NOT NULL,
    address VARCHAR(80),
    phone VARCHAR(13) NOT NULL,
	city VARCHAR(100),
	postcode VARCHAR(10),
	image VARCHAR(80),
	credit_available DECIMAL(10, 2),
	account_limit DECIMAL(10, 2),
	account_available DECIMAL(10, 2),
	registration_date DATE DEFAULT (CURRENT_DATE),
	last_login_date DATETIME,
	user_type ENUM('Residential', 'Business', 'Placeholder1', 'Placeholder2', 'Placeholder3') DEFAULT 'Residential' NOT NULL,
	depot_id TINYINT,
	subscription_id SMALLINT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
	FOREIGN KEY (depot_id) REFERENCES Depots(depot_id),
	FOREIGN KEY (subscription_id) REFERENCES Subscription(subscription_id)
);

CREATE TABLE Category (
    category_id TINYINT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(50) NOT NULL
);

CREATE TABLE Unit (
    unit_id TINYINT PRIMARY KEY AUTO_INCREMENT,
    unit_name VARCHAR(50) NOT NULL
);

CREATE TABLE Products (
    product_id SMALLINT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(50),
	description TEXT,
    price DECIMAL(10, 2),
	discount_price DECIMAL(10, 2), -- record?
    stock SMALLINT,
    category_id TINYINT,
	unit_id TINYINT,
	depot_id TINYINT,
    is_active BOOLEAN DEFAULT TRUE,
	FOREIGN KEY (category_id) REFERENCES Category(category_id),
	FOREIGN KEY (unit_id) REFERENCES Unit(unit_id),
	FOREIGN KEY (depot_id) REFERENCES Depots(depot_id)
);

-- another product??
CREATE TABLE GiftCardcode (
    gift_card_id SMALLINT PRIMARY KEY AUTO_INCREMENT,
	product_id SMALLINT,
	user_id SMALLINT,
    code VARCHAR(20) UNIQUE NOT NULL,
    balance DECIMAL(10, 2),
    is_used BOOLEAN DEFAULT FALSE,
	FOREIGN KEY (product_id) REFERENCES Products(product_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE ProductImages (
    product_image_id SMALLINT PRIMARY KEY AUTO_INCREMENT,
	product_id SMALLINT,
    image VARCHAR(50) NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    is_deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

CREATE TABLE Orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id SMALLINT,
    order_date DATE,
    delivery_date DATE,
	delivery_address VARCHAR(150),
	payment_status ENUM('Completed', 'Failed', 'Refunded', 'Placeholder1', 'Placeholder2', 'Placeholder3'),
	payment_method ENUM('Residential', 'Commercial', 'Placeholder1', 'Placeholder2', 'Placeholder3') DEFAULT 'Residential' NOT NULL,
    status ENUM('Pending', 'Comfirmed', 'Shipped', 'Delivered', 'Cancelled', 'Placeholder1', 'Placeholder2', 'Placeholder3'),
    total DECIMAL(10, 2),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE OrderItems (
    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    product_id SMALLINT,
    quantity TINYINT,
    subtotal DECIMAL(10, 2),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

CREATE TABLE Invoices (
    invoice_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id SMALLINT,
    invoice_date DATE,
    due_date DATE,
    total DECIMAL(10, 2),
    gst_rate SMALLINT DEFAULT 15,
	order_list JSON,
    is_paid BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Employees (
    user_id SMALLINT PRIMARY KEY,
    given_name VARCHAR(35),
    family_name VARCHAR(35) NOT NULL,
    address VARCHAR(80),
    phone VARCHAR(13) NOT NULL,
	image VARCHAR(80),
    hire_date DATE,
	depot_id TINYINT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
	FOREIGN KEY (depot_id) REFERENCES Depots(depot_id)
);

CREATE TABLE Boxes (
    box_id SMALLINT PRIMARY KEY AUTO_INCREMENT,
    box_type ENUM('Large', 'Medium', 'Small', 'Placeholder1', 'Placeholder2', 'Placeholder3'),
	start_date DATE NOT NULL,
    end_date DATE NOT NULL,
	depot_id TINYINT,
    FOREIGN KEY (depot_id) REFERENCES Depots(depot_id)
);

CREATE TABLE BoxItems (
    box_id SMALLINT,
    product_id SMALLINT,
    quantity TINYINT,
    PRIMARY KEY (product_id, box_id),
    FOREIGN KEY (box_id) REFERENCES Boxes(box_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

CREATE TABLE Promotions (
    promotion_id INT PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
	start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    discount_rate TINYINT
);

CREATE TABLE Messages (
    message_id SMALLINT PRIMARY KEY AUTO_INCREMENT,
    sender_id SMALLINT,
    receiver_id SMALLINT,
    message_content TEXT,
    message_date DATETIME,
    status ENUM('unread', 'read'),
    FOREIGN KEY (sender_id) REFERENCES Users(user_id),
    FOREIGN KEY (receiver_id) REFERENCES Users(user_id)
);


INSERT INTO Depots (location) VALUES ('Christchurch'), ('Invercargill'), ('Wellington'), ('Hamilton'), ('Auckland'), ('NZ');
INSERT INTO Category (category_name) VALUES ('Fruit'), ('Vegetable'), ('Herb'), ('Salad'), ('Egg'), ('Honey'), ('GiftCard');
INSERT INTO Unit (unit_name) VALUES ('Bunch'), ('Weight'), ('Each'), ('Half-size'), ('Punnet'), ('Tray');

-- Users table
INSERT INTO Users (email, password_hash, type, depot_id) VALUES
('john.doe@example.com', '9d529731444484d0e41992a8f3dc66ec8826c0ec27e525cf6eb28363f0b31392', 'Consumer', 1),
('jane.smith@example.com', '9d529731444484d0e41992a8f3dc66ec8826c0ec27e525cf6eb28363f0b31392', 'Staff', 1),
('alex.jones@example.com', '9d529731444484d0e41992a8f3dc66ec8826c0ec27e525cf6eb28363f0b31392', 'Local_Manager', 1),
('sarah.wilson@example.com', '9d529731444484d0e41992a8f3dc66ec8826c0ec27e525cf6eb28363f0b31392', 'National_Manager', 6),
('mark.white@example.com', '9d529731444484d0e41992a8f3dc66ec8826c0ec27e525cf6eb28363f0b31392', 'Consumer', 1);

-- Subscription table
INSERT INTO Subscription (user_id, start_date, end_date, type) VALUES
(1, '2024-05-01', '2024-05-31', 'Weekly'),
(5, '2024-05-01', '2024-05-15', 'Fortnightly');
	
-- Consumer table
INSERT INTO Consumer (user_id, given_name, family_name, address, phone, city, postcode, image, credit_available, account_limit, account_available, last_login_date, user_type, depot_id, subscription_id) VALUES
(1, 'John', 'Doe', '123 Main St', '0211234567', 'Christchurch', '8011', 'user_default_image.png', 100.00, null, null, '2024-05-05 18:30:00', 'Residential', 1, 1),
(5, 'Mark', 'White', '456 Elm St', '0279876543', 'Christchurch', '9810', 'user_default_image.png', null, 300.00, 150.00, '2024-05-04 09:15:00', 'Business', 1, 2);

-- Products table
INSERT INTO Products (name, description, price, stock, category_id, unit_id, depot_id) VALUES
('Apples', 'Fresh New Zealand apples', 2.99, 100, 1, 2, 1),
('Carrots', 'Organic carrots', 1.49, 150, 2, 2, 1),
('Lettuce', 'Crisp lettuce', 3.49, 80, 4, 1, 1),
('Free-range Eggs', 'Dozen free-range eggs', 5.99, 50, 5, 6, 1),
('Manuka Honey', 'Pure Manuka honey', 29.99, 30, 6, 3, 1),
('Gift Card', 'Gift Card', null, 3, 7, 3, 1);

-- GiftCardcode table
INSERT INTO GiftCardcode (product_id, user_id, code, balance, is_used) VALUES
(6, 1, 'GC123ABC', 50.00, TRUE),
(6, 1, 'GC456DEF', 50.00, TRUE),
(6, 1, 'GC789GHI', 50.00, FALSE);

-- Orders table
INSERT INTO Orders (order_id, user_id, order_date, delivery_date, delivery_address, payment_status, status, total) VALUES
(1, 1, '2024-05-03', '2024-05-10', '123 Main St, Christchurch', 'Completed', 'Delivered', 10.45),
(2, 5, '2024-04-01', '2024-04-08', '456 Elm St, Christchurch', 'Completed', 'Delivered', 71.96),
(3, 5, '2024-04-02', '2024-04-09', '456 Elm St, Christchurch', 'Completed', 'Delivered', 34.98);

-- OrderItems table
INSERT INTO OrderItems (order_id, product_id, quantity, subtotal) VALUES
(1, 1, 2, 5.98),
(1, 2, 3, 4.47),
(2, 3, 1, 59.98),
(2, 4, 2, 11.98),
(3, 5, 10, 34.98);

-- Invoices table
INSERT INTO Invoices (user_id, invoice_date, due_date, total, gst_rate, order_list) VALUES
(5, '2024-04-30', '2024-05-20', 106.94, 15, '[2,3]');

-- Employees table
INSERT INTO Employees (user_id, given_name, family_name, address, phone, hire_date, depot_id) VALUES
(2, 'Jane', 'Smith', '654 Cedar St', '0298765432', '2023-06-15', 1),
(3, 'Alex', 'Jones', '789 Oak St', '0223456789', '2022-12-01', 1),
(4, 'Sarah', 'Wilson', '321 Pine St', '0208765432', '2024-02-20', 6);

INSERT INTO Boxes (box_id, box_type, start_date, end_date, depot_id) VALUES
(1, 'Small', '2024-04-06', '2024-04-12', 1),
(2, 'Medium', '2024-04-06', '2024-04-12', 1),
(3, 'Large', '2024-04-06', '2024-04-12', 1);

-- BoxItems table
INSERT INTO BoxItems (box_id, product_id, quantity) VALUES
(1, 1, 2),
(1, 2, 2),
(1, 3, 2),
(2, 1, 4),
(2, 2, 4),
(2, 3, 4),
(3, 1, 6),
(3, 2, 6),
(3, 3, 6);
