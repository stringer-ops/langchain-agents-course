from langchain_docling import DoclingLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI

#Load PDF
loader = DoclingLoader(
    file_path=["my_pdf.pdf"]
)
document = loader.load()

#Perform the chunking with chunk overlap to enhance chunk context and avoid data loss
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 3000,
    chunk_overlap = 200,
)

chunks = text_splitter.split_documents(document)

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

summaries = []
for chunk in chunks[:20]:
    response = llm.invoke(f"Sum up the content of this piece of text in less than 10 phrases: {chunk}")
    summaries.append(response.content)

response = llm.invoke(f"Perform a summary of the content of this pieces of text: {'. '.join(summaries)}")
print(response.content)
