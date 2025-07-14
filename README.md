# Lume - Plataforma de Apoio Emocional

## 📋 Sobre o Projeto

O **Lume** é uma plataforma web desenvolvida em Django que oferece apoio emocional, conteúdo terapêutico e ferramentas de reinserção social para pessoas em processo de recuperação de dependência química.

## 🚀 Funcionalidades

### ✅ Implementadas
- **Home Page**: Página inicial com design moderno e responsivo
- **Sistema de Autenticação**: Login e logout de usuários
- **Chat de Apoio**: Interface de chat simulado para suporte emocional
- **Conteúdo Terapêutico**: Informações educativas sobre dependência e recuperação
- **Metas e Check-in**: Sistema para definir metas diárias e registrar humor
- **Diário Pessoal**: Espaço para registros pessoais com controle de humor
- **Design Responsivo**: Compatível com desktop, tablet e mobile
- **Interface Moderna**: Design limpo com cores terapêuticas (#ABD977)

## 🛠️ Tecnologias Utilizadas

- **Backend**: Django 5.2.4
- **Frontend**: HTML5, CSS3, JavaScript
- **Framework CSS**: Bootstrap 4.5.2
- **Banco de Dados**: SQLite
- **Ícones**: Font Awesome
- **Responsividade**: CSS Grid e Flexbox

## 📁 Estrutura do Projeto

```
Lume_project/
├── manage.py
├── lume_core/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── lume_app/
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── views.py
│       ├── urls.py
│       ├── tests.py
│       ├── migrations/
│       ├── templates/
│       │   ├── base.html
│       │   ├── index.html
│       │   ├── login.html
│       │   ├── chat.html
│       │   ├── conteudo.html
│       │   ├── metas.html
│       │   └── diario.html
│       └── static/
│           └── app/
│               ├── css/
│               └── js/
└── staticfiles/
```

## 🔧 Instalação e Configuração

### Pré-requisitos
- Python 3.8+
- pip

### Passos para instalação

1. **Clone o projeto**
```bash
git clone <url-do-repositorio>
cd Lume_project
```

2. **Instale as dependências**
```bash
pip install Django
```

3. **Execute as migrações**
```bash
python manage.py migrate
```

4. **Crie um superusuário (opcional)**
```bash
python manage.py createsuperuser
```

5. **Colete os arquivos estáticos**
```bash
python manage.py collectstatic
```

6. **Execute o servidor**
```bash
python manage.py runserver
```

7. **Acesse a aplicação**
- Abra o navegador em: `http://localhost:8000`
- Admin: `http://localhost:8000/admin`

## 👤 Usuário de Teste

- **Usuário**: admin
- **Senha**: admin123
- **Email**: admin@lume.com

## 📱 Páginas Disponíveis

| Página | URL | Descrição |
|--------|-----|-----------|
| Home | `/` | Página inicial com frases motivacionais |
| Login | `/login/` | Autenticação de usuários |
| Chat | `/chat/` | Chat de apoio simulado |
| Conteúdo | `/conteudo/` | Informações terapêuticas |
| Metas | `/metas/` | Definição de metas e check-in emocional |
| Diário | `/diario/` | Registro pessoal de pensamentos |
| Admin | `/admin/` | Painel administrativo |

## 🎨 Design e UX

### Cores Principais
- **Verde Principal**: #ABD977
- **Verde Hover**: #9BC765
- **Branco**: #FFFFFF
- **Cinza Claro**: #F8F9FA

### Características do Design
- Interface limpa e moderna
- Animações suaves e micro-interações
- Gradientes e sombras para profundidade
- Responsividade completa
- Acessibilidade considerada

## 🔒 Modelos de Dados

### Principais Modelos
- **FraseMotivacional**: Frases inspiradoras para a home
- **Diario**: Registros pessoais dos usuários
- **CheckinEmocional**: Registro de humor diário
- **MetaTerapeutica**: Metas definidas por psicólogos
- **Mensagem**: Sistema de mensagens do chat
- **Psicologo**: Cadastro de profissionais

## 🚀 Funcionalidades Futuras

- [ ] Sistema de notificações
- [ ] Integração com APIs de terceiros
- [ ] Chat em tempo real com WebSockets
- [ ] Sistema de gamificação
- [ ] Relatórios de progresso
- [ ] Integração com calendário
- [ ] Sistema de grupos de apoio
- [ ] Aplicativo mobile

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Contato

- **Projeto**: Lume
- **Email**: contato@lume.com
- **Website**: [Em desenvolvimento]

---

**Desenvolvido com ❤️ para ajudar pessoas em sua jornada de recuperação**

