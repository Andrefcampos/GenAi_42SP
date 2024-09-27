import os
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()

API_KEY_GEMINI = os.getenv("API_KEY_GEMINI")

github_comments = [
    {
        "text": "Ótimo trabalho na implementação desta feature! O código está limpo e bem documentado. Isso vai ajudar muito nossa produtividade.",
        "sentiment": ""
    },
    {
        "text": "Esta mudança quebrou a funcionalidade X. Por favor, reverta o commit imediatamente.",
        "sentiment": ""
    },
    {
        "text": "Podemos discutir uma abordagem alternativa para este problema? Acho que a solução atual pode causar problemas de desempenho no futuro.",
        "sentiment": ""
    },
    {
        "text": "Obrigado por relatar este bug. Vou investigar e atualizar a issue assim que tiver mais informações.",
        "sentiment": ""
    },
    {
        "text": "Este pull request não segue nossas diretrizes de estilo de código. Por favor, revise e faça as correções necessárias.",
        "sentiment": ""
    },
    {
        "text": "Excelente ideia! Isso resolve um problema que estávamos enfrentando há semanas. Mal posso esperar para ver isso implementado.",
        "sentiment": ""
    },
    {
        "text": "Esta issue está aberta há meses sem nenhum progresso. Podemos considerar fechá-la se não for mais relevante?",
        "sentiment": ""
    },
    {
        "text": "O novo recurso está causando conflitos com o módulo Y. Precisamos de uma solução urgente para isso.",
        "sentiment": ""
    },
    {
        "text": "Boa captura! Este edge case não tinha sido considerado. Vou adicionar testes para cobrir este cenário.",
        "sentiment": ""
    },
    {
        "text": "Não entendo por que estamos priorizando esta feature. Existem problemas mais críticos que deveríamos estar abordando.",
        "sentiment": ""
    },
]


def call_llm(text):
    few_shot_prompt = f"""
        A seguir estão alguns exemplos de análises de sentimentos:

        Exemplo 1:
        text: Ótimo implementação desta solução! Está tudo bem claro. Isso irá repercutir em ótimos resultados.
        sentiment: Positivo

        Exemplo 2:
        text: Esta proposta não é suficiente. Por favor, pense mais.
        sentiment: Negativo

        Exemplo 3:
        text: Funciona, mas acredito que você pode fazer melhor. Se empenhe.
        sentiment: Neutro

        Exemplo 4:
        text: O código ficou muito bom, adorei a forma como você resolveu o problema de performance. Parabéns!
        sentiment: Positivo

        Exemplo 5:
        text: Infelizmente, essa solução não resolve todos os casos e está causando erros em outras partes do sistema.
        sentiment: Negativo

        Exemplo 6:
        text: O código está quase lá, mas faltam alguns ajustes para melhorar a legibilidade e organização.
        sentiment: Neutro

        text: {text}
        sentiment:
    """
    try:
        print("Consultando Gemini...")
        genai.configure(api_key=API_KEY_GEMINI)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            few_shot_prompt,
            generation_config=genai.GenerationConfig(
                max_output_tokens=300,
                temperature=0.7,
            ),
        )
        return response.text
    except Exception as e:
        print(f"Unexpected error from API Gemini: {e}")
        return None


def parse_llm_response(response):
    if 'Positivo' in response:
        return 'Positivo'
    elif 'Negativo' in response:
        return 'Negativo'
    elif 'Neutro' in response:
        return 'Neutro'
    else:
        return 'Não identificado'


def analyze_sentiments(comments):
    for comment in comments:
        llm_response = call_llm(comment["text"])
        comment["sentiment"] = parse_llm_response(llm_response)


analyze_sentiments(github_comments)


for comment in github_comments:
    print(f"Texto: {comment['text']}")
    print(f"Sentimento: {comment['sentiment']}")
    print("-" * 50)
