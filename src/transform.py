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
    
    def typeCast(self, column, data_type):
        """
        Cast a column to a specific data type.
        """
        if data_type == 'Integer':
            self.df = self.df.withColumn(column, self.df[column].cast("Integer"))
        elif data_type == 'String':
            self.df = self.df.withColumn(column, self.df[column].cast("String"))
        elif data_type == 'BigDecimal':
            self.df = self.df.withColumn(column, self.df[column].cast("Decimal(38,2)"))
        elif data_type == 'Date':
            self.df = self.df.withColumn(column, self.df[column].cast("Date"))
        else:
            raise ValueError(f"Data type {data_type} is not supported.")
    
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

    def rename(self, _from, _to):
        """
        Rename columns in a DataFrame.
        """
        self.df = self.df.withColumnRenamed(_from, _to)

    def extraTransform(self, column, transform):
        """
        Perform extra transformation on a column.
        """
        if transform == 'propercase':
            self.df[column] = self.df[column].str.title()
    
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
            if _rule_type == 'pad_zero':
                self.paddingZero(rule['column'], rule['length'])
            elif _rule_type == 'format_number':
                self.formatNumber(rule['column'], rule['format'])
            elif _rule_type == 'rename':
                self.rename(rule['from'], rule['to'])
                self.typeCast(rule['to'], rule['output_type'])
                if "transform" in rule:
                    self.extraTransform(rule['to'], rule['transform'])
            elif _rule_type == 'add':
                self.addConstantCol(rule['column'], rule['value'])
                self.typeCast(rule['column'], rule['output_type'])
            elif _rule_type == 'concatenate':
                self.addConcatCol(rule['column'], rule['sourceColumns'], rule['separator'])
                self.typeCast(rule['column'], rule['output_type'])
            elif _rule_type == 'keep':
                self.keepCols(rule['columns'])

