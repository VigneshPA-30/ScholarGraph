from langgraph.graph import (
    StateGraph,
    START,
    END
)
from .nodes import AgentNodes
from .states import MainAgentState, RAGAgentState
from ..tools.tools import Tools
from langgraph.prebuilt import ToolNode

class MainAgentGraph:
    def __init__(self, dependecymanager):
        self.nodes = AgentNodes(dependecymanager)
        self.tools = dependecymanager.gettoolsobj()

    def mainAgentGraph(self):
        print(f"MainAgent Graph...")
        # ragSubGraph = self.ragAgentGraph()
        builder = StateGraph(MainAgentState)

    # Building Nodes
        # builder.add_node("retriever", self.nodes.retrieveDocs)
        builder.add_node("MainAgent",self.nodes.mainAgent)
        builder.add_node("callSubAgents",self.nodes.callSubAgents)
        builder.add_node("before_end",self.nodes.main_agent_before_end)
        

    #Connecting Nodes
        builder.add_edge(START,"MainAgent")
        builder.add_conditional_edges("MainAgent",self.nodes.route_after_mainAgent,{"callagents":"callSubAgents", "end":"before_end"})
        builder.add_edge("callSubAgents","MainAgent")
        builder.add_edge("before_end",END)

        graph = builder.compile()
        return graph




class RAGAgentGraph:
    def __init__(self, nodes,dependecymanager):
        self.nodes = nodes
        self.tools = dependecymanager.gettoolsobj()
    
    def ragAgentGraph(self):
        print(f"RAGAgentGraph...")
        builder = StateGraph(RAGAgentState)

        builder.add_node("RAGAgent",self.nodes.ragAgent)
        # builder.add_node("route_after_ragAgent", self.nodes.route_after_ragAgent)
        builder.add_node("retrievertool",ToolNode([self.tools.getretrieverTool()], messages_key="context"),)
        builder.add_node("before_end",self.nodes.before_end)

        builder.add_edge(START, "RAGAgent")
        builder.add_conditional_edges("RAGAgent",self.nodes.route_after_ragAgent,{"tools":"retrievertool", "end":"before_end"})
        builder.add_edge("retrievertool","RAGAgent")
        builder.add_edge("before_end",END)

        graph = builder.compile()
        return graph

