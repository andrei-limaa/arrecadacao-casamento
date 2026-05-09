# 💍 Sistema de Presentes de Casamento

Sistema desenvolvido em Django para gerenciamento de contribuições de casamento via Pix.

---

# 🌿 Funcionalidades

* ✅ Geração de pagamento via Pix
* ✅ QR Code automático
* ✅ Integração com Mercado Pago
* ✅ Painel administrativo
* ✅ Lista de contribuições
* ✅ Controle de status dos pagamentos
* ✅ Exibição do total arrecadado

---

# 🚀 Tecnologias Utilizadas

* Python
* Django
* MySQL
* Mercado Pago SDK

---

# ⚙️ Instalação

## 1️⃣ Clone o repositório

```bash
git clone URL_DO_REPOSITORIO
```

## 2️⃣ Acesse a pasta do projeto

```bash
cd nome-do-projeto
```

## 3️⃣ Crie um ambiente virtual

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## 4️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

## 5️⃣ Configure o banco de dados

Edite o arquivo `settings.py` com as informações do MySQL.

---

# ▶️ Executando o Projeto

Execute as migrations:

```bash
python manage.py migrate
```

Inicie o servidor:

```bash
python manage.py runserver
```

Acesse:

```text
http://127.0.0.1:8000/
```

---

# 💳 Integração Mercado Pago

Configure suas credenciais do Mercado Pago no projeto:

```python
MERCADO_PAGO_ACCESS_TOKEN = "SEU_TOKEN"
```

---

# 📌 Estrutura do Sistema

O sistema permite:

* Criar contribuições
* Gerar pagamentos instantaneamente
* Validar pagamentos realizados
* Acompanhar valores arrecadados
* Gerenciar contribuições pelo painel administrativo

---

# 💍 Projeto

Sistema criado para Jefferson & Carla 🌿

Desenvolvido com carinho para tornar os presentes do casamento mais práticos e modernos.
