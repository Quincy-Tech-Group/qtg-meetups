
import os
import json
from tqdm import tqdm
from snowflake.snowpark.functions import when_matched, when_not_matched
from snowflake.snowpark import Session

from llama.fmp.fmp_client import FmpClient


fmp_client = FmpClient()
TICKERS = open("./tickers.txt").read().splitlines()


CONNECT_KWGS = {
    "user": os.environ["SNOWFLAKE_USER"],
    "password": os.environ["SNOWFLAKE_PASSWORD"],
    "account": os.environ["SNOWFLAKE_ACCOUNT"],
    "warehouse": 'COMPUTE_WH',
    "database": 'LLAMA',
    "schema": 'bronze',
    "role": "ACCOUNTADMIN"
}

def main():
    with Session.builder.configs(CONNECT_KWGS).create() as session:
        for sym in tqdm(TICKERS):
            try:
                income_statements = fmp_client.get_income_statements(sym)
                balance_sheet_statements = fmp_client.get_balance_sheet_statements(sym)
                cash_flow_statements = fmp_client.get_cash_flow_statements(sym)

                # pprint(income_statements[0])
                # pprint(balance_sheet_statements[0])
                # pprint(cash_flow_statements[0])
                # exit(0)

                table_statements = {
                    "fmp_income_statements": income_statements,
                    "fmp_balance_sheet_statements": balance_sheet_statements,
                    "fmp_cash_flow_statements": cash_flow_statements
                }

                for table, statements in table_statements.items():
                    items = [
                        {
                            "symbol": statement["symbol"],
                            "calendar_year": statement["calendarYear"],
                            "period": statement["period"],
                            "accepted_datetime": statement["acceptedDate"],
                            "statement": json.dumps(statement)
                        }
                        for statement in statements
                    ]

                    source = session.create_dataframe(items)

                    target = session.table(table)
                    join_expr = (target["symbol"] == source["symbol"]) & (target["calendar_year"] == source["calendar_year"]) & (target["period"] == source["period"]) & (target["accepted_datetime"] == source["accepted_datetime"])
                    target.merge(
                        source,
                        join_expr,
                        [when_not_matched().insert(source)]
                    )
            except Exception as e:
                print(e)

        print("Done.")

if __name__ == "__main__":
    main()