import os
from dotenv import load_dotenv
from groq import Groq
import ollama
import google.generativeai as genai

load_dotenv()

API_KEY_GROQ = os.getenv("API_KEY_GROQ")
API_KEY_GEMINI = os.getenv("API_KEY_GEMINI")


def chatOllama(prompt):
    try:
        stream = ollama.chat(
            model='qwen2:1.5b',
            messages=[{'role': 'user', 'content': prompt}],
            stream=False,
        )
        return stream['message']['content']
    except KeyError:
        print("Erro: Estrutura inesperada no retorno da API Ollama")
        return None
    except Exception as e:
        print(f"Erro inesperado na API Ollama: {e}")
        return None


def chatGroq(prompt):
    try:
        client = Groq(api_key=API_KEY_GROQ)
        chat_completion = client.chat.completions.create(
            model='llama3-8b-8192',
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=300,
            temperature=1.0,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Erro inesperado na API Groq: {e}")
        return None


def chatGemini(prompt):
    try:
        genai.configure(api_key=API_KEY_GEMINI)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                max_output_tokens=300,
                temperature=0.1,
            ),
        )
        return response.text
    except genai.exceptions.APIError as e:
        print(f"Erro na API Gemini: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado na API Gemini: {e}")
        return None


def query_all_models(job_description):
    print(
        "Consultando Gemini...\n"
        "Consultando Groq...\n"
        "Consultando Ollama...\n"
    )
    results = {
        'Gemini 1.5 Flash': chatGemini(job_description) or "Erro ao consultar Gemini",
        'Llama 3 8B': chatGroq(job_description) or "Erro ao consultar Groq",
        'Qwen2 1.5B': chatOllama(job_description) or "Erro ao consultar Ollama",
    }
    return results


def format_prompt(job_description):
    return (
        f"Com base na seguinte descrição de vaga: {job_description}, elabore uma descrição concisa e precisa com base na primeira vaga de Engenharia de Software com mais informações que encontrar."
        "Inclua informações sobre as ferramentas e habilidades técnicas equisitadas (exemplo: Python, Java, etc.).\n"
        "Formato da resposta:\n"
        "Name of role: [cargo]\n"
        "Working hours: [horário]\n"
        "Country: [país]\n"
        "Tech skills: [habilidades técnicas]"
    )


def main():
    with open("job_description.txt", "r") as file:
        job_description = file.read()
    formatted_prompt = format_prompt(job_description)
    results = query_all_models(formatted_prompt)
    for model, response in results.items():
        print(f"\nAnálise do {model}:")
        print(response)
        print("-" * 50)


if __name__ == "__main__":
    main()
