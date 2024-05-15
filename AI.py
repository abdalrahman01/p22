from transformers import AutoTokenizer
import transformers
import torch

CONTEXT = "You are an API to convert user\u2019s text description of 3D objects into python code that can be used to generate 3D objects in Blender. You have access to a library of pre-defined 3D objects, (cups, knives, spoons, forks, and dishes) and you can generate 3D objects by combining these objects. You can also generate 3D objects by modifying the pre-defined objects (e.g., changing the size of the object, changing the color of the object, etc.).\n{{user}}: make a fork\n{{AI}}: forkObj=fork.ForkFactory(0).spawn_asset(0)\n{{user}}: change color of it to [red|green|blue]\n{{AI}}: forkObj.color = [(255,0,0,255)|(0,255,0,255)|(0,0,255,255)] #(r,g,b,a)\n{{user}}: make it [small | medium | big]\n{{AI}}: forkObj.dimensions = [(forkObj.dimensions[0] / 2, forkObj.dimensions[1] / 2, forkObj.dimensions[2] / 2)| (forkObj.dimensions[0] * 1.5, forkObj.dimensions[1] * 1.5, forkObj.dimensions[2] * 1.5)|(forkObj.dimensions[0] * 2),forkObj.dimensions[1] * 2), forkObj.dimensions[2] * 2)]\n{{user}}: make a horn\n{{AI}}: **Sorry, I can Only make cups, spoons, knives, forks, and dishes**\n{{user}}: make 3 cups\n{{AI}}: cupObjs = [cup.CupFactory(i).spawn_asset(i) for i in range(3)]\n{{user}}: make 1 red, 1 blue and 1 green\n{{AI}}: cupObjs[0].color = (255,0,0,255)\ncupObjs[1].color = (0,255,0,255)\ncupObjs[2].color = (0,0,255,255)\n{{user}}: move one to the left, one to the right, one to the top\n{{AI}}: cupObjs[0].location[0] += cupObjs[0].dimensions[0] * 2\ncupObjs[1].location[0] -= cupObjs[1].dimensions[0] * 2\ncupObjs[2].location[1] += cupObjs[2].dimensions[1] * 2"

if __name__ == "__main__":
    print(CONTEXT)
    exit()

class AI :

    context = CONTEXT
    def __init__(self, from_File = True):
        self.model_name = "codellama/CodeLlama-7b-hf"
        self.model_dir = "./CodeLlama-7b-Python-hf"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        if from_File:
            self.pipeline = transformers.pipeline(
                                    "text-generation",
                                    model=self.model_dir,
                                    torch_dtype=torch.float16,
                                    device_map="cpu"
                                    )
        else:
            self.pipeline = transformers.pipeline(
                                    "text-generation",
                                    model=self.model_name,
                                    torch_dtype=torch.float16,
                                    device_map="cpu"
                                    )
    
    # def AI_response_ended(self, txt):
    #     n = len(txt)
    #     if n == 1:
    #         return False
    #     if n == 2 and txt[1].startswith("{{AI}}"): 
    #         return True
    #     for sentance in range (2, n):
    #         if txt[sentance].startswith("{{user}}"):
    #             return True
    #     return False
    # def talk_with_ai(text, old_conv_len, max_new_tokens = 30):
    #     old_max_new_tokens = max_new_tokens
    #     sequences = pipeline(
    #     text,
    #     do_sample=True,
    #     temperature=0.29,
    #     num_return_sequences=1,
    #     eos_token_id=tokenizer.eos_token_id,
    #     max_new_tokens=max_new_tokens)

    #     new_lines = sequences[0]['generated_text'][old_conv_len:].split("\n")
        
    #     # # check the last line if it starts with ...
    #     # if (not AI_response_ended("{{user}}")):
    #     #     return talk_with_ai(text, old_conv_len, max_new_tokens = max_new_tokens + 10)
    #     # #print(new_lines)
    
    #     return get_last_ai_response("\n".join(new_lines))


    def chat_internal(self, text, conversation):
        old_conv_len = len(conversation)
        conversation += "{{user}}: " + text + "\n"
        conversation += "{{AI}}: "
        # ai_response = talk_with_ai(conversation, old_conv_len)
        ai_response = self.pipeline(
            text,
            do_sample=True,
            temperature=0.29,
            num_return_sequences=1,
            eos_token_id= self.tokenizer.eos_token_id,
            max_new_tokens=40)[0]['generated_text']
        extracted_ai_response = self.get_last_ai_response(ai_response)
        self.context += ai_response
        return ai_response
    def reset_chat(self):
        return ""
    
    
    def get_last_ai_response(self, ai_response):
        new_lines = ai_response.split("\n")
        n = len(new_lines)
        for i in range(n-1, -1, -1):
            if new_lines[i].startswith("{{AI}}"):
                return new_lines[i]
        return ""