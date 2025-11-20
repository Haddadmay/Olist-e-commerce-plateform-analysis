-- Créer les schémas
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;


-- Supprimer et créer les tables Bronze pour PostgreSQL

-- 1. olist_geolocation
DROP TABLE IF EXISTS bronze.olist_geolocation;
CREATE TABLE bronze.olist_geolocation (
    geolocation_zip_code_prefix INTEGER,
    geolocation_lat             NUMERIC(10, 8),
    geolocation_lng             NUMERIC(11, 8),
    geolocation_city            VARCHAR(100),
    geolocation_state           VARCHAR(2)
);

-- 2. product_category_name_translation
DROP TABLE IF EXISTS bronze.product_category_name_translation;
CREATE TABLE bronze.product_category_name_translation (
    product_category_name         VARCHAR(100),
    product_category_name_english VARCHAR(100)
);

-- 3. olist_customers
DROP TABLE IF EXISTS bronze.olist_customers;
CREATE TABLE bronze.olist_customers (
    customer_id              VARCHAR(50),
    customer_unique_id       VARCHAR(50),
    customer_zip_code_prefix INTEGER,
    customer_city            VARCHAR(100),
    customer_state           VARCHAR(2)
);

-- 4. olist_sellers
DROP TABLE IF EXISTS bronze.olist_sellers;
CREATE TABLE bronze.olist_sellers (
    seller_id              VARCHAR(50),
    seller_zip_code_prefix INTEGER,
    seller_city            VARCHAR(100),
    seller_state           VARCHAR(2)
);

-- 5. olist_products
DROP TABLE IF EXISTS bronze.olist_products;
CREATE TABLE bronze.olist_products (
    product_id            VARCHAR(50),
    product_category_name VARCHAR(100),
    product_name_lenght   INTEGER,
	product_description_lenght INTEGER,
	product_photos_qty INTEGER,
	product_weight_g INTEGER,
	product_length_cm INTEGER,
	product_height_cm INTEGER,
	product_width_cm INTEGER
);

-- 6. olist_orders
DROP TABLE IF EXISTS bronze.olist_orders;
CREATE TABLE bronze.olist_orders (
    order_id                      VARCHAR(50),
    customer_id                   VARCHAR(50),
    order_status                  VARCHAR(20),
    order_purchase_timestamp      TIMESTAMP,
    order_approved_at             TIMESTAMP,
    order_delivered_carrier_date  TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP
);

-- 7. olist_order_items
DROP TABLE IF EXISTS bronze.olist_order_items;
CREATE TABLE bronze.olist_order_items (
    order_id            VARCHAR(50),
    order_item_id       INTEGER,
    product_id          VARCHAR(50),
    seller_id           VARCHAR(50),
    shipping_limit_date TIMESTAMP,
    price               NUMERIC(10, 2),
    freight_value       NUMERIC(10, 2)
);

-- 8. olist_order_payments
DROP TABLE IF EXISTS bronze.olist_order_payments;
CREATE TABLE bronze.olist_order_payments (
    order_id             VARCHAR(50),
    payment_sequential   INTEGER,
    payment_type         VARCHAR(20),
    payment_installments INTEGER,
    payment_value        NUMERIC(10, 2)
);

-- 9. olist_order_reviews
DROP TABLE IF EXISTS bronze.olist_order_reviews;
CREATE TABLE bronze.olist_order_reviews (
    review_id               VARCHAR(50),
    order_id                VARCHAR(50),
    review_score            INTEGER,
    review_comment_title    VARCHAR(255),
    review_comment_message  TEXT,
    review_creation_date    TIMESTAMP,
    review_answer_timestamp TIMESTAMP
);