import os 
from transformers import pipeline
import ast


models = ["google/flan-t5-base", "google/bigbird-base-trivia-itc", "codellama/CodeLlama-7b-Python-hf"]

CONTEXT = """Your name is AI.
You greet the user: Hi there! I am AI. I can help you generate 3D objects. *Only cups, spoons, knives, forks, and dishes*
You are an API to convert user’s text description of 3D objects into python code that can be used to generate 3D objects in Blender. You have access to a library of pre-defined 3D objects, (cups, knives, spoons, forks, and dishes) and you can generate 3D objects by combining these objects. You can also generate 3D objects by modifying the pre-defined objects (e.g., changing the size of the object, changing the color of the object, etc.).
{{user}}: make a fork
{{AI}}: forkObj=fork.ForkFactory(0).spwan_asset()
{{user}}: change color of it to [red|green|blue]
{{AI}}: forkObj.color = [(255,0,0,255)|(0,255,0,255)|(0,0,255,255)]
{{user}}: make it [small | medium | (large|big)]
{{AI}}: forkObj.dimensions = [(forkObj.dimensions[0] / 2, forkObj.dimensions[1] / 2, forkObj.dimensions[2] / 2)| (forkObj.dimensions[0] * 1.5, forkObj.dimensions[1] * 1.5, forkObj.dimensions[2] * 1.5)|(forkObj.dimensions[0] * 2),forkObj.dimensions[1] * 2), forkObj.dimensions[2] * 2)]
"""
def build_pipeline(model_name):
    return pipeline("text-generation", model=model_name, device="cpu")
def build_pipeline_from_dir(model_dir):
    return pipeline("text-generation", model=model_dir, device="cpu")

class chatBot:
    def __init__(self):
        self.context = ""
        self.model_dir = "./app/saved_models"
        self.model_name = ""
        self.pipe = None
        self.conversation = []
    
    def set_context(self, context):
        self.context = context 
    
    def set_model(self, model_name=models[0]):
        self.model_name = model_name
         # Check if the directory exists
        if not os.path.exists(self.model_dir):
            print("Model directory not found. Downloading the model...")
            # Download the model
            self.pipe = build_pipeline(model_name)
            # Save the downloaded model to the specified directory
            self.pipe.save_pretrained(self.model_dir)
        else:
            # Load the model from the local directory
            
            try:
                self.pipe = build_pipeline_from_dir(self.model_dir)
            except Exception as e:
                print("Error loading the model. Downloading the model...")
                # Download the model
                self.pipe = build_pipeline(model_name)
                # Save the downloaded model to the specified directory
                self.pipe.save_pretrained(self.model_dir)
            
    def chat(self, text):
        if self.pipe is None or self.model_name == "":
            print("Please set the model first.")
            return
        
        if self.context == "":
            print("Please set the context first.")
            return
        
        if text == "":
            print("Please provide a text.")
            return
        
        if len(self.conversation) == 0:
            self.conversation.append(self.context)
        
        self.conversation.append(text)
        
        full_text = " ".join(self.conversation)
        
        response = self.pipe(full_text, max_length=50, do_sample=False)
        
        self.conversation.append(response[0]["generated_text"])
        
        return response[0]["generated_text"]
    
    def reset_converson(self):
        self.conversation = []
        
    def get_last_response(self):
        return self.conversation[-1]
    
    def check_response(self):
        if len(self.conversation) == 0 or len(self.conversation) == 1:
            return False
        last_response = self.conversation[-1]
        try:
            ast.parse(last_response)
        except SyntaxError:
            return False
        self.conversation[-1] = last_response
        return True
    
    def append_response_to_file(self, file_path):
        if self.check_response():
                
            with open(file_path, "a") as f:
                f.write(self.conversation[-1] + "\n")
    