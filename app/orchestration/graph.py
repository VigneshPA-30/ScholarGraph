from langgraph.graph import (
    StateGraph,
    START,
    END
)
from .nodes import AgentNodes
from .states import MainAgentState, RAGAgentState
from ..tools.tools import Tools
from langgraph.prebuilt import ToolNode

class AgentGraph:
    def __init__(self, dependecymanager):
        self.nodes = AgentNodes(dependecymanager)
        self.tools = Tools(dependecymanager)

    def ragAgentGraph(self):
        print(f"RAGAgentGraph...")
        builder = StateGraph(RAGAgentState)

        builder.add_node("RAGAgent",self.nodes.ragAgent)
        # builder.add_node("route_after_ragAgent", self.nodes.route_after_ragAgent)
        builder.add_node("retrievertool",ToolNode([self.tools.retrieverTool]))
        builder.add_node("before_end",self.nodes.before_end)

        builder.add_edge(START, "RAGAgent")
        builder.add_conditional_edges("RAGAgent",self.nodes.route_after_ragAgent,{"tools":"retrievertool", "end":"before_end"})
        builder.add_edge("retrievertool","RAGAgent")
        builder.add_edge("before_end",END)

        graph = builder.compile()
        return graph


    def mainAgentGraph(self):
        print(f"MainAgent Graph...")
        ragSubGraph = self.ragAgentGraph()
        builder = StateGraph(MainAgentState)

    # Building Nodes
        # builder.add_node("retriever", self.nodes.retrieveDocs)
        builder.add_node("MainAgent",self.nodes.mainAgent)
        builder.add_node("ragSubGraph",ragSubGraph)
        builder.add_node("before_end",self.nodes.before_end)
        

    #Connecting Nodes
        builder.add_edge(START,"MainAgent")
        builder.add_conditional_edges("MainAgent",self.nodes.route_after_mainAgent,{"rag":"ragSubGraph", "end":"before_end"})
        builder.add_edge("ragSubGraph","MainAgent")
        builder.add_edge("before_end",END)

        graph = builder.compile()
        return graph






