
import os
import json
import google.generativeai as genai
import streamlit as st
from database import RAE_LIBRARY_DATA, ONBOARDING_PLAN_DATA

# --- CONFIGURACIÓN DE LA API DE GEMINI ---
try:
    genai.configure(api_key=st.secrets['GEMINI_API_KEY'])
    print("API de Gemini configurada correctamente.")
except Exception as e:
    print(f"Error: La clave API de Gemini no está configurada en st.secrets. {e}")
    # Salir o manejar el error como prefieras
    exit()

# --- MODELO BASE DEL AGENTE ---
class BaseAgent:
    """Clase base para todos los agentes de IA."""
    def __init__(self, model_name="gemini-1.5-flash"):
        self.model = genai.GenerativeModel(model_name)

    def generate_response(self, prompt):
        """Genera una respuesta usando el modelo de Gemini."""
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error al generar respuesta de Gemini: {e}")
            return "Lo siento, estoy teniendo problemas para procesar tu solicitud en este momento."

    def answer_question_about_content(self, content, question):
        """Responde a una pregunta del usuario basándose en un contenido dado."""
        prompt = f"""
        Eres un asistente de onboarding. Tu tarea es responder a la pregunta del usuario basándose **únicamente** en el contenido proporcionado.

        **Instrucciones:**
        1.  Analiza la "PREGUNTA DEL USUARIO" y el "CONTENIDO" a continuación.
        2.  Si la respuesta se encuentra explícitamente en el contenido, respóndela de manera clara y concisa.
        3.  Si la respuesta **no se encuentra** en el contenido, debes responder exactamente con la siguiente frase: "No puedo responder a esa pregunta con la información que tengo. Para temas no cubiertos en este material, te recomiendo consultarlo con tu superior directo, el Gerente Comercial."

        **CONTENIDO:**
        ---
        {content}
        ---

        **PREGUNTA DEL USUARIO:**
        {question}

        **RESPUESTA:**
        """
        return self.generate_response(prompt)

# --- AGENTES ESPECÍFICOS ---

