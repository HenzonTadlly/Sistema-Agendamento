# Sistema de Agendamento Profissional

Aplicação web desenvolvida com **Django** para gerenciamento de agendamentos entre **clientes** e **prestadores de serviço**, com controle de status, avaliação de atendimentos, perfil com foto e dashboard com métricas.

---

## Objetivo do Projeto

Este projeto foi desenvolvido com o objetivo de praticar e demonstrar conhecimentos em desenvolvimento **Full-Stack com Python e Django**, focando na construção de um sistema real com regras de negócio, autenticação, relacionamentos entre modelos e experiência de uso mais próxima de um produto real.

---

## Funcionalidades

### Autenticação e Perfis
- Cadastro de usuários
- Login e logout
- Escolha do tipo de usuário no cadastro:
  - Cliente
  - Prestador
- Criação automática de perfil
- Edição de perfil
- Upload de foto de perfil
- Cadastro de telefone e descrição

### Prestadores
- Definição dos serviços oferecidos
- Dashboard com métricas próprias
- Visualização de avaliações recebidas
- Alteração rápida de status dos agendamentos

### Clientes
- Criação de agendamentos
- Escolha de serviço
- Escolha de prestador
- Cancelamento de agendamento
- Avaliação de atendimento concluído
- Dashboard com histórico e métricas

### Agendamentos
- Criação de agendamento com:
  - serviço
  - prestador
  - data
  - horário
  - observação
- Impedimento de agendamento em data passada
- Impedimento de conflito de horário para o mesmo prestador
- Bloqueio de auto seleção do usuário como prestador
- Controle de status:
  - pendente
  - confirmado
  - concluído
  - cancelado

### Avaliações
- Avaliação de atendimento concluído
- Nota de 1 a 5
- Comentário opcional
- Bloqueio de avaliação duplicada
- Exibição de média de avaliações no dashboard do prestador

### Dashboard
- Dashboard específico por tipo de usuário
- Métricas de agendamentos
- Últimas avaliações recebidas
- Visual moderno com cards

---

## Tecnologias Utilizadas

- **Python**
- **Django**
- **SQLite**
- **HTML**
- **CSS**
- **JavaScript**
- **Pillow** (upload de imagens)

---

## Estrutura do Projeto

```bash
Sistema_Agendamento/
│
├── config/
├── usuarios/
├── servicos/
├── agendamentos/
├── avaliacoes/
├── templates/
├── static/
├── media/
├── manage.py
└── db.sqlite3