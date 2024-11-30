# Assistente PDF 💬

Este é um aplicativo desenvolvido com Streamlit que processa documentos PDF e permite que o usuário faça perguntas sobre o conteúdo carregado. Ele utiliza a integração com o Google Generative AI e a biblioteca LangChain para dividir o texto, gerar embeddings e realizar buscas semânticas.

---

## 🚀 Requisitos

-  **Python 3.8 ou superior**
-  **Chave de API do Google Generative AI**

---

## 📦 Dependências

As dependências do projeto estão listadas no arquivo `requirements.txt`:

streamlit google-generativeai pypdf langchain langchain-google-genai faiss-cpu

---

## ⚙️ Configuração

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar a variável de ambiente GOOGLE_API_KEY

O aplicativo utiliza os.environ.get("GOOGLE_API_KEY") para acessar a chave de API. Para configurá-la, siga um dos métodos abaixo:

No terminal, configure a variável de ambiente:

Linux/MacOS:

```bash
export GOOGLE_API_KEY=SUA_CHAVE_DE_API
```

Windows:

```bash
set GOOGLE_API_KEY=SUA_CHAVE_DE_API
```

## 🏃‍♂️ Execução

Para iniciar o aplicativo, execute:

```bash
streamlit run main.py
```

Abra o navegador e acesse o link exibido no terminal, geralmente http://localhost:8501.

## 🛠️ Funcionalidades

-  Carregar PDFs: Faça upload de múltiplos arquivos PDF através da barra lateral.
-  Processar documentos: Extraia texto, divida em blocos e crie uma base de vetores para pesquisa.
-  Interface de Chat: Faça perguntas sobre os documentos processados e receba respostas detalhadas.

## 📝 Exemplo de Uso

Configure a variável de ambiente GOOGLE_API_KEY como explicado acima.

Faça upload de documentos PDF na barra lateral.

Clique em Processar.

Digite uma pergunta no campo de entrada do chat.

Veja as respostas baseadas no conteúdo dos PDFs.

# Link da aplicação: https://as05-vinicius-souza.streamlit.app/

# Link Drive: https://drive.google.com/drive/folders/177odyLCcsvSa2nAJepyINYLAz6zLLpCq?usp=sharing

# Github: https://github.com/vfsouza/as05
