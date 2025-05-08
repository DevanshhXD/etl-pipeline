import os
import sys
import io
import boto3
import mysql.connector
import pandas as pd
from config.config import CONFIG


def extract_from_s3():
    print("🔍 Extracting file from S3...")
    s3 = boto3.client(
        's3',
        aws_access_key_id=CONFIG["AWS_ACCESS_KEY"],
        aws_secret_access_key=CONFIG["AWS_SECRET_KEY"]
    )
    obj = s3.get_object(Bucket=CONFIG["S3_BUCKET"], Key=CONFIG["S3_KEY"])
    df = pd.read_csv(io.BytesIO(obj['Body'].read()))
    print("✅ Extracted Data:")
    print(df.head())
    return df


def transform_data(df):
    print("🔧 Transforming data...")
    df['total_price'] = df['quantity'] * df['price']
    return df


def load_to_mysql(df):
    print("🛢️ Loading data to RDS MySQL...")
    conn = mysql.connector.connect(
        host=CONFIG["RDS_HOST"],
        user=CONFIG["RDS_USER"],
        password=CONFIG["RDS_PASSWORD"],
        database=CONFIG["RDS_DB"],
        port=CONFIG["RDS_PORT"]
    )
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales_data (
            order_id INT,
            product VARCHAR(50),
            quantity INT,
            price FLOAT,
            date DATE,
            total_price FLOAT
        )
    """)
    conn.commit()

    # Insert rows
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO sales_data (order_id, product,
                        quantity, price, date, total_price)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, tuple(row))

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Load complete!")


def main():
    df = extract_from_s3()
    df = transform_data(df)
    load_to_mysql(df)


if __name__ == "__main__":
    main()
