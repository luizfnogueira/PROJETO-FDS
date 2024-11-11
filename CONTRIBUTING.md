
## Índice
- [Bem-vindo(a)!](#bem-vindoa)
- [Como contribuir?](#como-contribuir)
- [Configurando o repositório](#configurando-o-repositório)
- [Configurando o ambiente de desenvolvimento](#configurando-o-ambiente-de-desenvolvimento)
- [Executando os testes](#executando-os-testes)
- [Submetendo suas Alterações](#submetendo-suas-alterações)
- [Código de Conduta](#código-de-conduta)
- [Onde obter ajuda?](#onde-obter-ajuda)
- [Como fazer um relatório de bug](#como-fazer-um-relatório-de-bug)
- [Convenções de codificação e guia de estilo](#convenções-de-codificação-e-guia-de-estilo)
- [Arquivos de referência](#arquivos-de-referência)
- [Obrigado por Contribuir!](#obrigado-por-contribuir)

---
## 👋 Bem-vindo(a)!

Se você chegou até aqui, é porque tem interesse em contribuir com o FORTIS! Antes de começar, leia este guia para entender como você pode colaborar da melhor forma possível.

---

## 🤔 Como contribuir?

Você pode sugerir uma nova funcionalidade, propor melhorias ou escolher uma das [issues em aberto](https://github.com/luizfnogueira/PROJETO-FDS/issues) para resolver.

---

## 📁 Configurando o repositório

1. **Faça um Fork do Repositório:** Crie uma cópia do repositório na sua conta para realizar alterações sem afetar o repositório principal.

2. **Clone o repositório:**
   ```bash
   git clone https://github.com/luizfnogueira/PROJETO-FDS.git
   ```

3. **Crie sua Branch:**
   ```bash
   git checkout -b minha-nova-funcionalidade
   ```

---

## 💻 Configurando o ambiente de desenvolvimento

1. **Entre no Diretório do Projeto:**
   ```bash
   cd PROJETO-FDS
   ```

2. **Crie um Ambiente Virtual:**
   ```bash
   python -m venv venv
   ```

3. **Ative o Ambiente Virtual:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Instale as Dependências:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Aplique as Migrations (Criar o Banco de Dados):**
   ```bash
   python manage.py migrate
   ```

6. **Rode o Servidor:**
   ```bash
   python manage.py runserver
   ```

### Rodando os testes

Para garantir que seu código não afete outras partes do projeto:

1. **Baixe o [Node](https://nodejs.org/en) na versão LTS.**

2. **Instale as dependências:**
   ```bash
   npm ci
   ```

3. **Execute os testes:**
   ```bash
   npx cypress run
   ```

---

## 🛰️ Submetendo suas Alterações

Quando terminar, abra um Pull Request com uma descrição detalhada das alterações realizadas.

1. **No repositório do seu fork, clique em `Contribute`.**

2. **Clique em `Open pull request`.**

3. **Selecione o repositório e a branch onde realizou as alterações.**

4. **Para finalizar, clique em `Create pull request`.**

Nós da equipe do WhichTeacher iremos avaliar sua submissão. Se necessário, entraremos em contato para revisarmos o seu código.

---
## 📝 Código de Conduta

Ao colaborar neste projeto, pedimos que todos sigam nosso [Código de Conduta](PROJETO-FDS\CODE_OF_CONDUCT.md). Nosso objetivo é criar um ambiente inclusivo, respeitoso e colaborativo para todos os contribuidores. Esperamos que todos se comportem de maneira cordial, respeitosa e construtiva, tanto em interações dentro do código quanto fora dele.

Se você presenciar qualquer comportamento que viole essas diretrizes, entre em contato com a equipe de manutenção para que possamos resolver a situação da melhor forma possível. O não cumprimento do Código de Conduta pode resultar em ações, como a remoção de contribuições ou bloqueio de acesso ao projeto.

## Onde obter ajuda
Caso tenha dúvidas, entre em contato conosco através do e-mail: [contato.fortis@gmail.com](mailto:contato.fortis@gmail.com).

## 🐛 Como fazer um relatório de bug
Verifique se o bug já foi reportado em [issues em aberto](https://github.com/luizfnogueira/PROJETO-FDS/issues).
Forneça uma descrição clara e detalhada do erro.
Inclua o ambiente de desenvolvimento (sistema operacional, versão do Python, etc.).
Se possível, adicione um repositório mínimo reproduzível.

## 🛠️ Como corrigir um bug
Verifique a [documentação do código](PROJETO-FDS\README.md) para entender a estrutura do projeto.
Siga as convenções de codificação (veja a seção Convenções de codificação e guia de estilo).
Teste suas alterações localmente e garanta que todos os testes passem.
Submeta as alterações via Pull Request.

## 📚 Convenções de Codificação e Guia de Estilo

Para garantir que nosso código seja consistente e fácil de manter, por favor, siga as seguintes diretrizes ao contribuir:

1. Mensagens de Commit
  - Escreva mensagens de commit no **tempo presente** e de forma **imperativa**:
  - "Corrige bug na página de login"
  - "Adiciona testes para a funcionalidade de registro"

2. Comentários
- Comente seu código onde necessário, especialmente para trechos complexos. Evite comentários desnecessários.
- **Funções**: Sempre inclua uma descrição clara sobre o que a função faz, seus parâmetros e o valor retornado.


## 📄 Arquivos de referência
LICENSE.md (PROJETO-FDS\LICENSE.md)
README.md (PROJETO-FDS\README.md)
humans.txt (PROJETO-FDS\humans.txt)


## ❤️ Obrigado por Contribuir!

Agradecemos sinceramente a todos os colaboradores que ajudam a melhorar este projeto. Suas contribuições são valiosas para nós e fazem uma grande diferença. Estamos ansiosos para receber suas sugestões e melhorias! 
