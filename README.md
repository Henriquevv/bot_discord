# Bot de Gerenciamento de Pagamentos no Discord

Este bot foi desenvolvido para gerenciar pagamentos de assinaturas compartilhadas no Discord. Ele automatiza processos como a atualização da cotação do dólar, gerenciamento de pagamentos, notificações automáticas, e mais.

---

## Funcionalidades

- Atualização automática da cotação do dólar.
- Gerenciamento completo de pagamentos, incluindo histórico e controle de membros.
- Registro e remoção de pagamentos.
- Notificações automáticas de vencimento e pagamentos pendentes.
- Sincronização de dados com o Google Drive.
- Registro de comprovantes de pagamento.
- Configurações avançadas, como pagamento automático e vinculação de contas.

---

## Comandos Disponíveis

### Geral

- **`!preco`**  
  Mostra o preço da assinatura (em BRL), dividido entre os membros, e a data de vencimento.
  
  **Exemplo de Resposta:**
  ```
  💵 Cotação atual do dólar: R$5.25.
  💵 O preço total da assinatura de $20 é R$105.00.
  👥 Dividido por 4 pessoas, cada uma deve pagar R$26.25.
  📅 A data de vencimento para o pagamento é 05/01/2025.
  💳 A chave PIX para pagamento é: XXX.XXX.XXX-XX.
  ```

- **`!status`**  
  Exibe o status de pagamento dos membros no mês atual.
  
  **Exemplo de Resposta:**
  ```
  📊 Status dos Pagamentos do Mês Atual

  ❌ xxxxxxxx (Pendente)
  ❌ xxxxxxxx (Pendente)
  ✅ yyyyyyyy (Pago)
  ```

- **`!historico @membro`**  
  Mostra o histórico de pagamentos de um membro específico.
  
  **Exemplo de Resposta:**
  ```
  📊 Histórico de pagamentos de henrique.v:
  📅 2025-01: ❌ Não Pago
  📅 2025-02: ✅ Pago
  ```

- **`!arquivos`**  
  Envia o link da pasta no Google Drive onde os dados estão armazenados.
  
  **Exemplo de Resposta:**
  ```
  📂 Aqui está o link para a pasta no Google Drive: https://drive.google.com/drive/folders/xxxxxxxxxxxxx?usp=sharing
  ```

---

### Gerenciamento de Pagamentos

- **`!paguei`**  
  Registra seu pagamento e, opcionalmente, anexa o comprovante.
  
  **Exemplo de Resposta:**
  ```
  ✅ Pagamento registrado com sucesso para xxxxxxxx!
  ```

- **`!naopaguei`**  
  Remove o registro do pagamento do mês atual ou próximo.
  
  **Exemplo de Resposta:**
  ```
  🔄 xxxxxxxx, seu pagamento foi removido com sucesso para este mês.
  ```

- **`!pagamentoauto @membro`**  
  Configura um membro para ter pagamento automático.
  
  **Exemplo de Resposta:**
  ```
  ✅ O membro @membro foi configurado para pagamento automático todos os meses.
  ```

- **`!pago @membro YYYY-MM`**  
  Permite que administradores marquem um membro como pago para um mês específico.
  
  **Exemplo de Resposta:**
  ```
  ✅ Pagamento registrado para @membro no mês YYYY-MM.
  ```

---

### Gerenciamento de Membros

- **`!addmembro @membro`**  
  Adiciona um novo membro ao sistema.
  
  **Exemplo de Resposta:**
  ```
  ✅ O membro @membro foi adicionado ao sistema com o status de pagamento pendente.
  ```

- **`!removemembro @membro`**  
  Remove um membro do sistema.
  
  **Exemplo de Resposta:**
  ```
  ✅ O membro @membro foi removido do sistema de pagamentos.
  ```

- **`!linkcontas @principal @secundaria`**  
  Vincula uma conta secundária a uma conta principal.
  
  **Exemplo de Resposta:**
  ```
  ✅ Conta @secundaria foi vinculada à principal @principal.
  ```

---

### Administração

- **`!setdatapgamento <dia>`**  
  Define o dia do vencimento.
  
  **Exemplo de Resposta:**
  ```
  ✅ O dia de pagamento foi atualizado para o dia <dia> do mês.
  ```

- **`!limpar`**  
  Limpa todas as mensagens do canal atual (apenas para administradores).
  
  **Exemplo de Resposta:**
  ```
  ✅ Todas as mensagens foram apagadas com sucesso.
  ```

---

## Configuração

### Passo 1: Clone o repositório

```bash
git clone https://github.com/Henriquevv/bot_discord.git
cd bot_discord
```

### Passo 2: Instale as dependências

```bash
pip install -r requirements.txt
```

### Passo 3: Configure o token e outros parâmetros

Crie um arquivo `.env` com os seguintes dados:

```env
DISCORD_TOKEN=seu-token-aqui
NOTIFICATION_CHANNEL=id-do-canal
```

### Passo 4: Inicie o bot

```bash
python main.py
```

---

## Stack Utilizada

- **Linguagem**: Python 3.13
- **APIs**: Discord, Google Drive


