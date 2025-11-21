from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
from app.core.config import settings
from app.schemas.agenda import CriarAgenda

def get_calendar_service():
    try:
        creds = service_account.Credentials.from_service_account_file(
            settings.GOOGLE_SERVICE_ACCOUNT_FILE, scopes=[settings.SCOPES]
        )
        return build('calendar', 'v3', credentials=creds)
    except Exception as e:
        print(f"Erro ao carregar credenciais do Google: {e}")
        return None

def create_calendar_event(schema: CriarAgenda):
    service = get_calendar_service()
    if not service:
        return None

    start_datetime = datetime.combine(schema.data_agendamento, datetime.min.time())
    start_datetime = start_datetime.replace(hour=schema.hora_inicio)
    
    end_datetime = start_datetime + timedelta(hours=1)

    event_body = {
        'summary': f'Agendamento PC {schema.numero_computador}',
        'description': f'Reserva realizada via sistema para o computador {schema.numero_computador}',
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': 'America/Sao_Paulo',
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': 'America/Sao_Paulo',
        },
        # 'attendees': [
        #     {'email': schema.email_usuario},
        # ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 60},
                {'method': 'popup', 'minutes': 15},
            ],
        },
    }

    try:
        event = service.events().insert(
            calendarId=settings.GOOGLE_CALENDAR_ID,
            body=event_body,
            # sendNotifications=True
        ).execute()
        return event.get('id')
    except Exception as e:
        print(f"Erro ao criar evento no Google Calendar: {e}")
        return None

def delete_calendar_event(event_id: str):
    service = get_calendar_service()
    if not service:
        return False

    try:
        service.events().delete(
            calendarId=settings.GOOGLE_CALENDAR_ID,
            eventId=event_id
        ).execute()
        print(f"Evento {event_id} deletado do Google Calendar com sucesso.")
        return True
    except Exception as e:
        print(f"Erro ao deletar evento no Google (pode já ter sido removido): {e}")
        return False