class CultureGuide(BaseAgent):
    """Agente responsable de la inmersión cultural."""
    def get_prompt(self):
        return """
        Eres CultureGuide, el agente responsable de la inmersión cultural de Mantis FICC ERP.

        CONTEXTO EMPRESARIAL:
        - Empresa: Desarrolladora de software ERP para PYMES
        - Misión: Democratizar el acceso a herramientas de gestión empresarial
        - Valores: Innovación, cercanía al cliente, excelencia técnica
        - Cultura: Orientada a resultados, colaborativa, enfoque en crecimiento

        OBJETIVO DE APRENDIZAJE:
        El nuevo empleado debe internalizar la identidad corporativa y entender cómo su rol aporta a la misión empresarial.

        METODOLOGÍA:
        1. Presenta la historia de la empresa en 3 capítulos interactivos
        2. Explica valores mediante casos reales de decisiones empresariales
        3. Conecta el rol comercial con el impacto en clientes PYMES
        4. Valida comprensión mediante RAE específicos

        RECURSOS DISPONIBLES:
        - Manual de inducción corporativa
        - Videos institucionales
        - Casos de éxito de clientes

        INTERACCIÓN:
        Conversacional, empática, usa ejemplos reales. Haz UNA pregunta por vez.
        Si el empleado falla un RAE, proporciona retroalimentación específica y re-enseña el concepto.
        """

    def get_instructional_snippet(self, full_document_content, rae_info):
        """Extrae un fragmento relevante del documento de conocimiento para un RAE específico."""
        keywords = rae_info.get('document_section_keywords', [])
        if not keywords:
            return "No hay un contenido de enseñanza específico para este objetivo. Puedes hacerme preguntas sobre el material de onboarding si tienes dudas."

        prompt = f"""
        **TAREA DE EXTRACCIÓN DE CONTENIDO IA**

        **Contexto:** Eres un asistente de IA que prepara material de estudio para un nuevo empleado. Tu tarea es extraer la sección más relevante de un documento extenso para un objetivo de aprendizaje (RAE) específico.

        **Documento Completo:**
        ---
        {full_document_content}
        ---

        **Objetivo de Aprendizaje (RAE):**
        - **Descripción:** {rae_info['description']}
        - **Palabras Clave de la Sección:** {', '.join(keywords)}

        **Instrucción:**
        1.  Lee la descripción del RAE y las palabras clave.
        2.  Busca en el "Documento Completo" la sección o los párrafos que mejor expliquen los conceptos relacionados con el RAE.
        3.  Extrae y presenta **solo** ese fragmento de texto de manera limpia y concisa. No añadas introducciones ni conclusiones. Simplemente devuelve el texto relevante.
        
        **Ejemplo de Salida (si las palabras clave fueran "Indicadores de Desempeño", "KPIs"):**
        7. Indicadores de desempeño (KPIs)
        1. Ventas y Crecimiento
        ✓ Volumen de ventas: cantidad de software vendido durante un período determinado.
        ... (y el resto de esa sección)

        **Fragmento Extraído:**
        """
        return self.generate_response(prompt)

    def get_full_commercial_process(self):
        """Devuelve una explicación completa del proceso comercial basada en el documento PDF."""
        explanation = """
¡Excelente pregunta! Para ser un Asesor Comercial de alto impacto en Mantis FICC, es crucial dominar el proceso completo. Aquí te presento una guía ordenada basada en nuestra documentación interna:

### 1. Información General y Objetivo del Proceso
*   **Nombre del Proceso:** Ejecutiva Comercial Pymes.
*   **Responsable:** El área Comercial - Ventas.
*   **Objetivo Principal:** Gestionar y convertir oportunidades comerciales, desde el primer contacto hasta el cierre, para contribuir al crecimiento de nuestra base de clientes PYMES.

### 2. Aportes a la Organización y Alcance
Tu rol es vital. No solo generas ingresos, sino que también:
*   **Fortaleces la marca** y la relación con el cliente.
*   **Aportas retroalimentación estratégica** a las áreas de producto y soporte.
*   **Colaboras estrechamente** con Marketing, Desarrollo, Implementación y Gerencia para asegurar una estrategia coherente.

### 3. Entradas del Proceso (Lo que necesitas para empezar)
*   **Fuentes de Datos:** Leads de redes sociales, nuestra web, WhatsApp, y bases de datos de prospectos en GEVI y Excel.
*   **Personas Involucradas:** Trabajarás con Gerentes, Marketing, Soporte, Desarrollo y el área administrativa.

### 4. Actividades / Descripción del Flujo (Tu día a día)
Este es el corazón de tu trabajo, dividido en 9 pasos clave:
1.  **Recepción y Calificación de Leads:** Recibir y analizar los contactos iniciales.
2.  **Registro y Segmentación:** Ingresar y clasificar los leads en GEVI/Excel.
3.  **Contacto Inicial y Diagnóstico:** Llamar o enviar un mensaje para entender las necesidades del cliente.
4.  **Agendamiento de la DEMO:** Coordinar una demostración del software.
5.  **Seguimiento Post-DEMO:** Validar el interés y resolver dudas.
6.  **Elaboración de Propuesta Comercial:** Crear y enviar una cotización formal.
7.  **Negociación y Cierre:** Manejar objeciones y firmar el contrato.
8.  **Transición a Administración:** Entregar la información para la facturación.
9.  **Transición a Implementación:** Entregar la información al equipo técnico para la instalación.

### 5. Salidas del Proceso (Lo que produces)
*   **Documentos:** Cotizaciones, propuestas personalizadas, contratos.
*   **Sistemas:** Mantener actualizado el software GEVI y las plataformas de comunicación.

### 6. Indicadores de Desempeño (Cómo medimos el éxito)
*   **Ventas y Crecimiento:** Volumen de ventas, tasa de crecimiento.
*   **Eficiencia y Productividad:** Tiempo del ciclo de ventas, tasa de conversión.
*   **Satisfacción del Cliente:** Índice de satisfacción y tasa de retención.
*   **Rentabilidad:** Retorno de la inversión (ROI) y costo por transacción.

Dominar este proceso de principio a fin es tu camino al éxito.

¿Hay algo más que te gustaría aclarar sobre este proceso? O, si prefieres, podemos continuar con la pregunta del RAE.
"""
        return explanation

    def get_welcome_message(self, user_name):
        """Genera un mensaje de bienvenida detallado y contextual para el usuario."""
        company_name = "Mantis FICC"
        
        # Extraer la información del primer RAE
        first_rae_id = ONBOARDING_PLAN_DATA[0]['raes'][0]
        first_rae_info = RAE_LIBRARY_DATA[first_rae_id]
        rae1_name = "Identidad Corporativa" # Asignamos un nombre más descriptivo
        rae1_description = first_rae_info['description']
        rae1_resource = first_rae_info['remediation_strategy']

        # Construir el mensaje de bienvenida
        welcome_message = (
            f"¡Hola, {user_name}! Soy **CultureGuide**, tu asistente personal para el proceso de inducción en **{company_name}**.\n\n"
            f"Mi propósito es darte la bienvenida y guiarte paso a paso para que te integres de la mejor manera a nuestra cultura y equipo. "
            f"Este proceso de onboarding está diseñado para darte claridad sobre tu rol y cómo contribuyes a nuestra misión.\n\n"
            f"**¿Cómo funciona?**\n"
            f"El onboarding se divide en varias etapas, cada una con **Resultados de Aprendizaje Esperados (RAE)**. Un RAE es un objetivo concreto que debes demostrar que has aprendido. "
            f"Yo te presentaré cada RAE, te daré los recursos necesarios y evaluaré tus respuestas para asegurar que tienes todo el conocimiento para triunfar.\n\n"
            f"La **meta final** es que al terminar, tengas una comprensión profunda de nuestra cultura, tu rol, nuestros procesos y cómo todo se conecta para alcanzar el éxito.\n\n"
            f"--- \n\n"
            f"**Comencemos con el primer paso.**\n\n"
            f"Nuestra primera etapa es la de **Cultura**. Aquí nos enfocaremos en que respires y vivas la identidad de Mantis FICC.\n\n"
            f"Tu primer objetivo se llama **'{rae1_name}' ({first_rae_id})**. En este RAE, se evaluará tu comprensión sobre nuestra razón de ser.\n\n"
            f"**El objetivo es el siguiente:**\n> {rae1_description}\n\n"
            f"Para prepararte, te recomiendo que explores el siguiente recurso. ¡Es fundamental para que superes este RAE con éxito!\n"
            f"> **Recurso recomendado:** {rae1_resource}\n\n"
            f"Tómate tu tiempo para revisar el material y, cuando te sientas listo/a, responde a la pregunta del RAE. ¡Estoy aquí para ayudarte!"
        )
        return welcome_message

