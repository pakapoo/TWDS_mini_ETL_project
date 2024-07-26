## About
Take home project for 2024 Taiwan Data Science Meetup (TWDS) mentorship program. The project demonstated building an ETL (Extract, Transform, Load) pipeline, orchestrated with Airflow, and delivered as Docker compose file. 

Data is provided as csv files (pseudo-regex or number parsing format), processed with Spark (PySpark), and stored to MySQL database.

**Pipeline archetecture**

File system -> Python runtime on Linux (pyspark) -> MySQL

## Scenario
We are implementing a small system for (row-wise) wrangling of text data. The typical use case is taking a delimited data file from a customer and massaging it to fit with a standardized schema by applying a sequence of column transforms.

## Setup
1. CLone the repo to your desktop.
2. Place the input csv file(s) in `data/input`. There are already one available. Feel free to put additional csv files or modify the existing one.
3. For data quality checking, configure input schema in `config/input_schema`. The application will check the real data against the regular expression provided for each column.
* column: the column name
* format: regular expression for the expected value
4. Configure external DSL for the transformation steps in `config/transform_rules.yaml`. There are several rules (rule_type) available now:

    #### Create column
    * rename: create column from renaming a column
        * from: source column
        * to: target column
        * output_type: target column type
        * transform (optional): additional operation, e.g. proper case
    * concatenate: create column from concatenating columns
        * column: column
        * sourceColumns: list of columns to be concatenated
        * separator: separator when joining the sourceColumns
        * output_type: target column type
    * add: create column with a fixed value
        * column: column
        * value: fix value
        * output_type: target column type

    #### Format column
    * pad_zero: pad zeros with the given length
        * column: column (String)
        * length: length
    * format_number: format a numeric column
        * column: column
        * format: [Spark SQL - Number Pattern](https://spark.apache.org/docs/3.3.1/sql-ref-number-pattern.html)

    #### Dataframe operations
    * keep
        * columns: list of columns to be kept

## Installation
Run the below command(s) to start a Python environment and MySQL database. The -d parameter will allow the application to run in the background (detach mode) of the same session.
```bash
docker-compose up -d
```

## Result
You may find the ETL result at `data/output` and the report for logging invalid data at `reports`. The result will also be stored in MySQL database, which can be checked with the following command(s):
```bash

```

## Data Schema
**Input (csv)**
| Column Name     | String Format |
|-----------------|---------------|
| Order Number    | d+            |
| Year            | YYYY          |
| Month           | MM            |
| Day             | dd            |
| Product Number  | [A-Z0-9]+     |
| Product Name    | [A-Z]+        |
| Count           | #,##0.0#      |
| Extra Col1      | --            |
| Extra Col2      | --            |


**Output**
| Column Name | Data Type    | Source            | Action   |
|-------------|--------------|-------------------|----------|
| OrderID     | Integer      | Order Number      | Rename   |
| OrderDate   | DateTime     | Year+Month+Day    | Add      |
| ProductId   | String       | Product Number    | Rename   |
| ProductName | String       | Product Name      | Proper Case, Rename |
| Quantity    | BigDecimal   | Count             | Rename   |
| Unit        | String       | "kg"              | Add      |

## Requirements
* The transformations should be configurable with an external DSL (like a configuration file).

    -> An external YAML file for easy configuration without writing code

* The functionality should be implemented as a library, without (significant) external dependencies.

    -> Implement each functionality as a standalone library, including data extraction, data quality checking, data transformation and data loading

* Invalid rows should be collected, with errors describing why they are invalid (logging them is fine for now).

    -> Collect invalid rows and provide error descriptions by implementing type checking and reporting

* The data tables can have a very large number of rows.

    -> Consider implementing additional data simulation functions to efficiently handle large data tables

## Assumptions
* Each output column should be configured exactly once with the 'Create column' rule in `config/transform_rules.yaml`. You can find more details about the 'Create column' rule in the [previous section](#create-column).
* Regular expressions are updated according to the sample data
    * Product Number: allow dashes (-)
    * Product Name: allow spaces

## Todo
* Output to a database that can store JVM type data
* Leverage cloud technologies such as S3 for placing input data

## Reference
1. Wang, Y., & Zhang, Y. (2017). A Design of ETL Pipeline for Data Warehouse. In *2017 7th International Workshop on Computer Science and Engineering* (pp. 41-45). IEEE. [Link](http://www.wcse.org/WCSE_2017/041.pdf)