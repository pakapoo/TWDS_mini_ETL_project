import os
import configparser
# Custom library
import extract
import check
import transform

# Set working directory
current_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.abspath(os.path.join(current_dir, '../'))
os.chdir(base_dir)

# Read config file
config = configparser.ConfigParser()
config_path = os.path.join(base_dir, 'config/config.ini')
config.read(config_path)
data_souce = config['path']['source']
input_schema = config['path']['schema']
transformation_rules = config['path']['rules']
ETL_output = config['path']['output']
dq_report = config['path']['report']

# Extract
df = extract.readcsv(data_souce)
print(df.show(20, False), df.printSchema())

# Data Quality Check
typeChecker = check.typeChecker(df)
typeChecker.checker(input_schema)
typeChecker.logger(dq_report)
print(typeChecker.valid_df.show(20, False), typeChecker.invalid_df.show(20, False))

# Transform
transformer = transform.transformer(typeChecker.valid_df)
transformer.transform(transformation_rules, ETL_output)
print(transformer.df.show(20, False), transformer.df.printSchema())
