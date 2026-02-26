import psycopg2
import pandas as pd
from datetime import datetime


# Pipeline ETL pour transformer les données Silver en agrégations analytiques Gold
class SilverToGoldETL:

    def __init__(self, host="localhost", database="Database", user="postgres", password="*****"):
        self.conn_params = {
            'host': host,
            'database': database,
            'user': user,
            'password': password
        }
        self.conn = None

    # Établir la connexion
    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            print("Connexion à PostgreSQL établie")
        except Exception as e:
            print(f"Erreur de connexion: {e}")
            raise

    # Fermer la connexion
    def disconnect(self):
        if self.conn:
            self.conn.close()
            print("Connexion fermée")

    # Créer les tables Gold si elles n'existent pas
    def create_gold_tables(self):
        cur = self.conn.cursor()
        print("\nCréation des tables Gold...")

        # 1. Ventes & revenus par jour et catégorie
        cur.execute("""
            CREATE TABLE IF NOT EXISTS gold.fact_sales_by_category (
                sale_date             DATE,
                product_category      VARCHAR(100),
                total_orders          INTEGER,
                total_items           INTEGER,
                total_revenue         NUMERIC(14, 2),
                total_freight         NUMERIC(14, 2),
                avg_order_value       NUMERIC(10, 2),
                updated_at            TIMESTAMP DEFAULT NOW()
            );
        """)

        # 2. Performance des vendeurs
        cur.execute("""
            CREATE TABLE IF NOT EXISTS gold.fact_seller_performance (
                seller_id             VARCHAR(50),
                seller_city           VARCHAR(100),
                seller_state          VARCHAR(2),
                total_orders          INTEGER,
                total_items_sold      INTEGER,
                total_revenue         NUMERIC(14, 2),
                avg_review_score      NUMERIC(4, 2),
                total_reviews         INTEGER,
                avg_delivery_days     NUMERIC(6, 2),
                updated_at            TIMESTAMP DEFAULT NOW()
            );
        """)

        # 3. Satisfaction clients
        cur.execute("""
            CREATE TABLE IF NOT EXISTS gold.fact_customer_satisfaction (
                review_month          VARCHAR(7),
                product_category      VARCHAR(100),
                avg_review_score      NUMERIC(4, 2),
                total_reviews         INTEGER,
                pct_5_stars           NUMERIC(5, 2),
                pct_1_stars           NUMERIC(5, 2),
                updated_at            TIMESTAMP DEFAULT NOW()
            );
        """)

        # 4. Livraisons & délais
        cur.execute("""
            CREATE TABLE IF NOT EXISTS gold.fact_delivery_performance (
                order_month           VARCHAR(7),
                seller_state          VARCHAR(2),
                customer_state        VARCHAR(2),
                total_orders          INTEGER,
                avg_estimated_days    NUMERIC(6, 2),
                avg_actual_days       NUMERIC(6, 2),
                on_time_deliveries    INTEGER,
                late_deliveries       INTEGER,
                pct_on_time           NUMERIC(5, 2),
                updated_at            TIMESTAMP DEFAULT NOW()
            );
        """)

        self.conn.commit()
        print("  ✓ Tables Gold créées avec succès")

    # ─────────────────────────────────────────────
    # 1. VENTES & REVENUS PAR DATE ET CATÉGORIE
    # ─────────────────────────────────────────────
    def build_fact_sales_by_category(self):
        print("\n" + "=" * 60)
        print("Construction de gold.fact_sales_by_category")
        print("=" * 60)

        query = """
            SELECT
                DATE(o.order_purchase_timestamp)                        AS sale_date,
                COALESCE(t.product_category_name_english, p.product_category_name, 'Unknown') AS product_category,
                COUNT(DISTINCT o.order_id)                              AS total_orders,
                COUNT(oi.order_item_id)                                 AS total_items,
                SUM(oi.price)                                           AS total_revenue,
                SUM(oi.freight_value)                                   AS total_freight,
                ROUND(SUM(oi.price) / COUNT(DISTINCT o.order_id), 2)   AS avg_order_value
            FROM silver.olist_orders o
            JOIN silver.olist_order_items oi ON o.order_id = oi.order_id
            JOIN silver.olist_products p    ON oi.product_id = p.product_id
            LEFT JOIN silver.product_category_name_translation t
                ON p.product_category_name = t.product_category_name
            WHERE o.order_status NOT IN ('canceled', 'unavailable')
            GROUP BY 1, 2
            ORDER BY 1, 2
        """

        df = pd.read_sql(query, self.conn)
        print(f"  → {len(df)} lignes calculées")

        cur = self.conn.cursor()
        cur.execute("TRUNCATE TABLE gold.fact_sales_by_category")

        values = [tuple(x) for x in df.to_numpy()]
        cols = ', '.join(df.columns)
        placeholders = ', '.join(['%s'] * len(df.columns))
        cur.executemany(
            f"INSERT INTO gold.fact_sales_by_category ({cols}) VALUES ({placeholders})",
            values
        )
        self.conn.commit()
        print(f"  ✓ {len(df)} lignes chargées dans gold.fact_sales_by_category")

    # ─────────────────────────────────────────────
    # 2. PERFORMANCE DES VENDEURS
    # ─────────────────────────────────────────────
    def build_fact_seller_performance(self):
        print("\n" + "=" * 60)
        print("Construction de gold.fact_seller_performance")
        print("=" * 60)

        query = """
            SELECT
                s.seller_id,
                s.seller_city,
                s.seller_state,
                COUNT(DISTINCT oi.order_id)         AS total_orders,
                COUNT(oi.order_item_id)              AS total_items_sold,
                ROUND(SUM(oi.price), 2)              AS total_revenue,
                ROUND(AVG(r.review_score), 2)        AS avg_review_score,
                COUNT(r.review_id)                   AS total_reviews,
                ROUND(AVG(
                    EXTRACT(EPOCH FROM (
                        o.order_delivered_customer_date - o.order_purchase_timestamp
                    )) / 86400
                ), 2)                                AS avg_delivery_days
            FROM silver.olist_sellers s
            JOIN silver.olist_order_items oi  ON s.seller_id = oi.seller_id
            JOIN silver.olist_orders o        ON oi.order_id = o.order_id
            LEFT JOIN silver.olist_order_reviews r ON o.order_id = r.order_id
            WHERE o.order_status NOT IN ('canceled', 'unavailable')
            GROUP BY s.seller_id, s.seller_city, s.seller_state
            ORDER BY total_revenue DESC
        """

        df = pd.read_sql(query, self.conn)
        print(f"  → {len(df)} vendeurs calculés")

        cur = self.conn.cursor()
        cur.execute("TRUNCATE TABLE gold.fact_seller_performance")

        values = [tuple(x) for x in df.to_numpy()]
        cols = ', '.join(df.columns)
        placeholders = ', '.join(['%s'] * len(df.columns))
        cur.executemany(
            f"INSERT INTO gold.fact_seller_performance ({cols}) VALUES ({placeholders})",
            values
        )
        self.conn.commit()
        print(f"  ✓ {len(df)} lignes chargées dans gold.fact_seller_performance")

    # ─────────────────────────────────────────────
    # 3. SATISFACTION CLIENTS (REVIEWS)
    # ─────────────────────────────────────────────
    def build_fact_customer_satisfaction(self):
        print("\n" + "=" * 60)
        print("Construction de gold.fact_customer_satisfaction")
        print("=" * 60)

        query = """
            SELECT
                TO_CHAR(r.review_creation_date, 'YYYY-MM')              AS review_month,
                COALESCE(t.product_category_name_english, p.product_category_name, 'Unknown') AS product_category,
                ROUND(AVG(r.review_score), 2)                           AS avg_review_score,
                COUNT(r.review_id)                                       AS total_reviews,
                ROUND(100.0 * SUM(CASE WHEN r.review_score = 5 THEN 1 ELSE 0 END)
                    / COUNT(r.review_id), 2)                            AS pct_5_stars,
                ROUND(100.0 * SUM(CASE WHEN r.review_score = 1 THEN 1 ELSE 0 END)
                    / COUNT(r.review_id), 2)                            AS pct_1_stars
            FROM silver.olist_order_reviews r
            JOIN silver.olist_orders o        ON r.order_id = o.order_id
            JOIN silver.olist_order_items oi  ON o.order_id = oi.order_id
            JOIN silver.olist_products p      ON oi.product_id = p.product_id
            LEFT JOIN silver.product_category_name_translation t
                ON p.product_category_name = t.product_category_name
            WHERE r.review_creation_date IS NOT NULL
            GROUP BY 1, 2
            ORDER BY 1, 2
        """

        df = pd.read_sql(query, self.conn)
        print(f"  → {len(df)} lignes calculées")

        cur = self.conn.cursor()
        cur.execute("TRUNCATE TABLE gold.fact_customer_satisfaction")

        values = [tuple(x) for x in df.to_numpy()]
        cols = ', '.join(df.columns)
        placeholders = ', '.join(['%s'] * len(df.columns))
        cur.executemany(
            f"INSERT INTO gold.fact_customer_satisfaction ({cols}) VALUES ({placeholders})",
            values
        )
        self.conn.commit()
        print(f"  ✓ {len(df)} lignes chargées dans gold.fact_customer_satisfaction")

    # ─────────────────────────────────────────────
    # 4. LIVRAISONS & DÉLAIS
    # ─────────────────────────────────────────────
    def build_fact_delivery_performance(self):
        print("\n" + "=" * 60)
        print("Construction de gold.fact_delivery_performance")
        print("=" * 60)

        query = """
            SELECT
                TO_CHAR(o.order_purchase_timestamp, 'YYYY-MM')  AS order_month,
                s.seller_state,
                c.customer_state,
                COUNT(DISTINCT o.order_id)                      AS total_orders,
                ROUND(AVG(
                    EXTRACT(EPOCH FROM (
                        o.order_estimated_delivery_date - o.order_purchase_timestamp
                    )) / 86400
                ), 2)                                           AS avg_estimated_days,
                ROUND(AVG(
                    EXTRACT(EPOCH FROM (
                        o.order_delivered_customer_date - o.order_purchase_timestamp
                    )) / 86400
                ), 2)                                           AS avg_actual_days,
                SUM(CASE
                    WHEN o.order_delivered_customer_date <= o.order_estimated_delivery_date
                    THEN 1 ELSE 0
                END)                                            AS on_time_deliveries,
                SUM(CASE
                    WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date
                    THEN 1 ELSE 0
                END)                                            AS late_deliveries,
                ROUND(100.0 * SUM(CASE
                    WHEN o.order_delivered_customer_date <= o.order_estimated_delivery_date
                    THEN 1 ELSE 0
                END) / COUNT(DISTINCT o.order_id), 2)          AS pct_on_time
            FROM silver.olist_orders o
            JOIN silver.olist_order_items oi ON o.order_id = oi.order_id
            JOIN silver.olist_sellers s       ON oi.seller_id = s.seller_id
            JOIN silver.olist_customers c     ON o.customer_id = c.customer_id
            WHERE o.order_status = 'delivered'
              AND o.order_delivered_customer_date IS NOT NULL
            GROUP BY 1, 2, 3
            ORDER BY 1, 2, 3
        """

        df = pd.read_sql(query, self.conn)
        print(f"  → {len(df)} lignes calculées")

        cur = self.conn.cursor()
        cur.execute("TRUNCATE TABLE gold.fact_delivery_performance")

        values = [tuple(x) for x in df.to_numpy()]
        cols = ', '.join(df.columns)
        placeholders = ', '.join(['%s'] * len(df.columns))
        cur.executemany(
            f"INSERT INTO gold.fact_delivery_performance ({cols}) VALUES ({placeholders})",
            values
        )
        self.conn.commit()
        print(f"  ✓ {len(df)} lignes chargées dans gold.fact_delivery_performance")

    # ─────────────────────────────────────────────
    # PIPELINE COMPLET
    # ─────────────────────────────────────────────
    def run_full_pipeline(self):
        print("\n" + "=" * 60)
        print("DÉMARRAGE DU PIPELINE SILVER → GOLD")
        print("=" * 60)

        start_time = datetime.now()

        try:
            self.connect()
            self.create_gold_tables()

            self.build_fact_sales_by_category()
            self.build_fact_seller_performance()
            self.build_fact_customer_satisfaction()
            self.build_fact_delivery_performance()

            duration = (datetime.now() - start_time).total_seconds()

            print("\n" + "=" * 60)
            print("PIPELINE TERMINÉ AVEC SUCCÈS")
            print(f"Durée totale: {duration:.2f} secondes")
            print("=" * 60)

        except Exception as e:
            print(f"\n✗ ERREUR PIPELINE: {e}")

        finally:
            self.disconnect()


if __name__ == "__main__":
    etl = SilverToGoldETL(
        host="localhost",
        database="Database",
        user="postgres",
        password="*****"
    )
    etl.run_full_pipeline()
