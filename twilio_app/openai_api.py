import os
from decouple import config

os.environ["OPENAI_API_KEY"] = config('OPENAI_API_KEY')

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import DirectoryLoader
from langchain.chains import VectorDBQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
loader = DirectoryLoader('./', glob='MatbakhiFeeding(1).txt')
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings()
docsearch = Chroma.from_documents(
    texts,
    embeddings
)

system_template="""Use the following pieces of context to answer the users question:
You are a hotel cloud kitchen company in Saudi Arabia called "Matbakhi" with 7 brands, and you are designed to answer users' questions about which brands they can eat from. If the user enters the name of a meal, you will respond with the brand that serves that meal and information about it. For example, if the question is "I want to eat...", you will answer with the brand that serves that meal and provide the user with information about both the brand and the meal.
انت شركة مطابخ سحابية فندقية في المملكة العربية السعودية تدعى "مطبخي"، ولديك 7 علامات تجارية، وتقوم بلإجابة على أسئلة المستخدمين حول أي من العلامات التجارية التي يمكن لهم تناول الطعام منها. إذا أدخل المستخدم اسم وجبة، سترد عليه بالبراند الذي يقدم تلك الوجبة ومعلومات عن الوجبة. على سبيل المثال، إذا كان السؤال هو "أريد تناول ..."، سترد عليه بأن البراند التي تقدم تلك الوجبة هي "... " وأعطي المستخدم معلومات عن البراند والوجبة.

رد على السؤال باللغة العربية اذا كان السؤال باللغة العربية
----------------
{summaries}"""
messages = [
    HumanMessagePromptTemplate.from_template("{question}"),
    SystemMessagePromptTemplate.from_template(system_template)
]
prompt = ChatPromptTemplate.from_messages(messages)

chain_type_kwargs = {"prompt": prompt}
chain = VectorDBQAWithSourcesChain.from_chain_type(
    ChatOpenAI(temperature=0), 
    chain_type="stuff", 
    vectorstore=docsearch,
    chain_type_kwargs=chain_type_kwargs
)

def text_complition(question: str) -> dict:
    try:
        response = chain({ 'question': question })
        return {
            'status': 1,
            'response': response['answer']
        }
    except:
        return {
            'status': 0,
            'response': ''
        }
        
# while True:
#     quwstion = input('Enter your question: ')
#     answer = text_complition(quwstion)
#     print(answer['response'])