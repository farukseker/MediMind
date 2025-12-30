from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import HumanMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
import json
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. MODELLER
# llama3.2:1b
# qwen2.5:0.5b
# mistral:7b-instruct-q4_K_M

mdl = 'RefinedNeuro/Turkcell-LLM-7b-v1'
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', google_api_key=config.GEMINI_API_KEY)
# llm = ChatOllama(model=mdl, streaming=True, temperature=0.7)
embeddings = OllamaEmbeddings(model="nomic-embed-text")
print('modeller yüklendi')

# 2. VERİ YÜKLEME VE VEKTÖR YAPISI
docs = []

# Blogları ekle
with open("cemre_demirel.json", "r", encoding="utf-8") as f:
    posts = json.load(f)
    for post in posts:
        if content := post.get("content"):
            docs.append(content)
print('blog yazıları yüklendi')

# Kitabı ekle
loader = PyPDFLoader("AhlakFelsefesindeTanriNerede-icerik.pdf")
for page in loader.load():
    docs.append(page.page_content)

# Kitabı ekle
loader = PyPDFLoader("Bir_Baska_Din_Tasavvuf_.pdf")
for page in loader.load():
    docs.append(page.page_content)

print('kitaplar yüklendi')

# Parçala ve embed et
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
texts = splitter.split_text(" ".join(docs))
print('split edildi')


vectorstore = FAISS.from_texts(texts, embedding=embeddings)
retriever = vectorstore.as_retriever(k=4)
print('FAISS ediliyor')

vectorstore.save_local("cemre_faiss_blog_2_books_index")

print('FAISS kayıt adlı cemre_faiss_blog_2_books_index')

# 3. SOHBET GEÇMİŞİ
history = ChatMessageHistory()

print('geçmiş oluşturuldu')


# 4. SORU İŞLEYİCİ
def get_relevant_context(question):
    docs = retriever.invoke(question)
    return "\n\n".join([d.page_content if hasattr(d, 'page_content') else d for d in docs])


print('ready to go')
# 5. STREAMLİ CHAT DÖNGÜSÜ
while True:
    user_input = input("Sen > ")
    if user_input.lower() in ["q", "quit", "exit"]:
        print("Görüşürüz!")
        break

    context = get_relevant_context(user_input)
    prompt = f"""
Sen Cemre Demirel'in yazılarına göre yanıt veriyorsun.
Bilmediklerine cevap verme.
Soru: {user_input}
İlgili içerikler:
{context}
"""
    history.add_message(HumanMessage(content=user_input))

    print("Cemre >", end=" ", flush=True)
    response_text = ""
    for chunk in llm.stream([*history.messages, HumanMessage(content=prompt)]):
        print(chunk.content, end="", flush=True)
        response_text += chunk.content

    history.add_message(AIMessage(content=response_text))
    print("\n")
    history.clear()
