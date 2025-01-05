import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from openpyxl import Workbook, load_workbook
from googleapiclient.discovery import build
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.oauth2.credentials import Credentials
import os
import requests
from datetime import datetime


load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GOOGLE_CREDENTIALS = 'credentials.json'
NOTIFICATION_CHANNEL = int(os.getenv("NOTIFICATION_CHANNEL"))


intents = discord.Intents.all()
intents.message_content = True
intents.members = True

def get_dollar_exchange_rate():
    """Obtém a cotação atual do dólar em relação ao BRL."""
    API_URL = "https://api.exchangerate-api.com/v4/latest/USD"  
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        return data["rates"].get("BRL", None)  
    except Exception as e:
        print(f"❌ Erro ao buscar cotação do dólar: {e}")
        return None
    
# Inicializar o bot
bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    description="Bot para gerenciamento de pagamentos",
    help_command=commands.DefaultHelpCommand()
)

# Classe para gerenciamento de pagamentos
import io
from googleapiclient.http import MediaIoBaseDownload

class PaymentManager:
    def __init__(self, filename="payments.xlsx"):
        self.filename = filename
        self.payment_day = 10  
        self.data = {"members": {}}
        if not os.path.exists(self.filename):
            self.create_empty_file()
        self.load_data()

    def set_payment_day(self, day: int):
        """Define o dia de pagamento"""
        if day < 1 or day > 31:
            print("❌ O dia de pagamento deve ser entre 1 e 31.")
            return
        self.payment_day = day
        self.save_data()  


    def create_empty_file(self):
        """Cria um arquivo Excel vazio"""
        workbook = Workbook()
        sheet = workbook.active
        sheet.append(["UserID", "Username", "Payments"])  
        workbook.save(self.filename)
        print(f"✅ Arquivo vazio criado localmente: {self.filename}")


    def load_data(self):
        """Carrega dados do arquivo Excel"""
        if os.path.exists(self.filename):
            workbook = load_workbook(self.filename, data_only=True)
            sheet = workbook.active
            self.data["members"] = {
                str(row[0]): {"username": row[1], "payments": eval(row[2])}
                for row in sheet.iter_rows(min_row=2, values_only=True)
                if row[0] is not None 
            }
        else:
            self.save_data()


    def load_from_google_drive(self):
        """Baixa os dados mais recentes do Google Drive ou cria o arquivo se não existir"""
        SCOPES = ['https://www.googleapis.com/auth/drive.file']
        creds = Credentials.from_authorized_user_file(GOOGLE_CREDENTIALS, SCOPES)
        service = build('drive', 'v3', credentials=creds)

       
        query = f"name='{os.path.basename(self.filename)}'"
        response = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
        files = response.get('files', [])

        if files:
            file_id = files[0]['id']
            request = service.files().get_media(fileId=file_id)
            with open(self.filename, 'wb') as file:
                downloader = MediaIoBaseDownload(file, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
            print(f"✅ Arquivo carregado com sucesso do Google Drive: {self.filename}")
        else:
            print("❌ Arquivo não encontrado no Google Drive. Criando novo arquivo...")
            self.create_file_in_drive(service)

        self.load_data()

    def create_file_in_drive(self, service):
        """Cria o arquivo no Google Drive"""
        file_metadata = {'name': os.path.basename(self.filename)}
        media = MediaFileUpload(self.filename, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        # Criação do arquivo no Google Drive
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        file_id = file.get('id')
        print(f"✅ Arquivo criado com sucesso no Google Drive. Acesse em: https://drive.google.com/file/d/{file_id}")


    def save_data(self):
        """Salva os dados no arquivo Excel, atualizando registros existentes"""
        workbook = Workbook()
        sheet = workbook.active
        sheet.append(["UserID", "Username", "Payments"])  

        
        for user_id, info in self.data["members"].items():
            sheet.append([user_id, info["username"], str(info["payments"])])

        workbook.save(self.filename)


    def upload_to_google_drive(self, folder_id=None):
        """Faz upload do arquivo Excel para o Google Drive, substituindo o arquivo existente"""
        SCOPES = ['https://www.googleapis.com/auth/drive.file']
        creds = Credentials.from_authorized_user_file(GOOGLE_CREDENTIALS, SCOPES)
        service = build('drive', 'v3', credentials=creds)

       
        query = f"name='{os.path.basename(self.filename)}'"
        response = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
        files = response.get('files', [])

        if files:
        
            file_id = files[0]['id']
            file_metadata = {'name': os.path.basename(self.filename)}
            media = MediaFileUpload(self.filename, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            updated_file = service.files().update(fileId=file_id, body=file_metadata, media_body=media).execute()
            print(f"✅ Arquivo atualizado no Google Drive: {os.path.basename(self.filename)}")
        else:
           
            print("❌ Arquivo não encontrado no Google Drive. Criando novo arquivo...")
            file_metadata = {'name': os.path.basename(self.filename)}
            media = MediaFileUpload(self.filename, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print(f"✅ Arquivo criado no Google Drive: {os.path.basename(self.filename)}")


    def register_payment(self, user_id, username):
        """Registra o pagamento do usuário para o mês atual"""
        current_month = datetime.now().strftime("%Y-%m")
        user_id_str = str(user_id)  

        if user_id_str not in self.data["members"]:
           
            self.data["members"][user_id_str] = {"username": username, "payments": {}}
        
       
        self.data["members"][user_id_str]["payments"][current_month] = True
        self.save_data()


    def get_payment_status(self):
        """Retorna o status de pagamento de todos os membros"""
        current_month = datetime.now().strftime("%Y-%m")
        
        
        return [
            {"username": info["username"], "paid": info["payments"].get(current_month, False)}
            for info in self.data["members"].values()
        ]

    def register_initial_payment(self, user_id, username):
        """Registra todos os membros como pendentes no arquivo Excel."""
        current_month = datetime.now().strftime("%Y-%m")
        user_id_str = str(user_id) 

        if user_id_str not in self.data["members"]:
            
            self.data["members"][user_id_str] = {"username": username, "payments": {}}
        
        
        if current_month not in self.data["members"][user_id_str]["payments"]:
            self.data["members"][user_id_str]["payments"][current_month] = False 
        
        self.save_data()


    def has_paid(self, user_id):
        """Verifica se o usuário já pagou no mês atual"""
        current_month = datetime.now().strftime("%Y-%m")
        return user_id in self.data["members"] and current_month in self.data["members"][user_id]["payments"]

    def unregister_payment(self, user_id):
        """Remove o pagamento do usuário para o mês atual"""
        current_month = datetime.now().strftime("%Y-%m")
        user_id_str = str(user_id)  

        
        if user_id_str in self.data["members"]:
            payments = self.data["members"][user_id_str].get("payments", {})
            
            
            if current_month in payments:
                payments[current_month] = False 
                self.save_data()  
                self.upload_to_google_drive() 
                print(f"✅ Pagamento removido para o usuário {user_id_str}.")
                return True  
            else:
                print(f"❌ Nenhum pagamento encontrado para o usuário {user_id_str} no mês atual.")
                return False
        else:
            print(f"❌ Usuário {user_id_str} não está registrado.")
            return False


payment_manager = PaymentManager()

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
    guild = bot.guilds[0] 
    for member in guild.members:
        if not member.bot:  
            payment_manager.register_initial_payment(member.id, member.name)
    payment_manager.load_from_google_drive()
    check_payments.start()


@bot.command(name='paguei', help='Registra seu pagamento para o mês atual')
async def register_payment(ctx):
    """Registra o pagamento do membro e sincroniza com o Google Drive"""
    payment_manager.register_payment(ctx.author.id, ctx.author.name)
    payment_manager.upload_to_google_drive() 
    await ctx.send(f"✅ Pagamento registrado com sucesso para {ctx.author.name}!")


@bot.command(name='naopaguei', help='Remove seu registro de pagamento do mês atual')
async def unregister_payment(ctx):
    """Desfaz o pagamento do membro"""
    user_id = str(ctx.author.id)  
    
    if payment_manager.unregister_payment(user_id):
        await ctx.send(f"🔄 {ctx.author.name}, seu pagamento foi removido com sucesso para este mês.")
    else:
        await ctx.send(f"❌ {ctx.author.name}, você não tem um pagamento registrado para este mês.")



@bot.command(name='status', help='Mostra o status dos pagamentos de todos os membros')
async def payment_status(ctx):
    """Exibe o status de pagamento de todos os membros"""
    guild = ctx.guild
    for member in guild.members:
        if not member.bot:  
            payment_manager.register_initial_payment(member.id, member.name)

    
    status = payment_manager.get_payment_status()

   
    message = "📊 **Status dos Pagamentos do Mês Atual**\n\n"
    for member in status:
        emoji = "✅" if member["paid"] else "❌"
        payment_date = f"(Pago em: {datetime.now().strftime('%d/%m/%Y')})" if member["paid"] else "(Pendente)"
        message += f"{emoji} {member['username']} {payment_date}\n"

    await ctx.send(message)


@bot.command(name='preco', help='Exibe o preço atual da assinatura em BRL e por pessoa')
async def show_price(ctx):
    """Calcula e exibe o preço da assinatura com base na cotação atual do dólar, dividido entre 4 pessoas, com a data de vencimento e chave PIX."""
    
   
    exchange_rate = get_dollar_exchange_rate()
    if exchange_rate is None:
        await ctx.send("❌ Não foi possível obter a cotação atual do dólar. Tente novamente mais tarde.")
        return

   
    total_price = 20 * exchange_rate
    price_per_person = total_price / 4

  
    today = datetime.now()
    due_date = datetime(today.year, today.month, payment_manager.payment_day)
    due_date_str = due_date.strftime('%d/%m/%Y')

    pix_key = "146.980.396-81"  

    await ctx.send(
        f"💵 O preço total da assinatura de $20 é **R${total_price:.2f}**.\n"
        f"👥 Dividido por 4 pessoas, cada uma deve pagar **R${price_per_person:.2f}**.\n"
        f"📅 A data de vencimento para o pagamento é **{due_date_str}**.\n"
        f"💳 A chave PIX para pagamento é: **{pix_key}**."
    )



@tasks.loop(hours=24)
async def check_payments():
    """Tarefa automática para verificar pagamentos e notificar membros pendentes."""
    channel = bot.get_channel(NOTIFICATION_CHANNEL)
    if not channel:
        print("❌ Canal de notificações não encontrado.")
        return

    today = datetime.now()
    payment_date = datetime(today.year, today.month, payment_manager.payment_day)
    days_until_payment = (payment_date - today).days

    if days_until_payment in [2, 0]:
       
        payment_manager.load_from_google_drive()
        status = payment_manager.get_payment_status()

        
        pending_members = [f"<@{user_id}>" for user_id, info in payment_manager.data["members"].items() 
                           if not info["payments"].get(datetime.now().strftime("%Y-%m"), False)]

        
        exchange_rate = get_dollar_exchange_rate()
        if exchange_rate is not None:
            total_price = 20 * exchange_rate
            price_per_person = total_price / 4
            price_message = (
                f"\n💵 O preço total da assinatura de $20 é **R${total_price:.2f}**."
                f"\n👥 Dividido por 4 pessoas, cada uma deve pagar **R${price_per_person:.2f}**."
            )
        else:
            price_message = "\n❌ Não foi possível obter a cotação do dólar no momento."

       
        message = "🔔 **Lembrete de Pagamento**\n"
        if days_until_payment == 2:
            message += "Faltam 2 dias para o pagamento!\n\n"
        else:
            message += "O pagamento vence hoje!\n\n"

        if pending_members:
            message += f"📋 **Membros pendentes:**\n{', '.join(pending_members)}"
        else:
            message += "🎉 Todos os membros estão com os pagamentos em dia!"

        
        message += price_message

        await channel.send(message)


@bot.command(name='setdatapgamento', help='Define o dia de pagamento do mês')
async def set_payment_day(ctx, day: int):
    """Define o novo dia de pagamento"""
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Você não tem permissão para alterar o dia de pagamento.")
        return
    if day < 1 or day > 31:
        await ctx.send("❌ O dia de pagamento deve ser entre 1 e 31.")
        return
    
    payment_manager.payment_day = day
    await ctx.send(f"✅ O dia de pagamento foi atualizado para o dia {day} do mês.")


@bot.command(name='historico', help='Exibe o histórico de pagamentos de um usuário específico')
async def payment_history(ctx, member: discord.Member = None):
    """Exibe o histórico de pagamentos de um membro específico"""
    if member is None:
        await ctx.send("❌ Você precisa mencionar um membro. Exemplo: `!historico @usuario`")
        return

    user_id = str(member.id)
    if user_id not in payment_manager.data["members"]:
        await ctx.send(f"❌ Nenhum histórico encontrado para {member.name}.")
        return

    payments = payment_manager.data["members"][user_id]["payments"]
    if not payments:
        await ctx.send(f"📋 {member.name} não tem nenhum pagamento registrado.")
        return

    history = "\n".join(
        [f"📅 {month}: {'✅ Pago' if paid else '❌ Não Pago'}" for month, paid in sorted(payments.items())]
    )

    await ctx.send(f"📊 **Histórico de pagamentos de {member.name}:**\n{history}")


@bot.command(name='addmembro', help='Adiciona um novo membro ao sistema de pagamentos')
async def add_member(ctx, member: discord.Member):
    """Adiciona um novo membro ao sistema de pagamentos."""
    user_id = member.id
    username = member.name
    payment_manager.register_initial_payment(user_id, username)
    await ctx.send(f"✅ Membro {username} ({user_id}) adicionado ao sistema de pagamentos.")




@check_payments.before_loop
async def before_check_payments():
    await bot.wait_until_ready()

if __name__ == "__main__":
    bot.run(TOKEN)
