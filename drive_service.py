
import os.path
import streamlit as st
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

# Si modificas estos alcances, elimina el archivo token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

# --- CONFIGURACIÓN ---
# ID de la carpeta en Google Drive que contiene los materiales de onboarding.
# Reemplaza 'TU_FOLDER_ID_AQUI' con el ID real de tu carpeta.
ONBOARDING_FOLDER_ID = "1PTOxI2kNLZe0yfcCCmIVhV_UCM5-pKgZ"

class DriveService:
    """Servicio para interactuar con la API de Google Drive."""
    def __init__(self):
        self.creds = self._get_credentials()

    def _get_credentials(self):
        """Obtiene las credenciales de usuario, manejando el flujo de autenticación."""
        creds = None
        
        # Try to load from st.secrets (for Streamlit Cloud deployment)
        if "google_token" in st.secrets:
            try:
                creds = Credentials.from_authorized_user_info(
                    info=st.secrets["google_token"].to_dict(),
                    scopes=SCOPES
                )
            except Exception as e:
                print(f"Error loading token from st.secrets: {e}")

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Error al refrescar el token desde st.secrets: {e}")
                    creds = self._run_auth_flow() # Fallback to interactive flow if refresh fails
            else:
                creds = self._run_auth_flow() # Initial interactive flow or if no token in secrets
            
            # If running locally and new creds obtained, save them to token.json
            if not "google_token" in st.secrets and creds:
                with open('google_credentials/token.json', "w") as token:
                    token.write(creds.to_json())
        return creds

    def _run_auth_flow(self):
        """Ejecuta el flujo de autenticación interactivo (local only)."""
        # This flow is primarily for local development and initial token generation.
        # On Streamlit Cloud, credentials should come from st.secrets.
        if "google_credentials" in st.secrets:
            client_config = st.secrets["google_credentials"].to_dict()
        else:
            # Fallback for local development if credentials.json exists
            if os.path.exists('google_credentials/credentials.json'):
                with open('google_credentials/credentials.json', 'r') as f:
                    client_config = json.load(f)['installed'] # Assuming 'installed' type
            else:
                print(f"Error: No se encuentra el archivo de credenciales en 'google_credentials/credentials.json' ni en st.secrets.")
                return None
        
        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
        creds = flow.run_local_server(port=0)
        return creds

    def search_files(self, query, folder_id=None, page_size=5):
        """Busca archivos en Google Drive, opcionalmente dentro de una carpeta específica."""
        if not self.creds:
            print("No se pudieron obtener las credenciales. Búsqueda cancelada.")
            return []

        try:
            service = build("drive", "v3", credentials=self.creds)
            
            search_query = f"name contains '{query}' and mimeType != 'application/vnd.google-apps.folder'"
            if folder_id:
                search_query += f" and '{folder_id}' in parents"

            response = (
                service.files()
                .list(
                    q=search_query,
                    pageSize=page_size,
                    fields="nextPageToken, files(id, name, webViewLink)",
                )
                .execute()
            )
            files = response.get("files", [])
            
            print(f"Se encontraron {len(files)} archivos para la consulta: '{query}' en la carpeta: {folder_id}")
            return files
        except HttpError as error:
            print(f"Ocurrió un error con la API de Drive: {error}")
            return []
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            return []


    def upload_file(self, file_name, file_path, mime_type):
        """Sube un archivo a Google Drive."""
        if not self.creds:
            print("No se pudieron obtener las credenciales. Subida cancelada.")
            return None

        try:
            service = build("drive", "v3", credentials=self.creds)
            file_metadata = {"name": file_name}
            from googleapiclient.http import MediaFileUpload
            media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
            file = service.files().create(body=file_metadata, media_body=media, fields="id, webViewLink").execute()
            print(f"Archivo '{file_name}' subido. ID: {file.get('id')}, Link: {file.get('webViewLink')}")
            return file
        except HttpError as error:
            print(f"Ocurrió un error al subir el archivo: {error}")
            return None
        except Exception as e:
            print(f"Ocurrió un error inesperado al subir el archivo: {e}")
            return None

    def get_file_content(self, file_id):
        """Descarga el contenido de un archivo de Google Drive."""
        if not self.creds:
            print("No se pudieron obtener las credenciales. Descarga cancelada.")
            return None

        try:
            service = build("drive", "v3", credentials=self.creds)
            request = service.files().get_media(fileId=file_id)
            
            # Use io.BytesIO to handle the file content in memory
            import io
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}%.")
            
            fh.seek(0) # Rewind to the beginning of the file-like object
            return fh.read().decode('utf-8') # Assuming text content for now
        except HttpError as error:
            print(f"Ocurrió un error al descargar el archivo: {error}")
            return None
        except Exception as e:
            print(f"Ocurrió un error inesperado al descargar el archivo: {e}")
            return None

# --- BLOQUE DE PRUEBA ---
if __name__ == "__main__":
    print("Ejecutando prueba del servicio de Google Drive...")
    drive_service = DriveService()
    
    if drive_service.creds:
        print("\nCredenciales obtenidas exitosamente.")
        
        # Ejemplo de búsqueda
        search_query = "manual"
        print(f"\nBuscando archivos que contengan la palabra: '{search_query}'...")
        found_files = drive_service.search_files(search_query)

        if found_files:
            print("\nArchivos encontrados:")
            for item in found_files:
                print(f"- Nombre: {item['name']} (ID: {item['id']})")
                print(f"  Link: {item['webViewLink']}")
        else:
            print("No se encontraron archivos para esa consulta.")
    else:
        print("\nNo se pudo inicializar el servicio de Drive. Verifica tus credenciales.")
