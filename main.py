
import streamlit as st
from drive_service import DriveService, ONBOARDING_FOLDER_ID
from database import setup_database, ProgressTracker, RAE_LIBRARY_DATA, ONBOARDING_PLAN_DATA, KNOWLEDGE_DOCUMENT_CONTENT
from agents import CultureGuide, OrgNavigator, ProcessMaster, AssessmentBot
from dashboard import create_competency_spider_chart, get_rae_status_list
import os
import tempfile
import json
import uuid

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(layout="wide", page_title="Onboarding Inteligente - Mantis FICC")

# --- INICIALIZACIÓN ---
@st.cache_resource
def init_systems():
    """Inicializa y cachea los sistemas principales."""
    setup_database() # Asegura que la DB y las tablas existan
    drive_service = DriveService()
    
    # --- Validación de Conexión a Drive ---
    if 'drive_validated' not in st.session_state:
        print("--- VALIDANDO CONEXIÓN A GOOGLE DRIVE ---")
        # Intenta buscar un archivo común como "Manual" para validar.
        test_files = drive_service.search_files("Manual", folder_id=ONBOARDING_FOLDER_ID)
        if test_files is not None:
            print(f"Validación exitosa. Se encontraron {len(test_files)} archivos de prueba.")
            st.session_state.drive_validated = True
        else:
            print("Falló la validación de Google Drive. Revisa las credenciales y permisos.")
            st.session_state.drive_validated = False
    
    return {
        "tracker": ProgressTracker(),
        "agents": {
            'cultura': CultureGuide,
            'organizacion': OrgNavigator,
            'procesos': ProcessMaster,
            'evaluacion': AssessmentBot
        },
        "drive": drive_service
    }

def get_drive_service():
    """Obtiene una instancia del servicio de Drive del cache."""
    return systems["drive"]

systems = init_systems()
tracker = systems["tracker"]
agents = systems["agents"]
culture_guide = agents['cultura']()
org_navigator = agents['organizacion']()
process_master = agents['procesos']()
assessment_bot = agents['evaluacion']()

# --- MANEJO DE ESTADO DE SESIÓN ---
def init_session_state():
    """Inicializa el estado de la sesión de Streamlit."""
    if 'user_id' not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())
        st.session_state.user_name = None
        st.session_state.onboarding_stage = 'name_collection'
    
    if 'progress' not in st.session_state:
        progress = tracker.get_user_progress(st.session_state.user_id)
        st.session_state.progress = progress if progress else None
        if progress:
            st.session_state.user_name = progress.get('user_name')
            st.session_state.onboarding_stage = 'onboarding_active'

    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if 'rae_sub_stage' not in st.session_state:
        st.session_state.rae_sub_stage = 'teaching'
        
    if 'found_files' not in st.session_state:
        st.session_state.found_files = []

    if 'instructional_mode_active' not in st.session_state:
        st.session_state.instructional_mode_active = False
    if 'current_instruction_index' not in st.session_state:
        st.session_state.current_instruction_index = 0

init_session_state()

def move_to_next_rae(current_progress, user_name):
    """Avanza al siguiente RAE o etapa y genera el mensaje correspondiente."""
    current_stage = current_progress.get('current_stage', 'cultura')
    current_rae_id = current_progress.get('current_rae_id')
    updates = {}
    response_text = ""

    current_stage_index = next((i for i, stage in enumerate(ONBOARDING_PLAN_DATA) if stage['stage'] == current_stage), -1)

    if current_stage_index != -1:
        current_stage_raes = ONBOARDING_PLAN_DATA[current_stage_index]['raes']
        current_rae_index = current_stage_raes.index(current_rae_id) if current_rae_id in current_stage_raes else -1

        if current_rae_index != -1 and current_rae_index < len(current_stage_raes) - 1:
            next_rae_id = current_stage_raes[current_rae_index + 1]
            updates['current_rae_id'] = next_rae_id
            response_text = f"\n\n¡Excelente, {user_name}! Has aprobado el objetivo anterior."
        else:
            response_text = f"\n\n🎉 ¡Has completado todos los objetivos de la etapa de **{current_stage.capitalize()}**!, {user_name}!"
            next_stage_index = current_stage_index + 1
            if next_stage_index < len(ONBOARDING_PLAN_DATA):
                next_stage_data = ONBOARDING_PLAN_DATA[next_stage_index]
                updates['current_stage'] = next_stage_data['stage']
                updates['current_rae_id'] = next_stage_data['raes'][0] if next_stage_data['raes'] else None
            else:
                updates['current_stage'] = 'completado'
                updates['current_rae_id'] = None
                response_text += f"\n\n🏆 **¡FELICITACIONES, {user_name}!** Has completado todo el programa de onboarding."
    
    st.session_state.rae_sub_stage = 'teaching'
    st.session_state.found_files = [] # Limpiar archivos encontrados
    return updates, response_text


