from ..utils.prompts import main_prompt,ragAgent_prompt

from pydantic import BaseModel, Field
from typing import Literal


class MainAgentOutputStructure(BaseModel):
    subagents: list[Literal["rag"]] = Field(
        default=[],  
        description="List of agents to call. Return an empty list [] if no agents are needed."
    )
    output:str = Field(description="Final Output to the users question")

class Agents:
    def __init__(self, dependencymanager):
        self.dependencymanager = dependencymanager
        self.toolsObj = self.dependencymanager.gettoolsobj()
        self.modelinvokeobj = self.dependencymanager.getmodelInvokeobj()
        
    def mainAgent(self, user_ip:str, context:str):
        llm = self.modelinvokeobj.LLMModelInvoke()
        llm_output_structured = llm.with_structured_output(MainAgentOutputStructure)
        system_prompt = main_prompt()
        prompt = system_prompt + f"User_qn: {user_ip}"
        if context != "":
            prompt += f"Retrieved Content {context}"
        response = llm_output_structured.invoke(prompt)

        return response.content
    
    def ragAgent(self, input_query:str, context:str):
        llm = self.modelinvokeobj.LLMModelInvoke()
        llm_with_tools = llm.bind_tools([self.toolsObj])
        system_prompt = ragAgent_prompt()
        prompt = system_prompt + f"input_query: {input_query}"
        if context != "":
            prompt += f"Retrieved Content {context}"
        response = llm_with_tools.invoke(prompt)

        return response

