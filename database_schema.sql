-- Create Database
CREATE DATABASE IF NOT EXISTS inventory_db;
USE inventory_db;

-- Create Products Table
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    barcode VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    quantity INT DEFAULT 0,
    price DECIMAL(10, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_barcode (barcode),
    INDEX idx_name (name)
);

-- Insert Sample Data
INSERT INTO products (barcode, name, description, quantity, price) VALUES
('12345678', 'Product A', 'High quality product A', 50, 299.99),
('87654321', 'Product B', 'Premium product B', 30, 499.99),
('11111111', 'Product C', 'Standard product C', 100, 199.99),
('22222222', 'Product D', 'Deluxe product D', 20, 799.99),
('33333333', 'Product E', 'Basic product E', 75, 99.99);
