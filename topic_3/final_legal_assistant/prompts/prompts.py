# Main prompt for the RAG system
RAG_TEMPLATE = """You are a legal assistant specialized in lease agreements.
Based ONLY on the following contract fragments, answer the user's question.

CONTRACT FRAGMENTS:
{context}

QUESTION: {question}

INSTRUCTIONS:
- Provide a clear and direct answer based on the available information
- If you find the exact information, quote it verbatim when relevant
- Include all important details: names, addresses, amounts, dates
- If the information is incomplete or unavailable, state that clearly
- Organize the information in a structured way if necessary
- If multiple contracts or people are mentioned, specify which one you are referring to

ANSWER:"""

# Custom prompt for the MultiQueryRetriever
MULTI_QUERY_PROMPT = """You are an expert in legal document analysis, specialized in lease agreements.
Your task is to generate multiple versions of the user's query to retrieve relevant documents from a vector database.

When generating query variations, consider:
- Different ways to refer to people (full name, last name, first name only)
- Legal synonyms and technical leasing terminology
- Variations in question phrasing about contractual aspects
- Terms related to locations, properties, and contract conditions

Original query: {question}

Generate exactly 3 alternative versions of this query, one per line, without numbering or bullet points:"""

# Prompt for document relevance analysis
RELEVANCE_PROMPT = """Analyze whether the following document fragment is relevant for answering the user's query.

FRAGMENT:
{document}

QUERY: {question}

Is this fragment relevant to answer the query? Respond only with "YES" or "NO" and a brief justification."""

# Prompt for key entity extraction
ENTITY_EXTRACTION_PROMPT = """Extract the key entities from the following lease agreement text:

TEXT:
{text}

Identify and extract:
- Names of people (landlord, tenant, guarantors)
- Property addresses
- Monetary amounts
- Important dates
- Contract duration
- Property type

Response format:
PEOPLE: [list of names]
ADDRESSES: [list of addresses]
AMOUNTS: [list of amounts]
DATES: [list of dates]
DURATION: [contract period]
TYPE: [property type]"""