class OrgNavigator(BaseAgent):
    """Agente especialista en la estructura organizacional."""
    def get_prompt(self):
        return """
        Eres OrgNavigator, especialista en ubicación organizacional y relaciones empresariales.

        ESTRUCTURA ORGANIZACIONAL MANTIS FICC:
        - Gerencia General
        ├── Gerencia Comercial (SUPERIOR DIRECTO)
        ├── Gerencia Técnica
        ├── Gerencia Administrativa
        └── Gerencia de Producto

        ECOSISTEMA DEL ROL "EJECUTIVA COMERCIAL PYMES":
        - SUPERIOR: Gerente Comercial/Ventas
        - PARES: Otros Ejecutivos Comerciales, Equipo Marketing
        - ALIADOS CLAVE: Implementación, Soporte Técnico, Desarrollo
        - STAKEHOLDERS: Administrativo (contratos), Contabilidad (facturación)

        OBJETIVO DE APRENDIZAJE:
        Construir el mapa relacional completo y entender flujos de comunicación efectivos.

        METODOLOGÍA:
        1. Mapeo visual interactivo del organigrama
        2. Simulación de escenarios de escalamiento
        3. Role-play de coordinación interdepartamental
        """

class ProcessMaster(BaseAgent):
    """Agente maestro de los procesos comerciales."""
    def get_prompt(self):
        return """
        Eres ProcessMaster, maestro de los procesos comerciales de Mantis FICC ERP.

        PROCESOS CORE A DOMINAR:
        1. Calificación y registro de leads (GEVI + Excel)
        2. Contacto inicial y diagnóstico de necesidades
        3. Agendamiento y seguimiento de demos
        4. Elaboración de propuestas comerciales
        5. Negociación y cierre
        6. Transición a implementación

        HERRAMIENTAS A DOMINAR:
        - GEVI (CRM principal)
        - Excel (base de datos complementaria)
        - WhatsApp Business
        - Google Calendar
        - Plantillas de cotización
        - Mantis FICC ERP (para demos)
        """

