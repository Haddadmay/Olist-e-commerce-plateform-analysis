
-- Copier la structure des tables Bronze vers Silver
CREATE TABLE silver.olist_geolocation AS TABLE bronze.olist_geolocation WITH NO DATA;
CREATE TABLE silver.olist_customers AS TABLE bronze.olist_customers WITH NO DATA;
CREATE TABLE silver.olist_sellers AS TABLE bronze.olist_sellers WITH NO DATA;
CREATE TABLE silver.olist_products AS TABLE bronze.olist_products WITH NO DATA;
CREATE TABLE silver.olist_orders AS TABLE bronze.olist_orders WITH NO DATA;
CREATE TABLE silver.olist_order_items AS TABLE bronze.olist_order_items WITH NO DATA;
CREATE TABLE silver.olist_order_payments AS TABLE bronze.olist_order_payments WITH NO DATA;
CREATE TABLE silver.olist_order_reviews AS TABLE bronze.olist_order_reviews WITH NO DATA;
CREATE TABLE silver.product_category_name_translation AS TABLE bronze.product_category_name_translation WITH NO DATA;