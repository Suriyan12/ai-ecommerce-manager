import pandas as pd
from crewai.tools import BaseTool


class InventoryTool(BaseTool):
    name: str = "Inventory Checker"
    description: str = "Check product sales frequency to detect fast selling products."

    def _run(self):

        order_items = pd.read_csv("data/order_items.csv")

        inventory = order_items.groupby("product_id").size().reset_index(name="units_sold")

        fast_selling = inventory.sort_values("units_sold", ascending=False).head(10)

        return fast_selling.to_string()