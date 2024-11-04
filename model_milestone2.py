from transformers import pipeline
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# Convert image to text description
def img2text(url):
    img_to_text_pipe = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large")
    text = img_to_text_pipe(url)[0]["generated_text"]
    return text


def textGeneration_langchain(msg,type):
    """
    msg is the scenario for the text from the pic (hugging face model output);
   
    type is the name of the artist - including Dua Lipa, Ariana Grande, Charlie Puth, Drake, Billie Eilish, Eminem, Lady Gaga, Beyoncé, Ed Sheeran, Justin Bieber, Taylor Swift, Rihanna, Coldplay, Nicki Minaj, Katy Perry, Maroon 5, Selena Gomez, Post Malone

    """
    llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.2,
            max_tokens=200,
            timeout=None,
            max_retries=2
        )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system",

        "You are an expert in recommending and writing song lyrics. Based on the following emotional content. "
        "Choose lyrics from the artist {lyric_type} that matches this emotion as inspirations. "
        "Then write several lyric lines that best fits the {lyric_type} and says when this artist meets certain sitations, what lyrics she/her will sing"
            ),
            ("human", "{scenario_lang}"), ] )
    


    chain = prompt | llm | StrOutputParser()

    out_message = chain.invoke({
            "lyric_type" : type,
            "scenario_lang" : msg,
        })
    
    return out_message

def runModels_langchain(url, type):
    scenario = img2text(url)
    lyric = textGeneration_langchain(scenario,type)
    return([scenario,lyric])


def getRetriever(dir):
    """
    dir is the directory of the vector DB
    """
    embeddings_used = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorDB = Chroma(persist_directory=dir,embedding_function=embeddings_used)
    retriever = vectorDB.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    return retriever

def textGeneration_langChain_RAG(msg,type,retrieverDir):
    """
    msg is the scenario for the story from the pic (hugging face model output);
   
    type is the name of the artist - including Dua Lipa, Ariana Grande, Charlie Puth, Drake, Billie Eilish, Eminem, Lady Gaga, Beyoncé, Ed Sheeran, Justin Bieber, Taylor Swift, Rihanna, Coldplay, Nicki Minaj, Katy Perry, Maroon 5, Selena Gomez, Post Malone

    retriever is the vector DB with relevant stories from txt version of 
       lyrics dataset from Hugging face - https://huggingface.co/datasets/cmsolson75/artist_song_lyric_dataset
    """
    llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.2,
            max_tokens=200,
            timeout=None,
            max_retries=2
        )

    system_prompt = (

        "You are an expert in recommending and writing song lyrics, choose lyrics from the artist {lyric_type} that matches this scene and write them down. To recommend this song to audiences, tells the correct album name. "
        "Then write a verse including lyrics that best fits the {lyric_type}. "
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{scenario_lang}"),
        ]
    )

    rag_chain = prompt | llm | StrOutputParser()

    retriever = getRetriever(retrieverDir)

    out_message = rag_chain.invoke({
            "lyric_type" : type,
            "context":retriever,
            "scenario_lang" : msg,
        })
    
    return out_message

def runModels_langchain_RAG(url, type, retrieverDir):
    scenario = img2text(url)
    lyric = textGeneration_langChain_RAG(scenario,type,retrieverDir)
    # print(story)
    return([scenario,lyric])