import google.generativeai as genai

genai.configure(api_key="AIzaSyAT-tD3-8hh5zHs0SrBV8lZW7vKPIYb9XE")  # ここに正しいキーをコピペ

models = genai.list_models()
for m in models:
    print(m.name)