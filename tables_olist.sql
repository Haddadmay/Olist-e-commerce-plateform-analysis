CREATE TABLE olist_geolocation (
    geolocation_zip_code_prefix INTEGER PRIMARY KEY,
    geolocation_lat NUMERIC(10, 8),
    geolocation_lng NUMERIC(11, 8),
    geolocation_city VARCHAR(100),
    geolocation_state VARCHAR(2)
);

CREATE TABLE product_category_name_translation (
    product_category_name VARCHAR(100) PRIMARY KEY,
    product_category_name_english VARCHAR(100)
);

CREATE TABLE olist_customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_unique_id VARCHAR(50) UNIQUE NOT NULL,
    customer_zip_code_prefix INTEGER,
    customer_city VARCHAR(100),
    customer_state VARCHAR(2),
    FOREIGN KEY (customer_zip_code_prefix) 
        REFERENCES olist_geolocation(geolocation_zip_code_prefix) 
        ON DELETE SET NULL
);

CREATE TABLE olist_sellers (
    seller_id VARCHAR(50) PRIMARY KEY,
    seller_zip_code_prefix INTEGER,
    seller_city VARCHAR(100),
    seller_state VARCHAR(2),
    FOREIGN KEY (seller_zip_code_prefix) 
        REFERENCES olist_geolocation(geolocation_zip_code_prefix) 
        ON DELETE SET NULL
);

CREATE TABLE olist_products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_category_name VARCHAR(100),
    product_photos_qty INTEGER DEFAULT 0,
    FOREIGN KEY (product_category_name) 
        REFERENCES product_category_name_translation(product_category_name) 
        ON DELETE SET NULL
);

CREATE TABLE olist_orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    order_status VARCHAR(20) NOT NULL,
    order_purchase_timestamp TIMESTAMP NOT NULL,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP,
    FOREIGN KEY (customer_id) 
        REFERENCES olist_customers(customer_id) 
        ON DELETE CASCADE
);

CREATE TABLE olist_order_items (
    order_id VARCHAR(50) NOT NULL,
    order_item_id INTEGER NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    seller_id VARCHAR(50) NOT NULL,
    shipping_limit_date TIMESTAMP,
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    freight_value NUMERIC(10, 2) CHECK (freight_value >= 0),
    PRIMARY KEY (order_id, order_item_id),
    FOREIGN KEY (order_id) 
        REFERENCES olist_orders(order_id) 
        ON DELETE CASCADE,
    FOREIGN KEY (product_id) 
        REFERENCES olist_products(product_id) 
        ON DELETE RESTRICT,
    FOREIGN KEY (seller_id) 
        REFERENCES olist_sellers(seller_id) 
        ON DELETE RESTRICT
);

CREATE TABLE olist_order_payments (
    order_id VARCHAR(50) NOT NULL,
    payment_sequential INTEGER NOT NULL,
    payment_type VARCHAR(20) NOT NULL,
    payment_installments INTEGER DEFAULT 1,
    payment_value NUMERIC(10, 2) NOT NULL CHECK (payment_value >= 0),
    PRIMARY KEY (order_id, payment_sequential),
    FOREIGN KEY (order_id) 
        REFERENCES olist_orders(order_id) 
        ON DELETE CASCADE
);

CREATE TABLE olist_order_reviews (
    review_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL UNIQUE,  -- UNIQUE car 1 avis max par commande
    review_score INTEGER CHECK (review_score BETWEEN 1 AND 5),
    review_comment_title VARCHAR(255),
    review_comment_message TEXT,
    review_creation_date TIMESTAMP,
    review_answer_timestamp TIMESTAMP,
    FOREIGN KEY (order_id) 
        REFERENCES olist_orders(order_id) 
        ON DELETE CASCADE
);

CREATE INDEX idx_customers_zip ON olist_customers(customer_zip_code_prefix);
CREATE INDEX idx_sellers_zip ON olist_sellers(seller_zip_code_prefix);
CREATE INDEX idx_orders_customer ON olist_orders(customer_id);
CREATE INDEX idx_orders_status ON olist_orders(order_status);
CREATE INDEX idx_order_items_product ON olist_order_items(product_id);
CREATE INDEX idx_order_items_seller ON olist_order_items(seller_id);
CREATE INDEX idx_products_category ON olist_products(product_category_name);

CREATE INDEX idx_orders_purchase_date ON olist_orders(order_purchase_timestamp);
CREATE INDEX idx_reviews_creation_date ON olist_order_reviews(review_creation_date);