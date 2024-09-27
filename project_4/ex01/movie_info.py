import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY_GEMINI = os.getenv("API_KEY_GEMINI")

genai.configure(api_key=API_KEY_GEMINI)


def call_llm(prompt):
    try:
        genai.configure(api_key=API_KEY_GEMINI)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                max_output_tokens=500,
                temperature=0.7,
            ),
        )
        return response.text.strip()
    except Exception as e:
        print(f"Unexpected error from API Gemini: {e}")
        return None


def validate_json(response):
    try:
        movie_info = json.loads(response)
        return movie_info
    except json.JSONDecodeError as e:
        print(f"Erro: O modelo retornou uma resposta que não é um JSON válido: {e}")
        return None


def get_movie_info(movie_title):
    prompt = f"""
        <role>
            He works as a renowned filmmaker who has been writing scripts and film reviews for over 20 years. You are discerning and know almost all of the films that have been released to date.
        </role>
        <objective>
            Provide information about the movie "{movie_title}" in JSON format.
        </objective>
        <assistant_init>
            Start your response with:
            {{
            "title": {{"Movie Title"}},
        </assistant_init>
        <template>
            The answer must follow the template below. Return only the json as a response.
            {{
                "title": {{"Movie Title"}},
                "year": {{"0000"}},
                "director": {{"Director's Name"}},
                "genre": {{["Genre1", "Genre2"]}},
                "plot_summary": {{"Brief plot summary"}}
            }}
            <instructions>
                * Replacing {{"Movie Title"}} values with the movie title the film;
                * Replacing {{"0000"}} values with the year the film was released;
                * Replacing {{"Director's Name"}} values with the name of the film's directors;
                * Replacing {{["Genre1", "Genre2"]}} values  with the genres that the film contains;
                * Replacing {{"Brief plot summary"}} values with the brief of the film;
                * If you don't find any of the 5 pieces of information () return the string '#####' as input.
                * Please, review the json formatting in the final response. Don't forget to use commas as a separator and complete in pairs (open and close) all '{' '}' characters;
            </instructions>
        </template>
        <exemple>
            {{
                "title": {{"Ghost"}},
                "year": {{"1990"}},
                "director": {{"Jerry Zucker"}},
                "genre": {{["Drama", "Fantasy", "Romance"]}},
                "plot_summary": {{"Em Ghost - Do Outro Lado da Vida, Sam Wheat (Patrick Swayze) e Molly Jensen (Demi Moore) formam um casal muito apaixonado que tem suas vidas destruídas, pois ao voltarem de uma apresentação de "Hamlet" são atacados e Sam é morto. No entanto, seu espírito não vai para o outro plano e decide ajudar Molly, pois ela corre o risco de ser morta e quem comanda a trama, e o mesmo que tirou sua vida, é quem Sam considerava seu melhor amigo. Para poder se comunicar com Molly ele utiliza Oda Mae Brown (Whoopi Goldberg), uma médium trambiqueira que consegue ouvi-lo, para desta maneira alertar sua esposa do perigo que corre."}}
            }}
        </exemple>
	"""

    response = call_llm(prompt)
    movie_info = validate_json(response)
    return movie_info


def main():
    movie_titles = ["The Matrix", "Inception", "Pulp Fiction", "The Shawshank Redemption", "The Godfather"]

    for title in movie_titles:
        print(f"\nAnalyzing: {title}\n")
        result = get_movie_info(title)
        if result:
            for key, value in result.items():
                print(f"{key}: {value}")
        else:
            print("Não foi possível obter informações válidas sobre o filme.")
        print("-" * 50)


if __name__ == "__main__":
    main()