class AssessmentBot(BaseAgent):
    """Agente responsable de la evaluación y análisis de brechas."""
    def get_prompt(self):
        return """
        Eres AssessmentBot, responsable de evaluación continua y análisis de brechas de conocimiento.

        FRAMEWORK DE EVALUACIÓN:
        - Evaluación formativa: Durante cada interacción
        - Evaluación sumativa: Al final de cada etapa
        - Evaluación integral: Simulacro completo día 5

        SISTEMA DE SCORING:
        - Verde (85-100%): Avanza automáticamente
        - Amarillo (70-84%): Refuerzo específico + re-evaluación
        - Rojo (<70%): Repetir módulo completo
        """

    def validate_rae_with_ai(self, rae_id, rae_info, user_response=None, file_content=None):
        """Usa Gemini para validar la respuesta de un usuario (texto o archivo) contra un RAE."""
        content_to_evaluate = user_response if user_response else file_content
        if not content_to_evaluate:
            return False # No content to evaluate

        validation_prompt = f"""
        **TAREA DE EVALUACIÓN DE IA - ALTA PRECISIÓN**

        **Contexto:** Eres un evaluador de IA extremadamente riguroso. Tu tarea es validar la respuesta de un nuevo empleado contra un objetivo de aprendizaje (RAE), siguiendo reglas estrictas.

        **RAE a Evaluar:** {rae_id}
        **Descripción del RAE:** "{rae_info['description']}"
        
        **Criterios de Validación Estrictos:**
        - **OBLIGATORIO (Debe Contener):** {json.dumps(rae_info['validation_criteria'].get('must_have', []))}
        - **DESEABLE (Debería Contener):** {json.dumps(rae_info['validation_criteria'].get('should_have', []))}

        **Respuesta del Empleado:**
        ---
        {content_to_evaluate}
        ---

        **Instrucciones de Evaluación:**
        1.  **Verificación Obligatoria:** Primero, comprueba si la respuesta del empleado contiene **TODAS** las palabras o conceptos del criterio "OBLIGATORIO". Si falta **incluso uno solo** de estos elementos, la respuesta es un **FALLIDO** inmediato, sin importar qué más contenga.
        2.  **Verificación Deseable:** Si y solo si se cumplen todos los criterios obligatorios, procede a verificar cuántos de los conceptos "DESEABLES" están presentes.
        3.  **Decisión Final:**
            - Si no se cumplen todos los criterios OBLIGATORIOS, responde **FALLIDO**.
            - Si se cumplen todos los criterios OBLIGATORIOS y al menos la mitad de los DESEABLES, responde **APROBADO**.
            - Si se cumplen los OBLIGATORIOS pero no los DESEABLES suficientes, responde **FALLIDO**.

        Responde con una única palabra: **APROBADO** o **FALLIDO**.
        """
        
        result = self.generate_response(validation_prompt).upper()
        return "APROBADO" in result

    def get_feedback(self, rae_id, rae_info, user_response, is_approved):
        """Genera retroalimentación específica para el usuario."""
        status = "exitosa" if is_approved else "incorrecta"
        
        feedback_prompt = f"""
        **TAREA DE GENERACIÓN DE FEEDBACK DE IA**

        **Contexto:** Eres un coach de onboarding empático y efectivo. Un empleado acaba de dar una respuesta a un objetivo de aprendizaje (RAE).

        **RAE Evaluado:** {rae_id} - "{rae_info['description']}"
        **Respuesta del Empleado:** "{user_response}"
        **Resultado de la Evaluación:** La respuesta fue {status}.

        **Instrucción:**
        Basado en el resultado, genera un mensaje de retroalimentación para el empleado. 
        - Si la respuesta fue **exitosa**, felicítalo brevemente y refuerza por qué su respuesta fue buena.
        - Si la respuesta fue **incorrecta**, sé constructivo. No le des la respuesta directamente. En su lugar, dale una pista sutil y sugiérele que lo intente de nuevo, mencionando la estrategia de remediación: "{rae_info['remediation_strategy']}".
        
        **Tono:** Empático, motivador y profesional.
        
        **Ejemplo de Feedback (Incorrecto):**
        "Hmm, esa no es exactamente la respuesta que buscábamos. Recuerda que nuestra misión se centra en el impacto que tenemos en las PYMES. Intenta revisar el Módulo 1 del Manual de Inducción y enfócate en el 'porqué' de nuestra existencia. ¡Vamos, tú puedes!"

        **Mensaje de Retroalimentación:**
        """
        return self.generate_response(feedback_prompt)

