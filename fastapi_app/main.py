from fastapi import FastAPI, HTTPException
import xlwings as xw
import json
import os

app = FastAPI()

@app.post('/process/{model_id}')
async def process_data(model_id: str, data: dict):
    try:
        models_directory = os.path.join(os.path.dirname(__file__), '..', 'models')
        with open(os.path.join(models_directory, f'model_{model_id}', 'config.json')) as f:
            config = json.load(f)

        with xw.App(visible=False) as app:
            wb = xw.Book(os.path.join(models_directory, f'model_{model_id}', config["excel_file"]))
            input_sheet = wb.sheets[config["input_sheet"]]
            for param, cell in config["input_locations"].items():
                input_sheet.range(cell).value = data.get(param)
            
            output_sheet = wb.sheets[config["output_sheet"]]
            result = {key: output_sheet.range(cell).value for key, cell in config["output_locations"].items()}
            wb.close()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
