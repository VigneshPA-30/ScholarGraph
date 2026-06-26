from ..agents.agents import Agents
import threading

class AgentNodes():
    def __init__(self, dependecymanager, callbackconfig):
        self.dependecymanager = dependecymanager
        self.agents = Agents(dependecymanager)
        self.toolsObj = dependecymanager.gettoolsobj()
        self.callbackconfig = callbackconfig
    
    def mainAgent(self, MainAgentState):
        # print("chatNode chatwithllm")
        context = MainAgentState.get("context",[""])
        response = self.agents.mainAgent(MainAgentState["input"],context[-1])
        print("MainAgent\n\n"+str(response))
        MainAgentState["context"].append(response)
        # MainAgentState["output"] = response.output
        return MainAgentState
    
    def answerAgent(self, MainAgentState):
        context = MainAgentState.get("context",[""])
        response = self.agents.answerAgent(MainAgentState["input"],context[-1], callbackconfig= self.callbackconfig)
        print("AnswerAgent\n\n"+str(response))
        MainAgentState["context"].append(response)
        MainAgentState["output"] = response.content
        return MainAgentState

    def ragAgent(self, RagAgentState):
        context = RagAgentState.get("context",[""])
        response = self.agents.ragAgent(RagAgentState["input"],context[-1])
        print("RAGAgent\n\n"+str(response))
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
        subAgents = last_msg.subagents

        if subAgents == []:
            return "answerAgent"

        return "callagents"
    

    def callSubAgents(self, MainAgentState):
        from .graph import RAGAgentGraph #tmp fix

        last_msg = MainAgentState["context"][-1]
        subAgents = last_msg.subagents
        final_response = ""
        for agent_ in subAgents:
            if agent_.agent =="rag":
                ragagent = RAGAgentGraph(self, self.dependecymanager)
                graph = ragagent.ragAgentGraph()
                rag_response = self.start_graph(graph,agent_.query)
                final_response += f"RAG response {rag_response}"

        MainAgentState["context"].append(final_response)
        return {"final_response":final_response}



    def start_graph(self, graph, query):
        answer = graph.invoke({
                    "input": query,
                    "context": [""],
                    "output": ""
                }
                )
        return answer
        
    
    def before_end(self, State):
        return {"output":State["output"]}
    
    def main_agent_before_end(self, State):
        return {"output":State["output"]}


        







    