def process_user_input(user_prompt, tracker, assessment_bot, culture_guide, org_navigator, process_master, drive_service):
    user_id = st.session_state.user_id
    user_name = st.session_state.user_name
    current_progress = tracker.get_user_progress(user_id)
    current_stage = current_progress.get('current_stage', 'cultura')
    current_rae_id = current_progress.get('current_rae_id')
    rae_info = RAE_LIBRARY_DATA.get(current_rae_id)

    # --- Detección de intenciones globales ---
    instructional_keywords = ["primer paso", "explícame el onboarding", "dame el contenido", "modo instruccional"]
    drive_keywords = ["recursos", "material de drive", "ayuda", "documento"]

    if any(keyword in user_prompt.lower() for keyword in instructional_keywords) and not st.session_state.instructional_mode_active:
        st.session_state.instructional_mode_active = True
        st.session_state.current_instruction_index = 0
        st.session_state.rae_sub_stage = 'teaching' # Reiniciar a teaching para empezar la secuencia
        return "¡Excelente! Comenzaremos con el modo instruccional. Te guiaré paso a paso por el contenido de cada etapa. Cuando estés listo para el siguiente bloque, solo dímelo."

    if any(keyword in user_prompt.lower() for keyword in drive_keywords):
        with st.spinner("Buscando en Google Drive..."):
            resource_name = "Plantilla_Gestion_Conocimiento"
            found_files = drive_service.search_files(resource_name, folder_id=ONBOARDING_FOLDER_ID)
            st.session_state.found_files = found_files
        
        if not found_files:
            return "No pude encontrar el documento 'Plantilla_Gestion_Conocimiento' en la carpeta de onboarding de Google Drive."
        
        file_links = "\n".join([f"- [{file_item['name']}]({file_item['webViewLink']})" for file_item in found_files])
        return f"¡Claro! Encontré los siguientes documentos para ti:\n{file_links}\n\nPuedes hacer clic en ellos para abrirlos."

    # --- Lógica para el modo instruccional ---
    if st.session_state.instructional_mode_active:
        current_stage_data = next((stage for stage in ONBOARDING_PLAN_DATA if stage['stage'] == current_stage), None)
        if not current_stage_data:
            st.session_state.instructional_mode_active = False
            return "Error: No se encontró información para la etapa actual."

        stage_raes = current_stage_data['raes']
        
        if st.session_state.rae_sub_stage == 'teaching':
            if st.session_state.current_instruction_index < len(stage_raes):
                current_rae_to_teach_id = stage_raes[st.session_state.current_instruction_index]
                rae_to_teach_info = RAE_LIBRARY_DATA.get(current_rae_to_teach_id)
                if rae_to_teach_info:
                    # Usar el agente para extraer el contenido dinámicamente
                    with st.spinner("Preparando el siguiente tema..."):
                        instructional_content = culture_guide.get_instructional_snippet(KNOWLEDGE_DOCUMENT_CONTENT, rae_to_teach_info)
                    
                    response_text = f'''**Contenido para {rae_to_teach_info['stage'].capitalize()} - {current_rae_to_teach_id}:**

{instructional_content}

Cuando estés listo/a para el siguiente bloque de información, dímelo. También puedes hacerme cualquier pregunta sobre el material.'''
                    st.session_state.rae_sub_stage = 'waiting_for_next_instruction'
                    return response_text
                else:
                    st.session_state.current_instruction_index += 1
                    return "No se encontró contenido para este RAE. Pasando al siguiente..."
            else:
                # Todos los RAEs de la etapa actual han sido presentados
                st.session_state.rae_sub_stage = 'stage_evaluation_ready'
                return f"¡Hemos cubierto todo el contenido de la etapa de **{current_stage.capitalize()}**! Ahora es momento de evaluar tu comprensión. ¿Estás listo/a para las preguntas?"

        elif st.session_state.rae_sub_stage == 'waiting_for_next_instruction':
            affirmative_responses = ['sí', 'si', 'listo', 'lista', 'dale', 'ok', 'vale', 'adelante', 'siguiente', 'continuar']
            if any(word in user_prompt.lower() for word in affirmative_responses):
                st.session_state.current_instruction_index += 1
                st.session_state.rae_sub_stage = 'teaching'
                return process_user_input("", tracker, assessment_bot, culture_guide, org_navigator, process_master, drive_service)
            else:
                # Si no es una respuesta afirmativa, responder usando el documento completo
                ai_response_to_question = culture_guide.answer_question_about_content(KNOWLEDGE_DOCUMENT_CONTENT, user_prompt)
                response_text = f'''{ai_response_to_question}

¿Hay algo más que te gustaría que te aclare, {user_name}? O, ¿estás listo/a para el siguiente bloque de contenido?'''
                return response_text
        
        elif st.session_state.rae_sub_stage == 'stage_evaluation_ready':
            affirmative_responses = ['sí', 'si', 'listo', 'lista', 'dale', 'ok', 'vale', 'adelante', 'comencemos']
            if any(word in user_prompt.lower() for word in affirmative_responses):
                st.session_state.rae_sub_stage = 'assessing'
                st.session_state.current_instruction_index = 0
                current_rae_id = stage_raes[0]
                rae_info = RAE_LIBRARY_DATA.get(current_rae_id)
                response_text = f'''¡Perfecto! Aquí va la primera pregunta de la etapa de {current_stage.capitalize()}:

> **{rae_info['description']}**'''
                return response_text
            else:
                return f"No hay problema, {user_name}. Avísame cuando estés listo/a para comenzar la evaluación de la etapa de {current_stage.capitalize()}."

    # --- Lógica original para cuando el modo instruccional NO está activo ---
    if not rae_info:
        return "Error: No se encontró información para el RAE actual."

    if st.session_state.rae_sub_stage == 'teaching':
        with st.spinner("Preparando el material de estudio..."):
            instructional_content = culture_guide.get_instructional_snippet(KNOWLEDGE_DOCUMENT_CONTENT, rae_info)
        response_text = f"{instructional_content}\n\nHe compartido contigo la información clave. Avísame cuando estés listo/a para la pregunta."
        st.session_state.rae_sub_stage = 'waiting_for_confirmation'
        return response_text

    if st.session_state.rae_sub_stage == 'waiting_for_confirmation':
        # --- Detección de intención para el paso a paso ---
        step_by_step_keywords = ["paso a paso", "proceso comercial", "guía completa", "explicación del proceso"]
        if any(keyword in user_prompt.lower() for keyword in step_by_step_keywords):
            return culture_guide.get_full_commercial_process()

        affirmative_responses = ['sí', 'si', 'listo', 'lista', 'dale', 'ok', 'vale', 'adelante', 'comencemos']
        if any(word in user_prompt.lower() for word in affirmative_responses):
            response_text = f"""¡Perfecto! Aquí va la pregunta:

> **{rae_info['description']}**"""
            st.session_state.rae_sub_stage = 'assessing'
        else:
            # Si no es una respuesta afirmativa, usar el documento de conocimiento para responder
            ai_response_to_question = culture_guide.answer_question_about_content(KNOWLEDGE_DOCUMENT_CONTENT, user_prompt)
            
            response_text = f"""{ai_response_to_question}

¿Hay algo más en el material que te gustaría que te aclare, {user_name}? O, ¿estás listo/a para la pregunta del RAE?"""
            # Mantener el sub-estado como 'waiting_for_confirmation' para permitir más preguntas o la confirmación.
        return response_text

    if st.session_state.rae_sub_stage == 'assessing':
        is_approved = assessment_bot.validate_rae_with_ai(current_rae_id, rae_info, user_response=user_prompt)
        feedback = assessment_bot.get_feedback(current_rae_id, rae_info, user_prompt, is_approved)
        response_text = feedback
        
        rae_scores = current_progress.get('rae_scores', {})
        rae_scores[current_rae_id]['status'] = 'aprobado' if is_approved else 'fallido'
        rae_scores[current_rae_id]['score'] = 100 if is_approved else 0
        updates = {'rae_scores': json.dumps(rae_scores)}

        if is_approved:
            next_rae_updates, next_rae_message = move_to_next_rae(current_progress, user_name)
            updates.update(next_rae_updates)
            response_text += next_rae_message
        else:
            st.session_state.rae_sub_stage = 'teaching'
            response_text += f"\n\nNo te preocupes, vamos a revisar el material de nuevo."

        tracker.update_user_progress(user_id, updates)
        st.session_state.progress = tracker.get_user_progress(user_id)
        return response_text
    
    return "Ha ocurrido un error en el flujo de la conversación."


