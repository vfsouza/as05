import streamlit as st
from pathlib import Path
import google.generativeai as genai
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
import os

# Configuração da página Streamlit
st.set_page_config(page_title="Assistente PDF", layout="wide")

# Configuração do Gemini com API key fixa
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text.strip()


def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,  # Aumentado para pegar mais contexto
        chunk_overlap=400,  # Aumentado para melhor continuidade
        length_function=len,
        separators=["\n\n", "\n", " ", ""]  # Separadores mais específicos
    )
    chunks = splitter.split_text(text)
    return chunks


def create_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=GOOGLE_API_KEY
    )
    vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vector_store


def main():
    st.header("💬 Assistente PDF")

    # Inicializa o estado da sessão
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None
    if "raw_text" not in st.session_state:
        st.session_state.raw_text = ""

    # Upload de arquivos
    with st.sidebar:
        st.subheader("Seus documentos")
        pdf_docs = st.file_uploader(
            "Faça upload dos seus arquivos PDF e clique em 'Processar'",
            accept_multiple_files=True
        )
        if st.button("Processar"):
            if pdf_docs:
                with st.spinner("Processando"):
                    # Extrai o texto dos PDFs
                    st.session_state.raw_text = get_pdf_text(pdf_docs)

                    # Divide o texto em chunks
                    text_chunks = get_text_chunks(st.session_state.raw_text)

                    # Cria a base de vetores
                    st.session_state.vector_store = create_vector_store(text_chunks)

                    st.success("Documentos processados com sucesso!")
                    # Mostra uma prévia do texto extraído
                    with st.expander("Visualizar texto extraído"):
                        st.text(st.session_state.raw_text[:1000] + "...")
            else:
                st.error("Por favor, faça upload de pelo menos um documento PDF.")

    # Interface de chat
    if query := st.chat_input("Faça sua pergunta sobre os documentos..."):
        if st.session_state.vector_store is None:
            st.error("Por favor, faça upload e processe alguns documentos primeiro!")
        else:
            # Busca os documentos mais relevantes
            docs = st.session_state.vector_store.similarity_search(query, k=4)
            context = "\n\n".join([doc.page_content for doc in docs])

            # Prepara o prompt mais flexível
            prompt = f"""

            Documento para análise:
            {context}

            Pergunta do usuário: {query}

            Por favor, forneça uma resposta detalhada baseada nas informações do documento."""

            # Gera a resposta
            try:
                response = model.generate_content(prompt)

                # Adiciona à história do chat
                st.session_state.chat_history.append(("user", query))
                st.session_state.chat_history.append(("assistant", response.text))
            except Exception as e:
                st.error(f"Erro ao gerar resposta: {str(e)}")

    # Exibe o histórico do chat
    for role, content in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(content)


if __name__ == "__main__":
    main()