import os
from dotenv import load_dotenv
load_dotenv()


CONFIG = {
    "AWS_ACCESS_KEY": os.getenv("AWS_ACCESS_KEY"),
    "AWS_SECRET_KEY": os.getenv("AWS_SECRET_KEY"),
    "S3_BUCKET": "devansh-etl-bucket",
    "S3_KEY": "raw/new_data.csv",

    "RDS_HOST": os.getenv("RDS_HOST"),
    "RDS_PORT": 3306,
    "RDS_USER": "admin",
    "RDS_PASSWORD": os.getenv("RDS_PASSWORD"),
    "RDS_DB": "etldatabase"
}