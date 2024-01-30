
import os

import snowflake.connector
from llama.fmp.fmp_client import FmpClient


fmp_client = FmpClient()
TICKERS = open("./tickers.txt").read().splitlines()


CONNECT_KWGS = {
    "user": os.environ["SNOWFLAKE_USER"],
    "password": os.environ["SNOWFLAKE_PASSWORD"],
    "account": os.environ["SNOWFLAKE_ACCOUNT"],
    "warehouse": 'COMPUTE_WH',
    "database": 'DEMO',
    "schema": 'bronze',
    "role": "ACCOUNTADMIN"
}

def main():

    # Establish connection parameters
    conn = snowflake.connector.connect(
        **CONNECT_KWGS
    )

    sql = """
        INSERT INTO silver.fundamentals (
            symbol,
            statement_year,
            statement_period, 
            statement_date, 
            revenue, 
            net_income, 
            cash_and_cash_equivalents, 
            total_debt, 
            free_cash_flow,
            dividends_paid 
        )
        SELECT symbol, 
               calendar_year as statement_year, 
               period as statement_period, 
               inc_stmt:date as statement_date, 
               inc_stmt:revenue as revenue, 
               inc_stmt:netIncome as net_income, 
               bs_stmt:cashAndCashEquivalents as cash_and_cash_equivalents, 
               bs_stmt:totalDebt as total_debt, 
               cf_stmt:freeCashFlow as free_cash_flow,
               cf_stmt:dividendsPaid as dividends_paid 
        FROM (
            SELECT inc_stmts.symbol, inc_stmts.calendar_year, inc_stmts.period, PARSE_JSON(inc_stmts.statement) as inc_stmt, PARSE_JSON(bs_stmts.statement) as bs_stmt, PARSE_JSON(cf_stmts.statement) as cf_stmt
            FROM demo.bronze.fmp_income_statements inc_stmts
            JOIN demo.bronze.fmp_balance_sheet_statements bs_stmts
            ON inc_stmts.symbol = bs_stmts.symbol AND inc_stmts.calendar_year = bs_stmts.calendar_year AND inc_stmts.period = bs_stmts.period
            JOIN demo.bronze.fmp_cash_flow_statements cf_stmts
            ON inc_stmts.symbol = cf_stmts.symbol AND inc_stmts.calendar_year = cf_stmts.calendar_year AND inc_stmts.period = cf_stmts.period
        )
    """

    # Execute the copy operation
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

    # Close the connection
    conn.close()

    print("Done.")

if __name__ == "__main__":
    main()
