import os
from openai import OpenAI
class MAS():
    def __init__(self, agent):
        self.agent = os.getenv("Agent1")
        self.agent = agent
        print(self.agent)
    def chat(self, prompt):
        # Initialize the OpenAI client with the provided API key
        client = OpenAI(api_key=self.agent)

        # Send the chat completion request to the OpenAI API
        output = client.chat.completions.create(
            model="gpt-4",  # You can specify other models if required
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,  # You can adjust this value based on your needs
            temperature=0.7,  # Adjust creativity; 1.0 is more diverse, 0 is deterministic
            stop=None  # You can define stop sequences if needed
        )
        
        # Extract the content of the latest response from the assistant
        response_text = output.choices[0].message.content

        # Return the assistant's response text
        return response_text
    def manager(self, prompt):
        final_output = False
        
        while not final_output:
            print(prompt)
            task = prompt[:20].lower()
            
            # Determine the task type and set appropriate instructions
            if 'program' in task:
                instruction = f"""
                Instructions: 
                ```
                Remove the 'program' line from input before proceeding
                You are a programmer. Your task is to take an instruction for writing a program, and write the program in python.
                The backticks indicate the scope of the prompt.
                You shall write the first line with "debug", followed by outputting the program you wrote.
                The program and "debug" text shall be the ONLY output, with no additional text whatsoever. No greeting texts like "sure! This is a great idea" or anything of the sort.
                ```
                Prompt: 
                ```
                {prompt}
                ```
                """
                print("handing text to programmer agent")
            elif 'debug' in task:
                instruction = f"""
                Instructions: 
                ```
                Remove the 'debug' line from input before proceeding
                You are a programmer. Your task is to examine a python program, and look for errors. Look carefully for errors. Avoid false positives if you cannot find errors.
                The backticks indicate the scope of the prompt.
                Your output shall be structured in 2 parts:
                Command:
                If no errors are found, you shall write the instruction "quality" in the first line of your output.
                If there are errors, you shall write the instruction "program" in the first line of your output, then write instructions for how to correct the errors. 
                If there is no program, you shall write the instruction "final" in the frist line of your output. Then, write message to indicate program is missing.
                Code:
                You shall return the program exactly as-is, with no changes or omissions whatsoever.
                ```
                Prompt: 
                ```
                {prompt}
                ```
                """
                print("Handing text to debug agent")
            elif 'quality' in task:
                instruction = f"""
                Instructions: 
                ```
                Remove the 'quality' line from input before proceeding
                You are a software quality controller Your task is to examine a python program, and evaluate its quality. 
                The backticks indicate the scope of the prompt. 
                You shall evaluate the quality of the program on a scale of 1 to 10. Once you evaluate the program, you shall make a decision based on the quality score you gave. 
                Your output shall be structured in 2 parts: 
                Command:
                If quality is 7 or above, the first line of your output shall be the text "final". 
                If the quality of the program is below 7, the first line of your output shall be "program". You shall then write instructions on what needs to be improved, and how to improve it.
                Code:
                You shall return the program exactly as-is, with no changes or omissions whatsoever.
                ```
                Prompt: 
                ```
                {prompt}
                ```
                """
                print("Handing text to quality control agent")
            
            else:
                print("final output recieved")
                return prompt
            prompt = self.chat(instruction)