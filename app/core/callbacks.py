from queue import Queue
from langchain_core.callbacks import BaseCallbackHandler

class QueueStreamCallback(BaseCallbackHandler):
    def __init__(self, queue: Queue):
        self.queue = queue

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        # Push each token to the queue as it generates
        self.queue.put(token)
        
    def on_llm_end(self, *args, **kwargs) -> None:
        # Signal the end of the generation
        self.queue.put(None)