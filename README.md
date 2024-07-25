## About
This is the take home project of Taiwan Data Science Meetup (TWDS) mentorship program.

The data is extracted from csv files (pseudo-regex or number parsing format) and stored to MySQL database. The project is packed and delivered with **Docker**.

### Pipeline archetecture
Amazon S3 -> Python -> MySQL

## Setup
1. Unzip the code
2. Place input csv file(s) in `data/input`
3. Configure input schema in `config/input_schema`
* column: the column name
* format: regular expression for data quality checking
4. Configure external DSL for transformation steps in `config/transform_rules.yaml`. There are several rules (rule_type) available now:

    **Create new column**
    * rename: create column from renaming a column
        * from: source column
        * to: target column
        * output_type: target column type
    * concatenate: create column from concatenating columns
        * column: column
        * sourceColumns: list of columns to be concatenated
        * separator: separator when joining the sourceColumns
        * output_type: target column type
    * add: create column with a fixed value
        * column: column
        * value: fix value
        * output_type: target column type

    **Format column**
    * pad_zero: pad zeros with the given length
        * column: column (String)
        * length: length
    * format_number: format a numeric column
        * column: column
        * format: [Spark SQL - Number Pattern](https://spark.apache.org/docs/3.3.1/sql-ref-number-pattern.html)

    **Dataframe operations**
    * keep
        * columns: list of columns to be kept
5. Run the below command(s) to start a Python environment
```bash
docker-compose up
```
6. You may find the ETL result at `data/output` and report for logging invalid data at `reports`

## Data
### Input
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


### Output

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

    -> To make the transformations configurable, utilize an external YAML file for easy configuration and modification.

* The functionality should be implemented as a library, without (significant) external dependencies.

    -> Implement the functionality as a standalone library, minimizing the reliance on external dependencies.

* Invalid rows should be collected, with errors describing why they are invalid (logging them is fine for now).

    -> Collect invalid rows and provide error descriptions by implementing type checking and reporting.

* The data tables can have a very large number of rows.

    -> Consider implementing additional data simulation functions to efficiently handle large data tables.


## Implementations
1. Set up a Python environment and JVM-style DB with Docker compose
    -> Use Docker Compose for easy set-up for users

2. Develop Python script (library) to do the transformation

3. Develop Python script (library) to simulate data
    -> As the requirements mentioned that the data can be large

4. Set pre-checking rules with a configuration file

5. Set post-checking validation rules

## Assumption
* Each output column can at most appear once in `config/transform_rules.yaml`
* Regular expressions
    * Product Number: allow dashes (-)
    * Product Name: allow spaces

## Future
* Store output into a database that can store JVM type data
* Leverage cloud technologies such as S3 for placing input data

## Reference
1. Wang, Y., & Zhang, Y. (2017). A Design of ETL Pipeline for Data Warehouse. In *2017 7th International Workshop on Computer Science and Engineering* (pp. 41-45). IEEE. [Link](http://www.wcse.org/WCSE_2017/041.pdf)