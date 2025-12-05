from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = 'app/service-account-key.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']
SEU_EMAIL_CORPORATIVO = 'silva.luanny@escolar.ifrn.edu.br'

def setup():
    print("Autenticando robô...")
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=creds)

    print("Criando novo calendário...")
    calendar_body = {
        'summary': 'Agendamentos do Sistema (Robot)',
        'timeZone': 'America/Sao_Paulo'
    }
    
    new_calendar = service.calendars().insert(body=calendar_body).execute()
    calendar_id = new_calendar['id']
    print(f"✅ Calendário criado com sucesso! ID: {calendar_id}")

    print(f"Compartilhando com {SEU_EMAIL_CORPORATIVO}...")
    rule = {
        'scope': {
            'type': 'user',
            'value': SEU_EMAIL_CORPORATIVO,
        },
        'role': 'owner'
    }

    try:
        service.acl().insert(calendarId=calendar_id, body=rule).execute()
        print(f"✅ Calendário compartilhado com sucesso com {SEU_EMAIL_CORPORATIVO}")
    except Exception as e:
        print(f"⚠️ Aviso: O robô criou o calendário, mas não conseguiu compartilhar com você devido a regras da empresa.")
        print(f"Erro: {e}")
        print("Mas não tem problema! O sistema vai funcionar, você só não vai ver os eventos na sua agenda visualmente.")

    print("-" * 30)
    print("AGORA ATUALIZE SEU ARQUIVO .ENV / CONFIG COM ESTE ID:")
    print(f"GOOGLE_CALENDAR_ID={calendar_id}")
    print("-" * 30)

if __name__ == '__main__':
    setup()