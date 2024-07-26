import yaml
from pyspark.sql.functions import lit, col, when
from datetime import datetime
import os

class typeChecker:
    def __init__(self, df, valid_df=None, invalid_df=None):
        self.df = df
        self.valid_df = valid_df
        self.invalid_df = invalid_df

    def parseSchema(self, file):
        """
        Parse rules from a YAML file.
        """
        with open(file, 'r') as f:
            rules = yaml.load(f, Loader=yaml.SafeLoader)
        return rules
    
    def checkType(self, column, regex):
        """
        Check if a column matches a regex pattern.
        """
        self.df = self.df.withColumn('error', when(~col(column).rlike(regex), 1).otherwise(col('error')))
        temp_error_df = self.df.filter(~col(column).rlike(regex))
        temp_error_df = temp_error_df.withColumn('error', lit("unmatched regex - "+column))
        if self.invalid_df is None:
            self.invalid_df = temp_error_df
        else:
            self.invalid_df = self.invalid_df.union(temp_error_df)
        return self.df.filter(~col(column).rlike(regex)).count()
    
    def checker(self, rules):
        """
        Process all rules.
        """
        rules = self.parseSchema(rules)['inputSchema']
        self.df = self.df.withColumn('error', lit(0))
        for rule in rules:
            _col = rule['column']
            _format = rule['format']
            if self.checkType(_col, _format) > 0:
                print(f"Column {_col} has failed the test.")
            else:
                print(f"Column {_col} has passed the test.")
        self.valid_df = self.df.filter(col('error') == 0)
        self.valid_df = self.valid_df.drop('error')

    def logger(self, report):
        """
        Log the results to a file.
        """
        error_file_nm = "error_{date}.csv".format(date=datetime.now().strftime("%Y%m%d"))
        self.invalid_df.toPandas().to_csv(os.path.join(report, error_file_nm), 
                                          header=True,
                                          index=False)
        return None