from crewai import Agent, Task, Crew
from tools.sales_tool import SalesAnalysisTool
from tools.inventory_tool import InventoryTool
from tools.pdf_report import generate_pdf_report


# Initialize Tools
sales_tool = SalesAnalysisTool()
inventory_tool = InventoryTool()


# AGENTS

sales_agent = Agent(
    role="Sales Analyst",
    goal="Analyze ecommerce store sales performance",
    backstory="Expert in ecommerce sales analytics and retail insights",
    tools=[sales_tool],
    verbose=True
)

inventory_agent = Agent(
    role="Inventory Manager",
    goal="Monitor product demand and identify fast selling products",
    backstory="Specialist in supply chain and inventory management",
    tools=[inventory_tool],
    verbose=True
)

marketing_agent = Agent(
    role="Marketing Strategist",
    goal="Create marketing campaigns based on product demand and trends",
    backstory="Expert digital marketing strategist for ecommerce businesses",
    verbose=True
)

manager_agent = Agent(
    role="Store Manager",
    goal="Summarize the store performance and generate a business report",
    backstory="Experienced ecommerce manager responsible for strategic decisions",
    verbose=True
)


# TASKS

sales_task = Task(
    description="""
Analyze the ecommerce dataset and identify top selling product categories.
Provide revenue insights and important sales observations.
""",
    expected_output="A list of top selling product categories and sales insights.",
    agent=sales_agent
)

inventory_task = Task(
    description="""
Analyze product demand and identify fast selling products that may require restocking.
""",
    expected_output="List of fast selling products and inventory risks.",
    agent=inventory_agent
)

marketing_task = Task(
    description="""
Based on sales trends and product demand, create marketing campaign ideas
that could increase store revenue.
""",
    expected_output="Marketing campaign suggestions for high demand products.",
    agent=marketing_agent
)

manager_task = Task(
    description="""
Create a complete ecommerce business report summarizing:

1. Sales performance
2. Inventory insights
3. Marketing strategy recommendations
""",
    expected_output="A well structured ecommerce business report.",
    agent=manager_agent
)


# CREW EXECUTION

crew = Crew(
    agents=[
        sales_agent,
        inventory_agent,
        marketing_agent,
        manager_agent
    ],
    tasks=[
        sales_task,
        inventory_task,
        marketing_task,
        manager_task
    ],
    verbose=True
)

result = crew.kickoff()



# PRINT RESULT


print("\n===============================")
print(" AI STORE MANAGER REPORT ")
print("===============================\n")

print(result.raw)

# GENERATE PDF REPORT

report_file = generate_pdf_report(result.raw)

print("\nReport generated successfully:")
print(report_file)