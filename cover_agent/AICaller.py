import time
import litellm

class AICaller:
    def __init__(self, model):
        """
        Initializes an instance of the AICaller class.

        Parameters:
            model (str): The name of the model to be used.
        """
        self.model = model

    def call_model(self, prompt, max_tokens=4096):
        """
        Call the language model with the provided prompt and retrieve the response.

        Parameters:
            prompt (str): The prompt to provide to the language model.
            max_tokens (int, optional): The maximum number of tokens to generate in the response. Defaults to 4096.

        Returns:
            tuple: A tuple containing the response generated by the language model, the number of tokens used from the prompt, and the total number of tokens in the response.
        """
        messages = [{"role": "user", "content": prompt}]
        response = litellm.completion(model=self.model, messages=messages, max_tokens=max_tokens, stream=True)

        chunks = []
        print("Streaming results from LLM model...")
        try:
            for chunk in response:
                print(chunk.choices[0].delta.content or "", end="", flush=True)
                chunks.append(chunk)
                time.sleep(0.01)  # Optional: Delay to simulate more 'natural' response pacing
        except Exception as e:
            print(f"Error during streaming: {e}")
        print("\n")

        model_response = litellm.stream_chunk_builder(chunks, messages=messages)

        # Returns: Response, Prompt token count, and Response token count
        return model_response['choices'][0]['message']['content'], int(model_response['usage']['prompt_tokens']), int(model_response['usage']['completion_tokens'])
