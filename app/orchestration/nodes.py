from ..agents.agents import Agents

class AgentNodes():
    def __init__(self, dependecymanager):
        self.agents = Agents(dependecymanager)
        self.toolsObj = dependecymanager.gettoolsobj()

    
    def mainAgent(self, MainAgentState):
        # print("chatNode chatwithllm")
        context = MainAgentState.get("context",[""])
        response = self.agents.mainAgent(MainAgentState["input"],context[-1])
        MainAgentState["context"].append(response)
        MainAgentState["output"] = response["output"]
        return MainAgentState
    
    def ragAgent(self, RagAgentState):
        context = RagAgentState.get("context",[""])
        response = self.agents.ragAgent(RagAgentState["input"],context[-1])
        RagAgentState["context"].append(response)
        return RagAgentState
    
    def route_after_ragAgent(self, RagAgentState):
        last_msg = RagAgentState["context"][-1]
        retry_count = RagAgentState.get("retry_count", 0)

        if hasattr(last_msg, "tool_calls") and last_msg.tool_calls and retry_count<3:
            RagAgentState["retry_count"]=retry_count+1
            return "tools"

        RagAgentState["output"] = last_msg.content
        return "end"
    
    def route_after_mainAgent(self, MainAgentState):
        last_msg = MainAgentState["context"][-1]
        subAgents = last_msg["subagents"]

        if subAgents == []:
            return "end"

        return subAgents[-1]
    
    def before_end(self, State):
        return State["output"]


        







    