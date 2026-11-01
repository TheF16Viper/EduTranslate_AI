import os
from dotenv import load_dotenv

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

load_dotenv()

credentials = Credentials(
    url=os.getenv("WATSONX_URL"),
    api_key=os.getenv("WATSONX_APIKEY"),
)

# Define clean parameter limits so the model doesn't loop or hallucinate extra sentences
model_params = {
    "max_new_tokens": 50,          # Keeps the output short and precise
    "min_new_tokens": 1,
    "stop_sequences": ["\n"]       # Forces the model to stop running immediately at a line break
}

model = ModelInference(
    model_id="ibm/granite-4-h-small",
    credentials=credentials,
    project_id=os.getenv("WATSONX_PROJECT_ID"),
    params=model_params            # <-- Added configuration parameters here
)

# You can easily change this variable to "Marathi", "Tamil", "Bengali", etc.
target_language = "Marathi" 

structured_prompt = (
    f"System: You are an expert academic translator. Translate the text below into grammatically correct {target_language}.\n"
    "Rule: Do not include any definitions, introduction, or chat commentary. Output ONLY the raw translation.\n\n"
    "Text to translate: Machine Learning is a subset of Artificial Intelligence.\n"
    f"{target_language} Translation:"
)

response = model.generate_text(prompt=structured_prompt)

print(response.strip())
