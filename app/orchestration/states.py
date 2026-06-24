from typing import TypedDict


class MainAgentState(TypedDict):
    input:str
    context:list
    output:str


class RAGAgentState(TypedDict):
    input:str
    context:list
    output:str
    retry_count:int
