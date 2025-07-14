

import sqlite3
import json

# --- CONTENIDO DEL DOCUMENTO DE GESTIÓN DEL CONOCIMIENTO ---
KNOWLEDGE_DOCUMENT_CONTENT = """
Plantilla de Documentación de Proceso: Gestión del Conocimiento

1. Información general del proceso
- Nombre del proceso: Ejecutiva Comercial Pymes
- Código / ID del proceso: ACEP-003
- Versión: Vers.-001
- Fecha de creación / actualización: 8/07/2025
- Responsable del proceso: Silvia Fernanda Niño Dávila
- Área responsable: Comercial – Ventas.

2. Objetivo
Gestionar y convertir en oportunidades comerciales los contactos obtenidos a través de redes sociales y otros canales, mediante el análisis de sus necesidades, seguimiento efectivo, presentación del software Mantis FICC ERP y cierre de ventas, contribuyendo al crecimiento de la base de clientes PYMES de la empresa.

APORTES A LA ORGANIZACION
- Generación constante de nuevas oportunidades de negocio, aumentando la base de clientes.
- Contribución directa al crecimiento de los ingresos a través de procesos comerciales estructurados.
- Fortalecimiento de la relación con el cliente, promoviendo fidelización y reputación de marca.
- Alineación entre las necesidades del mercado Pyme y las soluciones ofrecidas por el ERP.
- Aporte estratégico mediante la retroalimentación del mercado a las áreas de producto y soporte.
- Representación estratégica del portafolio Mantis FICC ERP, generando confianza y credibilidad en el proceso de venta.
- Identificación y canalización de oportunidades de mejora del producto basadas en la experiencia del cliente.
- Apoyo directo en la expansión de la marca en mercados locales y regionales.

3. Alcance
Realizar análisis de las necesidades de los clientes y ofrecer soluciones personalizadas que se adapten a sus requerimientos.
Establecer y mantener relaciones con los clientes, asegurando su satisfacción y fidelidad.
Trabajar en estrecha colaboración con el equipo de desarrollo para entender las características y beneficios del software ERP y poder promocionarlo de manera efectiva.
Realizar seguimiento de las oportunidades de venta, analizar los resultados y presentar informes a la gerencia para ajustar la estrategia comercial.

1. Departamento de Marketing
- Alineación con campañas publicitarias y contenido digital.
- Informe mensual de resultados de Marketing.

2. Departamento Comercial
- Prospección, seguimiento y cierre de ventas.
- Negociación en precios, descuentos y metas comerciales.
- Generación de informes de ventas y análisis de resultados.

3. Gerencia Comercial - Ventas
- Contribuye con información estratégica para la toma de decisiones.
- Participa en reuniones de análisis de resultados y planificación.
- Representa la voz del cliente ante la alta dirección.

4. Departamento de Implementación / Soporte
- Coordinación para el inicio de proyectos con clientes nuevos.
- Transmisión clara de los compromisos comerciales y funcionalidades adquiridas.

5. Departamento de Desarrollo / Producto
- Comunicación de necesidades específicas del mercado Pyme.
- Reporte de funcionalidades solicitadas por los clientes.

4. Entradas del proceso
1. Fuentes de datos
- Base de datos de prospectos y clientes (GEVI y Excel).
- Base de datos empresas de Gestión Comercial (GEVI y Excel)
- Leads generados desde redes sociales o página web.
- Registros de interacción con clientes (WhatsApp, correo, llamadas).
- Estadísticas de campañas de marketing digital.

2. Personas involucradas
- Gerente Comercial o Gerente de Ventas.
- Equipo de Marketing.
- Equipo de Implementación y Soporte Técnico.
- Equipo de Desarrollo/Producto (para retroalimentación).
- Departamento administrativo (para coordinar contratos, facturación, Check List).
- Aliados comerciales o canales de distribución.

5. Actividades / Descripción del flujo
Paso | Descripción de la Actividad | Responsable | Herramientas / Sistema
--- | --- | --- | ---
1 | Recepción y calificación de leads: Recibe contactos desde redes sociales, WhatsApp, web, referidos u otros canales. | Marketing | WhatsApp Business, Email, Meta/Instagram, Página web, Google, Facebook, YouTube.
2 | Registro y segmentación del lead: Se ingresa la información del contacto en GEVI o base de datos, clasificándolo por sector, interés, canal de origen, etc. | Ejecutiva Comercial Pyme | GEVI, Excel
3 | Contacto inicial y diagnóstico: Llamada o mensaje para entender las necesidades del cliente, el tipo de empresa, procesos actuales y motivación de compra. | Ejecutiva Comercial Pyme | Teléfono, WhatsApp, GEVI
4 | Agendamiento de demostración (DEMO): Se coordina fecha y hora con el equipo técnico o el cliente para mostrar el software. | Ejecutiva Comercial Pyme | Calendario Google, WhatsApp, GEVI
5 | Seguimiento posterior a la DEMO: Se consulta percepción del cliente, dudas adicionales, y se valida el interés de continuar con propuesta. | Ejecutiva Comercial Pyme | Calendario Google, WhatsApp, GEVI
6 | Elaboración y envío de propuesta comercial: Cotización formal con alcance, módulos, precios, condiciones de pago, soporte y capacitación. | Ejecutiva Comercial Pyme | Plantilla de cotización, Word/PDF, GEVI
7 | Negociación y cierre: Se responden objeciones, se negocia precio o condiciones. Una vez aceptada la propuesta, se coordina la firma del contrato. | Ejecutiva Comercial Pyme | WhatsApp, Email, GEVI, Firma Contrato. transferencia
8 | Entrega y transición al equipo Administrativo y Contable: Se entrega la información del cliente al área de facturación y contable para la realización de la factura y el pago respectivo etc. | Ejecutiva Comercial Pyme | WhatsApp
9 | Entrega y transición al equipo de implementación: Se entrega la información del cliente al área técnica o de soporte para agendar la instalación y capacitación. | Ejecutiva Comercial Pyme | WhatsApp

6. Salidas del proceso
1. Documentos
- Cotizaciones (PDF).
- Propuestas comerciales personalizadas.
- Contrato de servicio de software.
- Brochures o catálogos de módulos.
- Presentaciones institucionales o comerciales (PowerPoint).
- Modelos de correo y mensajes WhatsApp.
- Plantillas de seguimiento a clientes (Excel y GEVI).
- Informe de gestión comercial mensual.
- Formato de levantamiento de toma de datos.

2. Herramientas o sistemas
- Software GEVI
- Plataformas de correo y WhatsApp Business.
- ERP Mantis FICC (para demostraciones en vivo).
- Plataformas de video llamada Meet.
- Herramientas de diseño o edición (Canva, PowerPoint, Prezzi).

7. Indicadores de desempeño (KPIs)
1. Ventas y Crecimiento
- Volumen de ventas: cantidad de software vendido durante un período determinado.
- Tasa de crecimiento de ventas: compara el crecimiento de las ventas en relación con períodos anteriores.
- Valor promedio del pedido: valor promedio de los pedidos realizados por los clientes.

2. Eficiencia y Productividad
- Tiempo de ciclo de ventas: tiempo que tarda en completarse un proceso de venta desde el inicio hasta el final.
- Tasa de conversión de ventas: compara la cantidad de ventas realizadas con la cantidad de oportunidades de venta identificadas.
- Número de nuevos clientes adquiridos: cantidad de nuevos clientes obtenidos durante un período determinado.

3. Satisfacción del Cliente y Retención
- Índice de satisfacción del cliente: mide la satisfacción de los clientes con los productos y servicios de la empresa.
- Tasa de retención de clientes: porcentaje de clientes que continúan utilizando los productos o servicios de la empresa.

4. Rentabilidad y Eficiencia Financiera
- Retorno de la inversión (ROI): compara los beneficios obtenidos con la inversión realizada en el sistema ERP.
- Costo por transacción: costo promedio de procesar una transacción, como un pedido de venta o una factura de proveedor.
"""

