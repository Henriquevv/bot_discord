
# Bot de Gerenciamento de Pagamentos Discord

Este bot foi desenvolvido para gerenciar pagamentos de assinaturas compartilhadas, exibindo valores atualizados com base na cotação do dólar, dividindo entre membros, e incluindo informações como data de vencimento e chave PIX para pagamento.


## Funcionalidades

- Cotação do dolar atual
- Gerenciamento de pagamento
- Notificações de pagamento


## Comandos Disponíveis

`!preco`

- Exibe o valor do dolar e da assinatura, dividido entre 4 pessoas, com base na cotação atual do dólar, além da data de vencimento e chave PIX.
```
💵 Cotação atual do dólar: R$5.25.
💵 O preço total da assinatura de $20 é R$105.00.
👥 Dividido por 4 pessoas, cada uma deve pagar R$26.25.
📅 A data de vencimento para o pagamento é 05/01/2025.
💳 A chave PIX para pagamento é: XXX.XXX.XXX-XX.
```


`!paguei`

- Registra o pagamento feito em um arquivo excel na nuvem.

```
✅ Pagamento registrado com sucesso para xxxxxxxx!
```

`!naopaguei`

- Tira do registro o pagamento do mes atual. (em caso de )

```
🔄 xxxxxxxx, seu pagamento foi removido com sucesso para este mês.
```

`!status`

- Exibe o status de pagamento de todos os membros registrados no sistema deste mês.

```
📊 Status dos Pagamentos do Mês Atual

❌ xxxxxxxx (Pendente)
❌ xxxxxxxx (Pendente)
❌ xxxxxxxx (Pendente)
❌ xxxxxxxx (Pendente)
```

`!historico @membro`

-  Exibe o histórico de pagamentos de um usuário específico

```
📊 Histórico de pagamentos de henrique.v:
📅 2025-01: ❌ Não Pago
```

`setdatapgamento <dia>`

- Define o dia de pagamento do mês

```
✅ O dia de pagamento foi atualizado para o dia X do mês.
```

`addmembro`

- Adiciona um novo membro ao sistema de pagamentos

```
✅ Membro {username} ({user_id}) adicionado ao sistema de pagamentos.
```

## Configuração

1- Clone o repositório

```bash
git clone https://github.com/Henriquevv/bot_discord.git
cd bot_discord
```
2- Instale as dependências:

```bash
pip install -r requirements.txt
```

3- Configure o token do bot (discord dev) no arquivo .env:

```bash
DISCORD_TOKEN=seu-token-aqui
```

4- Inicie o bot:

```bash
python bot.py
```

## Stack utilizada

- Python 3.13
- Google Drive API