# --- LÓGICA DE FLUJO DE ONBOARDING ---
if st.session_state.onboarding_stage == 'name_collection':
    st.title("¡Bienvenido/a a Mantis FICC!")
    st.write("Para comenzar tu proceso de onboarding, por favor, dinos tu nombre.")

    user_name_input = st.text_input("Mi nombre es:", key="user_name_input")
    if st.button("Comenzar Onboarding"):
        if user_name_input:
            st.session_state.user_name = user_name_input
            new_progress = tracker.create_new_user(st.session_state.user_id, st.session_state.user_name)
            st.session_state.progress = new_progress
            st.session_state.onboarding_stage = 'onboarding_active'
            st.session_state.rae_sub_stage = 'teaching'
            
            welcome_message = culture_guide.get_welcome_message(st.session_state.user_name)
            st.session_state.messages.append({"role": "assistant", "content": welcome_message})
            st.rerun()
        else:
            st.warning("Por favor, ingresa tu nombre para comenzar.")

elif st.session_state.onboarding_stage == 'onboarding_active':
    st.title("Onboarding Inteligente - Mantis FICC")

    with st.sidebar:
        st.header("Progreso del Usuario")
        st.write(f"Usuario actual: **{st.session_state.user_name}**")
        
        rae_scores = st.session_state.progress.get("rae_scores", {})
        if rae_scores:
            fig = create_competency_spider_chart(rae_scores, RAE_LIBRARY_DATA)
            st.subheader("Mapa de Competencias")
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Estado de RAEs")
        rae_status_list = get_rae_status_list(rae_scores)
        for item in rae_status_list:
            st.markdown(item)

    st.header("Asistente de Onboarding")

    if len(st.session_state.messages) == 1 and st.session_state.rae_sub_stage == 'teaching':
        teaching_message = process_user_input("", tracker, assessment_bot, culture_guide, org_navigator, process_master, get_drive_service())
        st.session_state.messages.append({"role": "assistant", "content": teaching_message})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Lógica para buscar recursos en Drive
    if st.session_state.rae_sub_stage == 'waiting_for_confirmation':
        rae_info = RAE_LIBRARY_DATA.get(st.session_state.progress['current_rae_id'])
        if rae_info:
            resource_name = "Plantilla_Gestion_Conocimiento.docx"
            if st.button(f"Buscar '{resource_name}' en Drive"):
                with st.spinner("Buscando en Google Drive..."):
                    drive_service = get_drive_service()
                    print(f"DEBUG: Buscando '{resource_name}' en Drive (Folder ID: {ONBOARDING_FOLDER_ID})")
                    st.session_state.found_files = drive_service.search_files(resource_name, folder_id=ONBOARDING_FOLDER_ID)
                    if not st.session_state.found_files:
                         st.info("No se encontraron archivos con ese nombre en la carpeta de onboarding.")
                    print(f"DEBUG: Archivos encontrados: {st.session_state.found_files}")
                    st.rerun()

    if st.session_state.found_files:
        st.markdown("--- \n**Recursos encontrados:**")
        for file_item in st.session_state.found_files:
            st.markdown(f"- [{file_item['name']}]({file_item['webViewLink']})")
        if st.button("Ocultar Recursos"):
            st.session_state.found_files = []
            st.rerun()

    if prompt := st.chat_input("Escribe tu respuesta aquí..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("El agente está pensando..."):
            assistant_response = process_user_input(prompt, tracker, assessment_bot, culture_guide, org_navigator, process_master, get_drive_service())
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            st.rerun()
