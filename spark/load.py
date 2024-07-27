def dump_df_to_db(df, DB_USER, DB_PASSWORD, DB_NAME, DB_TABLE):
    print(DB_NAME, DB_TABLE, DB_USER, DB_PASSWORD)
    df.write \
    .format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/"+DB_NAME) \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .option("dbtable", DB_TABLE) \
    .option("user", DB_USER) \
    .option("password", DB_PASSWORD) \
    .mode("overwrite") \
    .save()

