import pandas as pd
from crewai.tools import BaseTool


class SalesAnalysisTool(BaseTool):
    name: str = "Sales Analysis Tool"
    description: str = "Analyze ecommerce sales and return top selling categories"

    def _run(self):
        order_items = pd.read_csv("data/order_items.csv")
        products = pd.read_csv("data/products.csv")
        categories = pd.read_csv("data/category_translation.csv")

        sales = order_items.merge(products, on="product_id")

        sales = sales.merge(
            categories,
            left_on="product_category_name",
            right_on="product_category_name"
        )

        summary = sales.groupby("product_category_name_english").agg(
            revenue=("price", "sum"),
            units_sold=("product_id", "count")
        ).sort_values("revenue", ascending=False)

        return summary.head(10).to_string()