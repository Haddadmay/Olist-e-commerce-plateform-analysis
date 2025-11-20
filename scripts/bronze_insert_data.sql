CREATE OR REPLACE PROCEDURE bronze.insert_data()
LANGUAGE plpgsql
AS $$
BEGIN
    -- Geolocation
    TRUNCATE TABLE bronze.olist_geolocation;
    EXECUTE 
	'COPY bronze.olist_geolocation FROM'
	'C:/Users/Ayoub/Desktop/dataset/olist_geolocation_dataset.csv'
	'WITH (FORMAT CSV, HEADER true, DELIMITER '';'')';
    RAISE NOTICE 'olist_geolocation importé';

    -- Product category translation
    TRUNCATE TABLE bronze.product_category_name_translation;
    EXECUTE 'COPY bronze.product_category_name_translation FROM'
	'C:/Users/Ayoub/Desktop/dataset/product_category_name_translation.csv'
	'WITH (FORMAT CSV, HEADER true, DELIMITER '';'')';
    RAISE NOTICE 'product_category_name_translation importé';

    -- Customers
    TRUNCATE TABLE bronze.olist_customers;
    EXECUTE 'COPY bronze.olist_customers FROM'
	'C:/Users/Ayoub/Desktop/dataset/olist_customers_dataset.csv'
	'WITH (FORMAT CSV, HEADER true, DELIMITER '';'')';
    RAISE NOTICE 'olist_customers importé';

    -- Sellers
    TRUNCATE TABLE bronze.olist_sellers;
    EXECUTE 'COPY bronze.olist_sellers FROM'
	'C:/Users/Ayoub/Desktop/dataset/olist_sellers_dataset.csv'
	'WITH (FORMAT CSV, HEADER true, DELIMITER '';'')';
    RAISE NOTICE 'olist_sellers importé';

    -- Products
    TRUNCATE TABLE bronze.olist_products;
    EXECUTE 'COPY bronze.olist_products FROM'
	'C:/Users/Ayoub/Desktop/dataset/olist_products_dataset.csv'
	'WITH (FORMAT CSV, HEADER true, DELIMITER '';'')';
    RAISE NOTICE 'olist_products importé';

    -- Orders
    TRUNCATE TABLE bronze.olist_orders;
    EXECUTE 'COPY bronze.olist_orders FROM'
	'C:/Users/Ayoub/Desktop/dataset/olist_orders_dataset.csv'
	'WITH (FORMAT CSV, HEADER true, DELIMITER '';'')';
    RAISE NOTICE 'olist_orders importé';

    -- Order items
    TRUNCATE TABLE bronze.olist_order_items;
    EXECUTE 'COPY bronze.olist_order_items FROM'
	'C:/Users/Ayoub/Desktop/dataset/olist_order_items_dataset.csv'
	'WITH (FORMAT CSV, HEADER true, DELIMITER '';'')';
    RAISE NOTICE 'olist_order_items importé';

    -- Order payments
    TRUNCATE TABLE bronze.olist_order_payments;
    EXECUTE 'COPY bronze.olist_order_payments FROM'
	'C:/Users/Ayoub/Desktop/dataset/olist_order_payments_dataset.csv'
	'WITH (FORMAT CSV, HEADER true, DELIMITER '';'')';
    RAISE NOTICE 'olist_order_payments importé';

    -- Order reviews
    TRUNCATE TABLE bronze.olist_order_reviews;
    EXECUTE 'COPY bronze.olist_order_reviews FROM'
	'C:/Users/Ayoub/Desktop/dataset/olist_order_reviews_dataset.csv'
	'WITH (FORMAT CSV, HEADER true, DELIMITER '';'')';
    RAISE NOTICE 'olist_order_reviews importé';

    RAISE NOTICE '✓ Toutes les tables ont été importées avec succès';

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Erreur lors de l''import: %', SQLERRM;
END;
$$;

CALL bronze.insert_data();