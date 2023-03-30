from typing import Dict
from clickhouse_driver import Client
from clickhouse_pool import ChPool
import os

pool = ChPool(
    host=os.getenv("CLICKHOUSE_HOST", "localhost"),
    database=os.getenv("CLICKHOUSE_DATABASE", "default"),
    secure=os.getenv("CLICKHOUSE_SECURE", ""),
    user=os.getenv("CLICKHOUSE_USER", "default"),
    password=os.getenv("CLICKHOUSE_PASSWORD", ""),
    ca_certs=os.getenv("CLICKHOUSE_CA", None),
    verify=os.getenv("CLICKHOUSE_VERIFY", True),
    settings={"max_result_rows": "10000"}, 
)
    

def run_query(query: str, params: Dict[str, str | int] = {}, settings: Dict[str, str | int] = {}):
    with pool.get_client() as client:
        result = client.execute(query % (params or {}), settings=settings, with_column_types=True)
        response = []
        for res in result[0]:
            item = {}
            for index, key in enumerate(result[1]):
                item[key[0]] = res[index]
            
            response.append(item)
        return response

base_params = {
    "cluster": os.getenv("CLICKHOUSE_CLUSTER", "posthog")
}
