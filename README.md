# Sistema de Agendamento 
Aplicação web desenvolvida com **Django** para gerenciamento de agendamentos entre **clientes** e **prestadores de serviço**, com autenticação por perfis, controle de status, avaliação de atendimentos, edição de perfil com foto e dashboard personalizado.

---

## Sobre o projeto

O **Sistema de Agendamento Profissional** foi desenvolvido como projeto de portfólio com o objetivo de demonstrar habilidades em desenvolvimento **Full-Stack com Python e Django**, aplicando regras de negócio reais, autenticação, relacionamento entre modelos, validações e organização de fluxo por tipo de usuário.

O sistema foi projetado para simular um ambiente real de agendamento de serviços, no qual clientes podem solicitar atendimentos e prestadores podem gerenciar seus serviços, confirmações, conclusões e avaliações recebidas.

---

## Funcionalidades

### Autenticação e perfis
- Cadastro de usuários
- Login e logout
- Escolha do tipo de usuário no cadastro:
  - Cliente
  - Prestador
- Criação automática de perfil
- Edição de perfil
- Upload de foto de perfil
- Cadastro de telefone e descrição

### Cliente
- Criar agendamentos
- Escolher serviço
- Escolher prestador disponível
- Cancelar agendamentos permitidos
- Avaliar atendimentos concluídos
- Visualizar dashboard com histórico e métricas

### Prestador
- Definir serviços oferecidos
- Confirmar agendamentos pendentes
- Concluir agendamentos confirmados
- Visualizar avaliações recebidas
- Acompanhar métricas no dashboard

### Agendamentos
- Criação de agendamento com:
  - serviço
  - prestador
  - data
  - horário
  - observação
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
- Dashboard específico para cliente
- Dashboard específico para prestador
- Métricas por tipo de usuário
- Histórico de agendamentos
- Últimas avaliações recebidas

---

## Regras de negócio implementadas

- Apenas **clientes** podem criar agendamentos
- Apenas **prestadores** podem confirmar ou concluir agendamentos
- Clientes só podem cancelar seus próprios agendamentos
- Não é permitido criar agendamento em **data passada**
- Não é permitido criar dois agendamentos no mesmo dia e horário para o mesmo prestador
- O usuário não pode selecionar a si mesmo como prestador
- O prestador precisa oferecer o serviço escolhido
- Um atendimento só pode ser avaliado **uma única vez**
- Após a avaliação, o botão de avaliar deixa de ser exibido
- Status finais (`cancelado` e `concluído`) não podem voltar para estados anteriores

---

## Tecnologias utilizadas

- **Python**
- **Django**
- **SQLite**
- **HTML**
- **CSS**
- **JavaScript**
- **Pillow**

---

## Estrutura do projeto

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
├── manage.py
├── README.md
├── requirements.txt
└── .gitignore
