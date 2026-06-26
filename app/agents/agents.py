from ..utils.prompts import main_prompt,ragAgent_prompt, answer_prompt

from pydantic import BaseModel, Field
from typing import Literal

class AgentCall(BaseModel):
    agent: Literal["rag"] = Field(
        default="",  
        description="Agents which can be called. It should match the exact literal used here "
    )
    query:str = Field(description="What query should the Agent work on")

class MainAgentOutputStructure(BaseModel):
    subagents: list[AgentCall] = Field(
        default = [],
        description="List of agents to call"
    )
    # output:str = Field(description="Final Output to the users question")

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

        return response
    
    def answerAgent(self, user_ip:str, context:str, callbackconfig):
        llm = self.modelinvokeobj.LLMModelInvoke()
        system_prompt = answer_prompt()
        prompt = system_prompt + f"User_qn: {user_ip}"
        if context != "":
            prompt += f"Retrieved Content {context}"
        response = llm.invoke(prompt, config={"callbacks": callbackconfig})
        return response
    
    def ragAgent(self, input_query:str, context:str):
        llm = self.modelinvokeobj.LLMModelInvoke()
        # retrievaltool = self.toolsObj.getretrieverTool()
        # context_ = retrievaltool(input_query)
        # print(context_)
        llm_with_tools = llm.bind_tools([self.toolsObj.getretrieverTool()])
        system_prompt = ragAgent_prompt()
        prompt = system_prompt + f"input_query: {input_query}"
        if context != "":
            prompt += f"Retrieved Content {context}"
        response = llm_with_tools.invoke(prompt)

        return response

