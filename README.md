Gen AI project

The LLM is a customer. You are the agent. You will be assisted by a smart agent 
(RAG)

The scenario:
The customer is having trouble ordering via the store app due to connectivity 
issues. He has called the help desk to see if the order has gone through.
The agent will first attempt to resolve the connectivity issue (RAG over support 
documents)
When the customer is unable to apply the fixes suggested, the agent will then 
check the order history and confirm whether the order has been registered or not. 
(DB agent)

Solution:
The chat is one LLM flow
The RAG and DB agent are another
The LLM should be provided the scenario and also provided the current 
conversation asking it to generate the next msg.
The human will respond based on one side window providing RAG and the other 
side window providing DB agent details – Customer info and Customer order info
