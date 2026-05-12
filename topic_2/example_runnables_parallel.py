from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import json

load_dotenv()

MAX_TEXT_SIZE=300

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)


text_to_analyze = [
    """Today was a wonderful day, I celebrated my birthday with all my friends after
    coming from living in Brazil for three years
    and in the night we went partying. This is what life should be all about""",
    """It's been 3 weeks and a half since I saw the sky completely clear, I'm starting
    to get tired of this cloudy weather""",
    """Lately nothing really clicks. I have been fired from my job, my girlfriend and I are
    arguing quite often and my knee hurts since that football game last Friday. I feel like
    all the odds are against me and I can do nothing to fix it"""
]

def preprocess_text(text):
    """Eliminated useless whitespace and limits the text size"""

    text = text[:MAX_TEXT_SIZE].strip()

    return text

def generate_summary(text):

    prompt = f"Sum up the text given in one phrase that catches the feeling of it: {text}"
    result = llm.invoke(prompt)

    return result.content

def analyze_feeling(text):
    
    prompt = f""""Analyze the feeling of the next text. 
        Answer MUST ONLY BE the next JSON template filled:
        {{
            "feeling": "positive|negative|neutrum",
            "reason": **short justification**"
        }}
        
        Text: {text}
        """
    
    result = llm.invoke(prompt)
    result_formated = None
    try:
        result_formated = json.loads(result.content)
    except Exception as e:
        print(f"Error when formatting string '{result.content}' to JSON: {e}")
    else:
        return result_formated

preprocessor = RunnableLambda(preprocess_text)
summarize = RunnableLambda(generate_summary)
analyzer = RunnableLambda(analyze_feeling)
    
parallel_stage = RunnableParallel({
    "summary": summarize,
    "feeling_data": analyzer
})

def merge_results(data):
    return {
        "summary": data['summary'],
        "feeling": data["feeling_data"]["feeling"],
        "reason": data["feeling_data"]["reason"]
    }

merger = RunnableLambda(merge_results)

chain = preprocessor | parallel_stage | merger

for text in text_to_analyze:
    print(f"Initial text: '{text}'")
    result = chain.invoke(text)
    print(f"Processed text: '{result}'")

