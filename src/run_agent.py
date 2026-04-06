from agent import PricingAgent

agent = PricingAgent()

while True:
    query = input("Ask: ")
    print(agent.run(query))