# --- BLOQUE DE PRUEBA ---
if __name__ == '__main__':
    print("Ejecutando pruebas para el módulo de agentes...")
    
    # Cargar RAEs desde la base de datos para la prueba
    from database import ProgressTracker, RAE_LIBRARY_DATA
    
    # Instanciar el bot de evaluación
    assessment_bot = AssessmentBot()

    # --- Escenario de Prueba 1: Respuesta Correcta ---
    print("\n--- ESCENARIO 1: RESPUESTA CORRECTA ---")
    rae_id_1 = 'RAE1'
    rae_info_1 = RAE_LIBRARY_DATA[rae_id_1]
    user_response_1 = "Mantis FICC existe para democratizar la gestión empresarial, entregando herramientas poderosas a las pymes para que puedan crecer."
    
    print(f"Usuario responde a {rae_id_1}: \"{user_response_1}\"")
    
    is_approved_1 = assessment_bot.validate_rae_with_ai(rae_id_1, rae_info_1, user_response_1)
    print(f"Resultado de la validación IA: {'APROBADO' if is_approved_1 else 'FALLIDO'}")
    
    feedback_1 = assessment_bot.get_feedback(rae_id_1, rae_info_1, user_response_1, is_approved_1)
    print(f"Feedback generado:\n---\n{feedback_1}\n---")

    # --- Escenario de Prueba 2: Respuesta Incorrecta ---
    print("\n--- ESCENARIO 2: RESPUESTA INCORRECTA ---")
    rae_id_2 = 'RAE4'
    rae_info_2 = RAE_LIBRARY_DATA[rae_id_2]
    user_response_2 = "Si un cliente tiene un problema técnico, le digo que reinicie la computadora."
    
    print(f"Usuario responde a {rae_id_2}: \"{user_response_2}\"")
    
    is_approved_2 = assessment_bot.validate_rae_with_ai(rae_id_2, rae_info_2, user_response_2)
    print(f"Resultado de la validación IA: {'APROBADO' if is_approved_2 else 'FALLIDO'}")
    
    feedback_2 = assessment_bot.get_feedback(rae_id_2, rae_info_2, user_response_2, is_approved_2)
    print(f"Feedback generado:\n---\n{feedback_2}\n---")
