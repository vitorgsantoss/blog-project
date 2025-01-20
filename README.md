# Blog Project

## Descrição

O **Blog Project** é uma aplicação web desenvolvida para gestão e exibição de blogs. Ele utiliza tecnologias modernas para garantir escalabilidade, segurança e facilidade de uso. Este projeto é executado em containers Docker, garantindo um ambiente isolado e fácil de configurar.

## Tecnologias Utilizadas

A aplicação utiliza as seguintes tecnologias:

- **Python** (Framework: Django)
- **Docker** e **Docker Compose**
- **PostgreSQL**
- **HTML e CSS**
- **Nginx**
- **Gunicorn**

## Requisitos

Antes de executar a aplicação, certifique-se de ter os seguintes pré-requisitos instalados em sua máquina:

- [Git](https://git-scm.com/)
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)

## Passo a Passo para Execução (Linux)

1. **Clone o repositório do projeto**:
   ```bash
   git clone https://github.com/vitorgsantoss/blog-project.git
   ```

2. **Inicie o serviço Docker**:
   ```bash
   sudo systemctl start docker
   ```

3. **Acesse o diretório do projeto**:
   ```bash
   cd blog-project/
   ```

4. **Configure o ambiente**:
   - Crie o arquivo `.env` na pasta `dotenv_files` com base no arquivo `.env_example` fornecido:
     ```bash
     cp dotenv_files/.env_example dotenv_files/.env
     ```
   - Edite o arquivo `.env` conforme necessário para seu ambiente.

5. **Inicie a aplicação**:
   ```bash
   docker compose up --build
   ```

6. **Corrija permissões (se necessário)**:
   - Caso receba o erro abaixo:
     ```
     PermissionError: [Errno 13] Permission denied: '/data/web/static/admin'
     ```
   - Pare a aplicação com `Ctrl+C` e execute o seguinte comando para corrigir as permissões:
     ```bash
     sudo chmod -R 777 data
     ```
   - Reinicie a aplicação:
     ```bash
     docker compose up
     ```

## Acesso à Aplicação

Após a inicialização bem-sucedida, a aplicação estará disponível no navegador no seguinte endereço:

```
http://127.0.0.1:8000
```

## Contribuição

Para sugestões e melhorias, entrar em contato por e-mail: vitor.santos800411@gmail.com.

---

**Autor**: [Vitor G. Santos](https://github.com/vitorgsantoss)
