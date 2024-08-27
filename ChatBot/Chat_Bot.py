import os
import re
from db_Agent import DBAgent
import openai
from llama_index.core import Settings, SimpleDirectoryReader, StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from dotenv import load_dotenv
from llama_index.core.tools import FunctionTool
from llama_index.agent.openai import OpenAIAgent

# Load environment variables
load_dotenv()
client = openai.OpenAI()

# Initialize LLM and embedding models
Settings.llm = OpenAI(model="gpt-4o-mini")
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")


def get_OrderNo_from_llm(prompt):

    OrderNo_str = prompt

    # print(f"Received response from LLM: '{OrderNo_str}'")  # Debugging line

    # Use regex to find numeric value in the response
    match = re.search(r'\b\d+\b', OrderNo_str)
    if match:
        return match.group(0)
    else:
        return None


def RAG(prompt):
    """ This function is used to answer queries related to slow internet issues and troubleshooting connectivity issues """
    # check if storage already exists
    PERSIST_DIR = "./storage"

    if not os.path.exists(PERSIST_DIR):
        # load the documents and create the index
        documents = SimpleDirectoryReader("data/Support_Doc/").load_data()
        index = VectorStoreIndex.from_documents(documents)
        # store it for later
        index.storage_context.persist(persist_dir=PERSIST_DIR)
    else:
        # load the existing index
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)

    query_engine = index.as_query_engine()
    RAG_res = query_engine.query(prompt+".Give a compact answer in points.")
    print("RAG Assistant :")
    print(RAG_res)


def DB(query):
    """ This function is used to fetch order related queries """
    prompt = query
    # Get OrderNo from the query
    OrderNo_str = get_OrderNo_from_llm(prompt)
    if OrderNo_str is None:
        print("DB Assistant :No valid OrderNo was provided by the LLM. Please ensure it provides a numeric value.")
        return

    # Validate and convert OrderNo
    try:
        OrderNo_to_check = int(OrderNo_str)
        # print(f"OrderNo to check: {OrderNo_to_check}")  # Debugging line
    except ValueError:
        print("The OrderNo provided by the LLM is not valid. Please ensure it's a numeric value.")
        return

    # Initialize the database agent and check order status
    database_name = 'Orders.db'  # Ensure this matches your actual database file name
    agent1 = DBAgent(database_name)

    # Check the order status for the given OrderNo
    status = agent1.check_order_status(OrderNo_to_check)
    print("DB Assistant: ")
    print(status)

    # Close the database connection
    agent1.close()


RAG_tool = FunctionTool.from_defaults(fn=RAG)

DB_tool = FunctionTool.from_defaults(fn=DB)

tools = [RAG_tool, DB_tool]

llm = OpenAI(model="gpt-4o-mini")

agent = OpenAIAgent.from_tools(tools, llm=llm, verbose=False)


def get_completion_from_messages(messages, model="gpt-4o-mini", temperature=0):
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,  # this is the degree of randomness of the model's output
    )
    return completion.choices[0].message.content


def is_issue_resolved(response):
    """Determine if the issue has been resolved based on the response."""
    resolved_keywords = ["issue resolved", "problem fixed", "order confirmed", "Exit"]
    return any(keyword in response.lower() for keyword in resolved_keywords)


def append_system_messages(messages, system_message):
    # Append the system message
    messages.append({'role': 'system', 'content': system_message})

    return messages


def append_user_messages(messages, user_message):

    # Append the user message
    messages.append({'role': 'user', 'content': user_message})

    return messages


