import os
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()

API_KEY_GEMINI = os.getenv("API_KEY_GEMINI")


def send_to_gemini(prompt):
    try:
        print("Consultando Gemini...")
        genai.configure(api_key=API_KEY_GEMINI)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                max_output_tokens=300,
                temperature=1.0,
            ),
        )
        return response.text
    except Exception as e:
        print(f"Unexpected error from API Gemini: {e}")
        return None


def create_prompt(role, task, topic, specific_question):
    return (
            f"""<prompt>
                    <role>Your new role is {role}</role>
                    <topic>The topic of the task is {topic}</topic>
                    <task>
                        <description>Your task is to {task}</description>
                        <question>And the question that you need answers for is {specific_question}</question>
                    </task>
                    <format>
                        <instruction>Use this format to make it easy to understand:</instruction>
                            {{the answer generated by you}}
                    </format>
                </prompt>"""
    )


def main():
    role = "especialista em métodos de educação inovadores em tecnologia"
    task = "explicar o conceito e a abordagem única da École 42 para interessados em educação em tecnologia"
    topic = "École 42 e seu método de ensino"
    specific_question = "O que é a École 42 e como seu método de ensino difere das faculdades tradicionais de computação?"
    prompt = create_prompt(role, task, topic, specific_question)
    response = send_to_gemini(prompt)
    print("\nResposta do Gemini 1.5 Flash:")
    print(response)


if __name__ == "__main__":
    main()
