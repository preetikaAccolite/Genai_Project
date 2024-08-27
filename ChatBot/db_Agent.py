import openai
import sqlite3
import re
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI()

class DBAgent:
    def __init__(self, database_name):
        self.database_name = database_name
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()

    def check_order_status(self, OrderNo):
        # SQL command to check all information of an order by OrderNo
        query = "SELECT * FROM Orders WHERE OrderNo = ?"
        self.cursor.execute(query, (OrderNo,))
        result = self.cursor.fetchone()

        if result:
            # Unpack the result tuple into individual variables
            order_no, name, mobile_number, items, order_status, order_time, delivery_time, remarks = result

            # Format the result into a readable string
            return (
                f"Order No: {order_no}\n"
                f"Customer Name: {name}\n"
                f"Mobile Number: {mobile_number}\n"
                f"Order Items: {items}\n"
                f"Order Status: {order_status}\n"
                f"Order Time: {order_time}\n"
                f"Delivery Time: {delivery_time if delivery_time else 'Not Delivered Yet'}\n"
                f"Remarks: {remarks if remarks else 'None'}"
            )
        else:
            return "No order found with the given OrderNo."

    def close(self):
        self.conn.close()

def get_OrderNo_from_llm(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Or another model that suits your needs
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=10,  # Adjust the number of tokens as needed
        temperature=0.5
    )
    # Extract the generated text from the response
    OrderNo_str = response.choices[0].message.content.strip()
    print(f"Received response from LLM: '{OrderNo_str}'")  # Debugging line

    # Use regex to find numeric value in the response
    match = re.search(r'\b\d+\b', OrderNo_str)
    if match:
        return match.group(0)
    else:
        return None


# Main execution
if __name__ == "__main__":
    # Define the prompt for the LLM
    prompt = "You are a customer that ordered certain items from an app. Please provide an OrderNo as a number between 1 and 20."

    # Get OrderNo from the LLM
    OrderNo_str = get_OrderNo_from_llm(prompt)
    if OrderNo_str is None:
        print("No valid OrderNo was provided by the LLM. Please ensure it provides a numeric value.")
        exit()

    # Validate and convert OrderNo
    try:
        OrderNo_to_check = int(OrderNo_str)
        print(f"OrderNo to check: {OrderNo_to_check}")  # Debugging line
    except ValueError:
        print("The OrderNo provided by the LLM is not valid. Please ensure it's a numeric value.")
        exit()

    # Initialize the database agent and check order status
    database_name = 'Orders.db'  # Ensure this matches your actual database file name
    agent = DBAgent(database_name)

    # Check the order status for the given OrderNo
    status = agent.check_order_status(OrderNo_to_check)
    print(status)

    # Close the database connection
    agent.close()
