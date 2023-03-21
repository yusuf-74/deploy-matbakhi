import os
os.environ["OPENAI_API_KEY"] = "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"

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import DirectoryLoader
from langchain.chains import VectorDBQAWithSourcesChain
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
loader = DirectoryLoader('/home/yaaa3ser/Desktop/fine-tuning-demo/25QAs/', glob='MatbakhiFeeding(1).txt')
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
texts = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings()
docsearch = Chroma.from_documents(
    texts,
    embeddings
)

system_template="""Use the following pieces of context to answer the users question:
Your name is ServiceBot2.0, you are designed to answer questions about a restaurant called 'Matbakhi'.
استخدم القطع التالية من السياق للإجابة عن سؤال المستخدم:
اسمك بوت الخدمة 2.0 ، وأنت مصمم للإجابة عن أسئلة حول مطعم يسمى "مطبخي" اجب على السؤال باللغة العربية اذا كان السؤال باللغة العربية
----------------
{summaries}"""
messages = [
    HumanMessagePromptTemplate.from_template("{question}"),
    SystemMessagePromptTemplate.from_template(system_template)
]
prompt = ChatPromptTemplate.from_messages(messages)

chain_type_kwargs = {"prompt": prompt}
chain = VectorDBQAWithSourcesChain.from_chain_type(
    ChatOpenAI(temperature=0.2), 
    chain_type="stuff", 
    vectorstore=docsearch,
    chain_type_kwargs=chain_type_kwargs
)

def print_question_response(response):
    print('----')
    print("You asked: ")
    print(response['question'])
    print("")
    print("The chatbot answered: ")
    print(response['answer'])
    print("")
    print("---------")
  
questions = [
    'سعر البيبسي',
    'سعر الايس كريم',
    'price of pepsi',
    "سعر البطاطا المقلية",
    "Juices available and their prices",
    "سعر ميل كريم 16 والنكهات المتوفرة",
    "اماكن فروع مطبخي"
]
with open('answers.txt', 'w') as f:
    for question in questions:
        response = chain({ 'question': question })
        ans = ""
        ans+="----\n" + "You asked: \n" + question+"\n\n" + "The chatbot answered: \n"+response['answer']+"\n"+"---------\n"
        f.write(ans)
