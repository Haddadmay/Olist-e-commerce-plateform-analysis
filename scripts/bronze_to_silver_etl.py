import psycopg2
import pandas as pd
from datetime import datetime
import numpy as np


#Pipeline ETL pour nettoyer les données Bronze et les charger dans Silver
class BronzeToSilverETL:
    
    def __init__(self, host="localhost", database="Database", user="postgres", password="*****"):
        self.conn_params = {
            'host': host,
            'database': database,
            'user': user,
            'password': password
        }
        self.conn = None

    #Établir la connexion    
    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            print("Connexion à PostgreSQL établie")
        except Exception as e:
            print(f"Erreur de connexion: {e}")
            raise
    
    #"""Fermer la connexion"""
    def disconnect(self):
        if self.conn:
            self.conn.close()
            print("Connexion fermée")
    
    #Extraire les données d'une table Bronze
    def extract_from_bronze(self, table_name):
        try:
            query = f"SELECT * FROM bronze.{table_name}"
            df = pd.read_sql(query, self.conn)
            print(f" Extraction de bronze.{table_name}: {len(df)} lignes")
            return df
        except Exception as e:
            print(f"✗ Erreur extraction {table_name}: {e}")
            return None
    
    #Nettoyer la table olist_geolocation
    def clean_geolocation(self, df):
        print("Nettoyage geolocation...")
        
        # Supprimer les doublons
        df = df.drop_duplicates()
        
        # Supprimer les lignes avec coordonnées manquantes
        df = df.dropna(subset=['geolocation_lat', 'geolocation_lng'])
        
        # Filtrer les coordonnées aberrantes (Brésil: lat -34 à 5, lng -74 à -34)
        df = df[(df['geolocation_lat'] >= -34) & (df['geolocation_lat'] <= 5)]
        df = df[(df['geolocation_lng'] >= -74) & (df['geolocation_lng'] <= -34)]
        
        # Nettoyer le zip code (enlever espaces, mettre en uppercase)
        df['geolocation_zip_code_prefix'] = df['geolocation_zip_code_prefix'].astype(str).str.strip()
        
        print(f"Nettoyage terminé: {len(df)} lignes conservées")
        return df
    
    #Nettoyer la table olist_customers
    def clean_customers(self, df):
        print("Nettoyage customers...")
        
        # Supprimer les doublons
        df = df.drop_duplicates(subset=['customer_id'])
        
        # Supprimer les lignes avec customer_id manquant
        df = df.dropna(subset=['customer_id'])
        
        # Nettoyer et standardiser les noms de villes/états
        df['customer_city'] = df['customer_city'].str.strip().str.title()
        df['customer_state'] = df['customer_state'].str.strip().str.upper()
        
        # Nettoyer le zip code
        df['customer_zip_code_prefix'] = df['customer_zip_code_prefix'].astype(str).str.strip()
        
        print(f"  ✓ Nettoyage terminé: {len(df)} lignes conservées")
        return df
    
    #Nettoyer la table olist_sellers
    def clean_sellers(self, df):
        print("Nettoyage sellers...")
        
        # Supprimer les doublons
        df = df.drop_duplicates(subset=['seller_id'])
        
        # Supprimer les lignes avec seller_id manquant
        df = df.dropna(subset=['seller_id'])
        
        # Nettoyer et standardiser
        df['seller_city'] = df['seller_city'].str.strip().str.title()
        df['seller_state'] = df['seller_state'].str.strip().str.upper()
        df['seller_zip_code_prefix'] = df['seller_zip_code_prefix'].astype(str).str.strip()
        
        print(f"  ✓ Nettoyage terminé: {len(df)} lignes conservées")
        return df
    
    #Nettoyer la table olist_products
    def clean_products(self, df):
        print("Nettoyage products")
        
        # Supprimer les doublons
        df = df.drop_duplicates(subset=['product_id'])
        
        # Supprimer les lignes avec product_id manquant
        df = df.dropna(subset=['product_id'])
        
        # Remplacer les valeurs manquantes dans les dimensions par 0
        dimension_cols = ['product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm']
        for col in dimension_cols:
            if col in df.columns:
                df[col] = df[col].fillna(0)
        
        # Supprimer les produits avec des dimensions négatives
        for col in dimension_cols:
            if col in df.columns:
                df = df[df[col] >= 0]
        
        print(f"Nettoyage terminé: {len(df)} lignes conservées")
        return df
    
    #Nettoyer la table olist_orders
    def clean_orders(self, df):
        print("Nettoyage orders...")
        
        # Supprimer les doublons
        df = df.drop_duplicates(subset=['order_id'])
        
        # Supprimer les lignes avec order_id ou customer_id manquant
        df = df.dropna(subset=['order_id', 'customer_id'])
        
        # Convertir les dates en datetime
        date_columns = ['order_purchase_timestamp', 'order_approved_at', 
                       'order_delivered_carrier_date', 'order_delivered_customer_date',
                       'order_estimated_delivery_date']
        
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Supprimer les commandes avec des dates incohérentes
        if 'order_delivered_customer_date' in df.columns and 'order_purchase_timestamp' in df.columns:
            df = df[(df['order_delivered_customer_date'].isna()) | 
                   (df['order_delivered_customer_date'] >= df['order_purchase_timestamp'])]
        
        print(f"Nettoyage terminé: {len(df)} lignes conservées")
        return df
    
    #Nettoyer la table olist_order_items
    def clean_order_items(self, df):
        print("Nettoyage order_items...")
        
        # Supprimer les doublons
        df = df.drop_duplicates(subset=['order_id', 'order_item_id'])
        
        # Supprimer les lignes avec IDs manquants
        df = df.dropna(subset=['order_id', 'product_id', 'seller_id'])
        
        # Supprimer les prix négatifs ou nuls
        df = df[df['price'] > 0]
        
        # Remplacer les frais de livraison négatifs par 0
        if 'freight_value' in df.columns:
            df.loc[df['freight_value'] < 0, 'freight_value'] = 0
        
        # Convertir les dates
        if 'shipping_limit_date' in df.columns:
            df['shipping_limit_date'] = pd.to_datetime(df['shipping_limit_date'], errors='coerce')
        
        print(f"Nettoyage terminé: {len(df)} lignes conservées")
        return df
    
    #Nettoyer la table olist_order_payments
    def clean_order_payments(self, df):
        print("Nettoyage order_payments...")
        
        # Supprimer les doublons
        df = df.drop_duplicates()
        
        # Supprimer les lignes avec order_id manquant
        df = df.dropna(subset=['order_id'])
        
        # Supprimer les paiements avec valeur négative ou nulle
        df = df[df['payment_value'] > 0]
        
        # Standardiser les types de paiement
        if 'payment_type' in df.columns:
            df['payment_type'] = df['payment_type'].str.strip().str.lower()
        
        print(f"  ✓ Nettoyage terminé: {len(df)} lignes conservées")
        return df
    
    #Nettoyer la table olist_order_reviews
    def clean_order_reviews(self, df):
        print("Nettoyage order_reviews...")
        
        # Supprimer les doublons
        df = df.drop_duplicates(subset=['review_id'])
        
        # Supprimer les lignes avec review_id ou order_id manquant
        df = df.dropna(subset=['review_id', 'order_id'])
        
        # S'assurer que le score est entre 1 et 5
        if 'review_score' in df.columns:
            df = df[(df['review_score'] >= 1) & (df['review_score'] <= 5)]
        
        # Convertir les dates
        date_cols = ['review_creation_date', 'review_answer_timestamp']
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Remplacer les commentaires vides par NULL
        if 'review_comment_message' in df.columns:
            df['review_comment_message'] = df['review_comment_message'].replace('', None)
        
        print(f"  ✓ Nettoyage terminé: {len(df)} lignes conservées")
        return df
    
    #Charger les données nettoyées dans Silver
    def load_to_silver(self, df, table_name):
        try:
            cur = self.conn.cursor()
            
            # Vider la table Silver
            cur.execute(f"TRUNCATE TABLE silver.{table_name} CASCADE")
            
            # Insérer les données
            # Convertir le DataFrame en liste de tuples
            columns = df.columns.tolist()
            values = [tuple(x) for x in df.to_numpy()]
            
            # Créer la requête d'insertion
            cols_str = ', '.join(columns)
            placeholders = ', '.join(['%s'] * len(columns))
            insert_query = f"INSERT INTO silver.{table_name} ({cols_str}) VALUES ({placeholders})"
            
            # Insertion en batch
            cur.executemany(insert_query, values)
            self.conn.commit()
            
            print(f"Chargement dans silver.{table_name}: {len(df)} lignes insérées")
            
        except Exception as e:
            self.conn.rollback()
            print(f"Erreur chargement {table_name}: {e}")
    
    #Pipeline complet pour une table: Extract → Clean → Load
    def process_table(self, table_name, clean_function):
        print(f"\n{'='*60}")
        print(f"Traitement de {table_name}")
        print(f"{'='*60}")
        
        # Extract
        df = self.extract_from_bronze(table_name)
        if df is None or df.empty:
            print(f"✗ Aucune donnée à traiter pour {table_name}")
            return
        
        # Transform (Clean)
        df_clean = clean_function(df)
        
        # Load
        self.load_to_silver(df_clean, table_name)
    
    #Exécuter le pipeline complet pour toutes les tables
    def run_full_pipeline(self):
        print("\n" + "="*60)
        print("DÉMARRAGE DU PIPELINE BRONZE → SILVER")
        print("="*60)
        
        start_time = datetime.now()
        
        try:
            self.connect()
            
            # Définir les tables et leurs fonctions de nettoyage
            tables = [
                ('olist_geolocation', self.clean_geolocation),
                ('olist_customers', self.clean_customers),
                ('olist_sellers', self.clean_sellers),
                ('olist_products', self.clean_products),
                ('olist_orders', self.clean_orders),
                ('olist_order_items', self.clean_order_items),
                ('olist_order_payments', self.clean_order_payments),
                ('olist_order_reviews', self.clean_order_reviews),
            ]
            
            # Traiter chaque table
            for table_name, clean_func in tables:
                self.process_table(table_name, clean_func)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            print("\n" + "="*60)
            print(f"PIPELINE TERMINÉ AVEC SUCCÈS")
            print(f"Durée totale: {duration:.2f} secondes")
            print("="*60)
            
        except Exception as e:
            print(f"\n ERREUR PIPELINE: {e}")
        
        finally:
            self.disconnect()



if __name__ == "__main__":
    # Configuration de la connexion
    etl = BronzeToSilverETL(
        host="localhost",
        database="Database",
        user="postgres",
        password="*****"
    )
    
    # Exécuter le pipeline complet
    etl.run_full_pipeline()
