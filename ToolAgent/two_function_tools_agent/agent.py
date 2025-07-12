from google.adk.agents import Agent

def get_order_status(order_id: str) -> str:
    """Looks up the status of a given order ID."""
    mock_db = {"order-123": "Shipped", "order-456": "Processing"}
    return mock_db.get(order_id, "Order not found.")

def check_product_inventory(product_name: str) -> str:
    """Checks the inventory for a given product"""
    mock_inventory = {"Laptop Pro": "In Stock", "Wireless Mounse": "Out of Stock"}
    return mock_inventory.get(product_name, "Product not found.")

root_agent = Agent(
    name="two_function_tools_agent",
    model="gemini-2.0-flash",
    description="An Agent with two Function Tools",
    instruction="""
    You are a helpful assistant that can use the following tools:
    - Get order status
    - Check product inventory
    """,
    tools=[get_order_status, check_product_inventory]
)
