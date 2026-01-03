import time

import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from ISO_Codes import country_to_iso

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def load_and_index():
    """
    Load and index the knowledge base
    :return:
    """
    with open("KnowledgeBase.txt", "r", encoding="utf-8") as f:
        text = f.read()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.create_documents([text])
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    Chroma.from_documents(chunks, embedding, persist_directory="chroma_store")


def generate(confirmation):
    """
    Updates/Generates the knowledge base
    :param confirmation:
    :return:
    """
    print("Updating Knowledge Base..... \n\n")
    with open("KnowledgeBase.txt", "w", encoding="utf-8") as f:
        for country in country_to_iso:
            time.sleep(2)

            # Preprocessing
            if country == "Russia":
                country = "Russian Federation"
            formatted_country = country.replace(" ", "")

            # Handling United States
            if formatted_country == "UnitedStates":
                url = "https://travel.gc.ca/destinations/united-states"
                res = requests.get(url, headers=headers)
                res.raise_for_status()

                soup = BeautifulSoup(res.content, 'html.parser')
                sections = soup.select(".mwsgeneric-base-html h2, .mwsgeneric-base-html p")

                f.write(f"Country: United States\n")
                for sec in sections:
                    text = sec.get_text(strip=True)
                    if text:
                        f.write(text + "\n")

            else:
                url = f"https://travel.state.gov/content/travel/en/international-travel/International-Travel-Country-Information-Pages/{formatted_country}.html"
                res = requests.get(url, headers=headers)
                res.raise_for_status()

                soup = BeautifulSoup(res.content, 'html.parser')
                advisory = soup.select_one(".tsg-rwd-alert-more-box-content")

                f.write(f"Country: {country}\n")
                if advisory:
                    f.write(advisory.text.strip())
                else:
                    f.write("No advisory information found.")

            f.write("\n\n" + "=" * 300 + "\n\n")
    load_and_index()


def retrieve(country):
    """
    Retrieves knowledge base
    :return:
    """

    # Retrieve advisory
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = Chroma(persist_directory="chroma_store", embedding_function=embedding)
    retriever = db.as_retriever(search_kwargs={"k": 1})
    results = retriever.get_relevant_documents(f"Travel advisory for {country}")

    return results
