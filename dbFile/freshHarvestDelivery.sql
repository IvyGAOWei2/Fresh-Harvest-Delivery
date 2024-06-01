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

CREATE TABLE BusinessApplications (
    application_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id SMALLINT NOT NULL,
    business_name VARCHAR(100) NOT NULL,
    contact_name VARCHAR(100) NOT NULL,
    email VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    postcode VARCHAR(10) NOT NULL,
    documentation VARCHAR(255) NOT NULL,
    status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
    application_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    approved_by SMALLINT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (approved_by) REFERENCES Users(user_id)
);

CREATE TABLE AccountLimitReviewRequests (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id SMALLINT,
    current_account_limit DECIMAL(10, 2),
    new_account_limit DECIMAL(10, 2),
    status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
    request_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    decision_date DATETIME,
    FOREIGN KEY (user_id) REFERENCES Consumer(user_id)
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
    discount_price DECIMAL(10, 2),
    stock SMALLINT,
    category_id TINYINT,
    unit_id TINYINT,
    depot_id TINYINT,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (category_id) REFERENCES Category(category_id),
    FOREIGN KEY (unit_id) REFERENCES Unit(unit_id),
    FOREIGN KEY (depot_id) REFERENCES Depots(depot_id)
);

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
    image VARCHAR(80) NOT NULL,
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

CREATE TABLE Packages (
    package_id SMALLINT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    depot_id TINYINT,
    FOREIGN KEY (depot_id) REFERENCES Depots(depot_id)
);


CREATE TABLE Boxes (
    box_id SMALLINT PRIMARY KEY AUTO_INCREMENT,
    package_id SMALLINT,
    box_type ENUM('Large', 'Medium', 'Small') NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (package_id) REFERENCES Packages(package_id)
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
    promotion_id INT PRIMARY KEY AUTO_INCREMENT,
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

CREATE TABLE Reviews (
    review_id SMALLINT PRIMARY KEY AUTO_INCREMENT,
    user_id SMALLINT NOT NULL,
    depot_id TINYINT NOT NULL,
    product_id SMALLINT NOT NULL,
    review_date DATE NOT NULL,
    review_text TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (depot_id) REFERENCES Depots(depot_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

CREATE TABLE Discounts (
    discount_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    discount_rate DECIMAL(5, 2) NOT NULL,
    status BOOLEAN DEFAULT TRUE
     depot_id TINYINT,
    FOREIGN KEY (depot_id) REFERENCES Depots(depot_id)
);

CREATE TABLE DiscountedProducts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    discount_id INT,
    product_id SMALLINT,
    FOREIGN KEY (discount_id) REFERENCES Discounts(discount_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);
