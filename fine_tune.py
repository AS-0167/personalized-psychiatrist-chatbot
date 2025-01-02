import google.generativeai as genai
import time
import pandas as pd

with open("api.key", "r") as file:
    API_KEY = file.read().strip()
genai.configure(api_key=API_KEY)
base_model = "models/gemini-1.5-flash-001-tuning"


def load_training_data_from_csv(file_path, max_rows=100):
    """
    Loads and preprocesses training data from the first `max_rows` of a CSV file.
    
    Args:
        file_path (str): Path to the CSV file.
        max_rows (int): Maximum number of rows to read from the CSV file. Default is 100.
    
    Returns:
        list: Preprocessed training data in the format required for fine-tuning.
    """
    df = pd.read_csv(file_path, nrows=max_rows)
    
    required_columns = {"questionTitle", "questionText", "answerText"}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"CSV must contain the columns: {', '.join(required_columns)}")
    
    df["text_input"] = df["questionTitle"] + " " + df["questionText"]
    
    training_data = [
        {"text_input": row["text_input"], "output": row["answerText"]}
        for _, row in df.iterrows()
    ]
    
    return training_data

if (__name__ == "__main__") :

    # --- Psychiatric-specific training data ---
    file_path = "data.csv"
    training_data = load_training_data_from_csv(file_path, max_rows=100)
 
    # --- Create a tuned model ---
    operation = genai.create_tuned_model(
        
        display_name="psychiatrist_assistant",
        source_model=base_model,              
        epoch_count=20,                       
        batch_size=4,                         
        learning_rate=0.001,                  
        training_data=training_data           
    )

    # --- Monitor the training process ---
    print("Fine-tuning in progress...")
    for status in operation.wait_bar():
        time.sleep(10)

    # --- Get the fine-tuned model result ---
    result = operation.result()
    print("Fine-tuning complete.")
    print("Tuned model name:", result.name)


    #Tuned model name: tunedModels/psychiatristassistant-w8m6ckrnbbp2