# --- CONEXIÓN A LA BASE DE DATOS ---
DB_NAME = 'onboarding_mantis.db'

def get_db_connection():
    """Crea y retorna una conexión a la base de datos."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# --- DATOS INICIALES ---
# Estos datos ahora pueden ser más simples, ya que el contenido principal está en el documento.
RAE_LIBRARY_DATA = {
    'RAE1': {
        'stage': 'cultura',
        'description': 'Explica en 3 frases por qué Mantis FICC existe, basándote en el objetivo y aportes del proceso comercial.',
        'validation_criteria': ['objetivo', 'aportes', 'crecimiento', 'pymes', 'democratizar'],
        'remediation_strategy': 'Revisa la sección 2 (Objetivo y Aportes a la Organización) del documento de Gestión del Conocimiento.'
    },
    'RAE2': {
        'stage': 'cultura',
        'description': 'Describe cómo tu rol se alinea con al menos dos "Aportes a la Organización" mencionados en el documento.',
        'validation_criteria': ['fortalecimiento', 'contribución', 'ingresos', 'relación con cliente'],
        'remediation_strategy': 'Analiza la sección de "Aportes a la Organización" y conecta tus tareas diarias con esos puntos.'
    },
    # ... (otros RAEs pueden ser definidos aquí)
}

ONBOARDING_PLAN_DATA = [
    {'stage': 'cultura', 'raes': ['RAE1', 'RAE2'], 'checkpoint': 80},
    # ... (otras etapas del plan)
]


# --- FUNCIONES DE LA BASE DE DATOS ---
def setup_database():
    """Crea las tablas necesarias si no existen."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tabla de progreso de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_progress (
            user_id TEXT PRIMARY KEY,
            user_name TEXT,
            current_stage TEXT,
            current_rae_id TEXT,
            rae_scores TEXT, -- JSON con el estado y puntaje de cada RAE
            completed BOOLEAN DEFAULT FALSE
        )
    ''')
    
    conn.commit()
    conn.close()

class ProgressTracker:
    """Clase para manejar el progreso del usuario en la base de datos."""
    
    def get_user_progress(self, user_id):
        """Obtiene el progreso de un usuario."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_progress WHERE user_id = ?", (user_id,))
        progress = cursor.fetchone()
        conn.close()
        if progress:
            # Deserializar rae_scores de JSON a un diccionario
            progress_dict = dict(progress)
            progress_dict['rae_scores'] = json.loads(progress_dict['rae_scores']) if progress_dict['rae_scores'] else {}
            return progress_dict
        return None

    def create_new_user(self, user_id, user_name):
        """Crea un nuevo registro de progreso para un usuario."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        initial_rae_scores = {rae_id: {'status': 'pendiente', 'score': 0} for rae_id in RAE_LIBRARY_DATA.keys()}
        initial_stage = ONBOARDING_PLAN_DATA[0]['stage']
        initial_rae_id = ONBOARDING_PLAN_DATA[0]['raes'][0]

        cursor.execute('''
            INSERT INTO user_progress (user_id, user_name, current_stage, current_rae_id, rae_scores, completed)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, user_name, initial_stage, initial_rae_id, json.dumps(initial_rae_scores), False))
        
        conn.commit()
        conn.close()
        return self.get_user_progress(user_id)

    def update_user_progress(self, user_id, updates):
        """Actualiza el progreso de un usuario con un diccionario de cambios."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Construir la consulta de actualización dinámicamente
        set_clause = ", ".join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values())
        values.append(user_id)
        
        query = f"UPDATE user_progress SET {set_clause} WHERE user_id = ?"
        cursor.execute(query, tuple(values))
        
        conn.commit()
        conn.close()

# --- Bloque de prueba ---
if __name__ == '__main__':
    print("Configurando la base de datos...")
    setup_database()
    print("Base de datos lista.")
    
    print("\nContenido del Documento de Conocimiento:")
    print(KNOWLEDGE_DOCUMENT_CONTENT[:500] + "...") # Imprimir un fragmento
    
    print("\nRAE Library Data:")
    print(json.dumps(RAE_LIBRARY_DATA, indent=2))
