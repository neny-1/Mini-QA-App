from abc import ABC,abstractclassmethod

class LLMInterface(ABC):
    # using abstractclassmethod that make this function required when create or use an object from this class
    @abstractclassmethod
    def set_generation_model(self,model_id:str):
        pass

    @abstractclassmethod
    def set_embedding_model(self,model_id:str,embedding_size:int):
        pass

    @abstractclassmethod
    def generate_text(self,prompt:str,chat_history:list=[],max_output_tokens:int=None,temperature:float=None):
        pass

    # to convert data text into embeddings 
    @abstractclassmethod
    def embed_text(self,text:str,document_type:str):
        pass
    
    # before generate_text
    @abstractclassmethod
    def construct_prompt(self,prompt:str,role:str):
        pass

    