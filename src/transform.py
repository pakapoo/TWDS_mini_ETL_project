import yaml
from pyspark.sql.functions import lit, concat_ws, col, lpad, to_number 

class transformer:
    def __init__(self, df):
        self.df = df

    def parseRules(self, file):
        """
        Parse rules from a YAML file.
        """
        with open(file, 'r') as f:
            rules = yaml.load(f, Loader=yaml.SafeLoader)
        return rules
    
    def paddingZero(self, column, length):
        """
        Pad zeros to the left of a column.
        """
        self.df = self.df.withColumn(column, lpad(col(column), length, '0'))

    def formatNumber(self, column, format):
        """
        Format a number in a column.
        """
        self.df = self.df.withColumn(column, to_number(col(column), lit(format)))

    def rename(self, _from, _to, transform=None):
        """
        Rename columns in a DataFrame.
        """
        self.df = self.df.withColumnRenamed(_from, _to)
        if transform == 'propercase':
            self.df[_to] = self.df[_to].str.title()
    
    def addConstantCol(self, column, value):
        """
        Add a column to a DataFrame.
        """
        self.df = self.df.withColumn(column, lit(value))

    def addConcatCol(self, column_name, columns, separator):
        """
        Add a column to a DataFrame.
        """
        self.df = self.df.withColumn(column_name, concat_ws(separator, *columns))

    def keepCols(self, columns):
        """
        Reorder columns in a DataFrame.
        """
        self.df = self.df.select(columns)

    def transform(self, rules):
        """
        Process all rules.
        """
        rules = self.parseRules(rules)['transformation']
        for rule in rules:
            _rule_type = rule['rule_type']
            if _rule_type == 'padding_zero':
                self.paddingZero(rule['column'], rule['length'])
            elif _rule_type == 'format_number':
                self.formatNumber(rule['column'], rule['format'])
            elif _rule_type == 'rename':
                if "transform" in rule:
                    self.rename(rule['from'], rule['to'], rule['transform'])
                else:
                    self.rename(rule['from'], rule['to'])
            elif _rule_type == 'add':
                self.addConstantCol(rule['column'], rule['value'])
            elif _rule_type == 'concatenate':
                self.addConcatCol(rule['column'], rule['sourceColumns'], rule['separator'])
            elif _rule_type == 'keep':
                self.keepCols(rule['columns'])