def main():
    messages = [
        {'role': 'system',
         'content': "You are a customer who is having trouble ordering via app due to slow internet connectivity issues. Always keep in mind that you are the customer and you could only communicate in conversation as a customer. You have called the help desk to see if the order has gone through.You will first attempt to resolve the connectivity and slow internet issue. After trying those fixes, go towards checking your order status. Don't give information about your order number until asked specifically. Choose your order number somewhere between 1 to 20 if asked.If the query is resolved, say 'issue resolved'."},
        {'role': 'user', 'content': "A human agent is assigned the task to solve your queries, please ask your query."}]
    while True:
        cus = get_completion_from_messages(messages, temperature=1)
        print("Customer: ", cus)
        append_system_messages(messages, cus)

        # print("-----------------------------------------------------------------------------")
        agent.chat(cus)
        # print("Assistant: ", res)
        # print("-----------------------------------------------------------------------------")

        # Check if the issue is resolved
        if is_issue_resolved(cus):
            print("Agent: It seems the issue is resolved. Thank you :)")
            exit()

        agent_message = input("Agent: ")
        if agent_message in ['exit', 'issue solved']:
            exit()
        append_user_messages(messages, agent_message)


if __name__ == "__main__":
    main()

# Customer:  Hi! I'm having trouble ordering through the app due to slow internet connectivity. Can you help me with fixing these connection issues first? I've tried a few things, but it’s still not working well.
# Agent: Are you facing slow internet issue?
# Customer:  Yes, I'm facing slow internet issues that are making it difficult for me to place an order through the app. I've already tried a few troubleshooting steps, but it's still not working. Can you help me with that?
# - Check for peak bandwidth saturation; consider upgrading your broadband service or reducing the number of devices in use.
# - Ensure home networking equipment (routers, switches) is configured correctly; seek manufacturer support if needed.
# - Run antivirus software to check for and remove any viruses that may be affecting performance.
# - Minimize interference from other devices operating on the 2.4GHz band by changing Wi-Fi channels or connecting to a 5GHz network.
# - Identify and disable any background applications that may be consuming bandwidth, such as cloud services or automatic updates.
# - Power off any unused devices to free up bandwidth for active ones.
# Agent: Please ensure all your networking equipment is configured correctly.
# Customer:  I've checked my networking equipment, and everything seems to be set up correctly. The router and modem are working fine, and the connection appears stable. What should I try next?
# - Check for peak bandwidth saturation; consider upgrading your broadband service or reducing the number of devices using the internet simultaneously.
# - Ensure that all networking equipment is configured correctly; consult the manufacturer for support if needed.
# - Scan your devices for computer viruses and ensure that antivirus protection is enabled and up to date.
# Agent: Please restart all your devices once.
# Customer:  I've restarted my router, modem, and phone, but the internet connection is still slow. What should I do next?
# - Check for peak bandwidth saturation; consider upgrading your broadband service or reducing the number of devices using the internet simultaneously.
# - Ensure home networking equipment (routers, switches, etc.) is configured correctly; consult the manufacturer or a qualified professional if needed.
# - Run a virus scan on your devices to check for any computer viruses that may be affecting performance; ensure antivirus protection is enabled.
# - Verify that all wired and wireless devices are properly connected and that the Internet Gateway is optimally located for coverage.
# - Consider potential interference from neighbors using the same Wi-Fi network; ensure your Wi-Fi is password-protected.
# Agent: I think the issue is something from your Internet Service Provider, please contact them for this issue.
# Customer:  Alright, I will contact my Internet Service Provider to check if there are any issues on their end. Thank you for the suggestion.
#
# In the meantime, could you help me check the status of my order? I want to ensure it went through since I've been having these connectivity issues.
# No valid OrderNo was provided by the LLM. Please ensure it provides a numeric value.
# Agent: Please provide me your Order Number.
# Customer:  My order number is 7. Can you please check the status for me?
# Order No: 7
# Customer Name: Charlie
# Mobile Number: +15583177125
# Order Items: Item2, Item3
# Order Status: Delivered
# Order Time: 2023-09-29 21:55:53
# Delivery Time: 2023-09-30 21:55:53
# Remarks: Gift
# Agent: As far as I can see in the Database, your order had 2 items and has been delivered on 30th August.
# Customer:  Thank you for the information! It looks like my order has been delivered, which is great to hear. Just to confirm, the connectivity issue is being handled with my Internet Service Provider, and I can now rest easy knowing my order status.
#
# Issue resolved!
# Agent: It seems the issue is resolved. Thank you :)
