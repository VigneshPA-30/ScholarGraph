from queue import Queue
from langchain_core.callbacks import BaseCallbackHandler

class QueueStreamCallback(BaseCallbackHandler):
    def __init__(self, queue: Queue):
        self.queue = queue
    
    def on_llm_new_token(self, token, **kwargs) -> None:
        if isinstance(token, list):
            token = "".join(
                item.get("text", "")
                if isinstance(item, dict)
                else str(item)
                for item in token
            )
        elif isinstance(token, dict):
            token = token.get("text", "") if "text" in token else str(token)
        else:
            token = str(token)

        if token:
            self.queue.put(token)
        
    def on_llm_end(self, *args, **kwargs) -> None:
        # Signal the end of the generation
        self.queue.put(None)