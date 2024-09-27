import re
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY_GEMINI = os.getenv("API_KEY_GEMINI")
genai.configure(api_key=API_KEY_GEMINI)


def extract_content(text, tag):
    pattern = f"<{tag}>(.*?)</{tag}>"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""


def call_llm(prompt):
    try:
        genai.configure(api_key=API_KEY_GEMINI)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                max_output_tokens=1000,
                temperature=0.7,
            ),
        )
        return response.text
    except Exception as e:
        print(f"Unexpected error from API Gemini: {e}")
        return None


def run_prompt_chain():
    stage_1_prompt = """
        <instruction>
            Provide an overview of the life and career of Claude Shannon, the father of information theory. Structure the response using the following XML tags:
            <overview>...</overview>
        </instruction>
        """
    overview = call_llm(stage_1_prompt)

    stage_2_prompt = f"""
        <instruction>
            Using the following information about the life and career of Claude Shannon:
            <overview>{overview}</overview>
            Analyze his key contributions to information theory. Structure the response using the tag:
            <contributions>...</contributions>
        </instruction>
        """
    contributions = call_llm(stage_2_prompt)

    stage_3_prompt = f"""
        <instruction>
            Considering Claude Shannon's contributions to information theory:
            <contributions>{contributions}</contributions>
            Explore the impact of his work on modern computing and communication technologies. Structure the response using the tag:
            <impact>...</impact>
        </instruction>
        """
    impact = call_llm(stage_3_prompt)

    stage_4_prompt = f"""
        <instruction>
            Using the following information:
                <overview>{overview}</overview>
                <contributions>{contributions}</contributions>
                <impact>{impact}</impact>
                Synthesize this information into a comprehensive analysis of Claude Shannon's life, career, and impact. Structure the response using the tags:<analysis>...</analysis>
        </instruction>
        """
    response_4 = call_llm(stage_4_prompt)
    analysis = extract_content(response_4, "analysis")

    print("Análise Completa sobre Claude Shannon:")
    print(analysis)


if __name__ == "__main__":
    run_prompt_chain()
