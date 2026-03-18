import pandas as pd


def generate_excel_report(sales_summary, inventory_summary):

    with pd.ExcelWriter("store_report.xlsx", engine="openpyxl") as writer:

        sales_summary.to_excel(writer, sheet_name="Sales Summary")

        inventory_summary.to_excel(writer, sheet_name="Inventory Insights")

    return "Excel report generated: store_report.xlsx"