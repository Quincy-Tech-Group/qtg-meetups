
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
    "schema": 'gold',
    "role": "ACCOUNTADMIN"
}

def main():

    # Establish connection parameters
    conn = snowflake.connector.connect(
        **CONNECT_KWGS
    )

    sql = """
        INSERT INTO gold.metrics (
            symbol,
            statement_year,
            revenue_growth, 
            debt_to_cash
        )
        SELECT 
            symbol,
            statement_date,
            revenue / LAG(revenue, 4) OVER (PARTITION BY symbol ORDER BY statement_date)-1 AS revenue_growth,
            total_debt / cash_and_cash_equivalents as debt_to_cash
        FROM 
            demo.silver.fundamentals
        ORDER BY 
            symbol, statement_date;
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
