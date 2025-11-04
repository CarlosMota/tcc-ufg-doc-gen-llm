# Aplicação Prática de LLMs e engenharia de prompt no mercado (M10)
Repositório de código referente ao Microcurso 10 da Especialização _lato sesu_ em Processamento de Linguagem Natural (NLP) do **AKCIT** - Centro de Competência EMBRAPII em Tecnologias Imersivas (_Advanced Knowledge Center for Immersive Technologies_).

## Recomendação

É altamente indicado que você assista a todas as videoaulas do Microcurso 10!

## Como executar?

Acompanhe o seguinte passo a passo, criado a partir do material fornecido pelo professor.

As etapas aqui exibidas foram apresentadas durante as vídeoaulas, disponíveis no AVA.

1. Baixe o código disponível aqui, nesse repositório, clicando no botão **Code** e depois em **Download ZIP**.

2. Em seguida, extraia o arquivo baixado.

3. Entre na pasta que acabou de extrair. Ela possui a seguinte estrutura:
   ```
   ├── arquitetura
   │   ├── templates
   │   ├── app.py
   │   ├── bd.py
   │   ├── business_rules_be.py
   │   ├── business_rules_fe.py
   │   ├── controlador.py
   │   ├── db_classes.py
   │   ├── extract_classes.py
   │   ├── extract_pdf_be.py
   │   ├── extract_pdf_fe.py
   │   ├── extract_sql_be.py
   │   ├── extract_sql_fe.py
   │   ├── gerenciador.py
   │   ├── sad_sql.json
   │   ├── virtual_assistant_be.py
   │   └── virtual_assistant.json
   ├── chatbot
   │   ├── chroma_db
   │   ├── templates
   │   ├── app.py
   │   ├── extract_pdf.json
   │   ├── message.db
   │   └── virtual_assistant.json
   ├── sad
   │   ├── chroma_db
   │   ├── templates
   │   ├── app.py
   │   ├── business_rules.json
   │   ├── message.db
   │   ├── sad_sql.json
   │   ├── vendas.db
   │   └── virtual_assistant.json
   ├── env_ebook10.yml
   └── README.md
   ```

4. Faça o download do ebook do Microcurso 4 - Introdução a Machine Learning e Redes Neurais. Salve-o na pasta que você acabou de extrair com o nome sugerido. A estrutura deve ficar da seguinte forma:
   ```
   ├── arquitetura
   │   ├── templates
   │   ├── app.py
   │   ├── bd.py
   │   ├── business_rules_be.py
   │   ├── business_rules_fe.py
   │   ├── controlador.py
   │   ├── db_classes.py
   │   ├── extract_classes.py
   │   ├── extract_pdf_be.py
   │   ├── extract_pdf_fe.py
   │   ├── extract_sql_be.py
   │   ├── extract_sql_fe.py
   │   ├── gerenciador.py
   │   ├── sad_sql.json
   │   ├── virtual_assistant_be.py
   │   └── virtual_assistant.json
   ├── chatbot
   │   ├── chroma_db
   │   ├── templates
   │   ├── app.py
   │   ├── extract_pdf.json
   │   ├── message.db
   │   └── virtual_assistant.json
   ├── sad
   │   ├── chroma_db
   │   ├── templates
   │   ├── app.py
   │   ├── business_rules.json
   │   ├── message.db
   │   ├── sad_sql.json
   │   ├── vendas.db
   │   └── virtual_assistant.json
   ├── env_ebook10.yml
   ├── M4_IMLRN_10-12-24.pdf
   └── README.md
   ```

---

> ❗ Antes de prosseguir, assista a Videoaula 2 (Unidade 1 do Microcurso 10). É nessa aula que o professor mostra como instalar o software necessário (Anaconda).

---

5. Se estiver utilizando **Windows**, abra o **Anaconda Powershell Prompt** (conforme a Videoaula 2). Em seguida, navegue até a pasta que você extraiu anteriormente (onde se encontra o arquivo `env_ebook10.yml`). Nessa janela, execute:

   `conda env create -f env_ebook10.yml`

   > 💡 Você pode tentar usar a tecla TAB após digitar as iniciais do nome do arquivo para autocompletar.

   > ❗ Essa etapa pode demorar um pouco. Aguarde até que esteja finalizado para continuar. Com a execução finalizada, feche a janela.

6. Edite o arquivo `arquitetura/virtual_assistant_be.py`, alterando a linha:

   `genai.configure(api_key="SUA-KEY")`.

   Você deve substituir o texto `SUA-KEY`por uma *key* pessoal e válida. Pode ser a *key* que você gerou no **Microcurso 9**. Salve e feche o arquivo.

7. Abra quatro janelas do **Anaconda Powershell Prompt** e navegue até a pasta que extraiu inicialmente. Você precisa fazer isso nas quatro janelas.

8. Em cada uma das quatro janelas, digite:

   `conda activate ebook10`

9. Nas quatro janelas, acesse a pasta `chatbot`.

   `cd chatbot`

10. Na primeira janela, digite: 

      `python ../arquitetura/bd.py -dbname message.db -r` \
      `fastapi dev ../arquitetura/gerenciador.py`

11. Na segunda janela, digite: 

      `python ../arquitetura/controlador.py`

12. Na terceira janela, digite:

      `set FLASK_APP=app.py` \
      `python app.py`

14. Na quarta janela, digite:

      `python ../arquitetura/extract_pdf_fe.py -j ./extract_pdf.json`

15. Quando o comando anterior finalizar, acesse o seguinte endereço utilizando seu navegador de Internet (Chrome, Firefox, Safari, etc): `127.0.0.1:5000` ou `localhost:5000`. Agora, basta interagir com o chatbot.

> ❗ Lembre-se de **aguardar** após clicar em **Enviar**.

> 🎓 *Todos os passos descritos anteriormente foram extraídos do material disponibilizado pelo professor.*