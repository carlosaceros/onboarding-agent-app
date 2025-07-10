import sqlite3
import json

DB_NAME = "users_progress.db"

RAE_LIBRARY_DATA = {
    'RAE1': {
        'stage': 'cultura',
        'instructional_content': (
            "**Nuestra Misión y Propósito (RAE1):**\n\n"
            "El objetivo principal de tu rol es **gestionar y convertir en oportunidades comerciales los contactos que generamos**, contribuyendo directamente al crecimiento de nuestra base de clientes PYMES. No solo vendemos un producto; ofrecemos una solución que transforma negocios.\n\n"
            "**Aportas valor de múltiples maneras:**\n"
            "- **Generas nuevas oportunidades:** Eres la primera línea para expandir nuestra cartera de clientes.\n"
            "- **Fortaleces la marca:** Una buena gestión comercial crea clientes leales y mejora nuestra reputación.\n"
            "- **Eres la voz del mercado:** La retroalimentación que recoges de los clientes es crucial para que las áreas de producto y soporte mejoren nuestro ERP."
        ),
        'description': 'Explica con tus propias palabras, como si se lo contaras a un colega, cuál es el propósito principal de tu rol y de qué manera aportas valor a la organización.',
        'validation_criteria': {'keywords': ['oportunidades', 'crecimiento', 'pymes', 'clientes', 'reputación', 'retroalimentación']},
        'remediation_strategy': 'Revisar la sección 2 (Objetivo y Aportes a la Organización) del documento de Gestión del Conocimiento.'
    },
    'RAE2': {
        'stage': 'cultura',
        'instructional_content': (
            "**Nuestros Valores en Acción (RAE2):**\n\n"
            "Más allá de los procesos, nos guiamos por valores que se reflejan en nuestro trabajo diario. Dos de los más importantes son:\n\n"
            "1. **Cercanía al Cliente:** No se trata solo de vender, sino de **establecer y mantener relaciones sólidas**, asegurando la satisfacción y fidelidad de quienes confían en nosotros. Esto implica escuchar activamente sus necesidades para ofrecer soluciones que realmente les sirvan.\n\n"
            "2. **Excelencia y Colaboración Técnica:** Tu rol es un puente. Trabajas en **estrecha colaboración con el equipo de desarrollo y producto** para entender a fondo el software. Esta sinergia te permite promocionar el ERP de manera efectiva y comunicar al equipo técnico las necesidades que detectas en el mercado."
        ),
        'description': 'Basado en los valores de "Cercanía al Cliente" y "Colaboración Técnica", describe una situación práctica donde aplicarías ambos.',
        'validation_criteria': {'keywords': ['relaciones', 'satisfacción', 'fidelidad', 'colaboración', 'desarrollo', 'necesidades']},
        'remediation_strategy': 'Analizar la sección 3 (Alcance) del documento, enfocándote en la interacción con clientes y otros departamentos.'
    },
    'RAE3': {
        'stage': 'cultura',
        'instructional_content': (
            "**Tu Impacto Directo en la Misión (RAE3):**\n\n"
            "Nuestra misión es **democratizar el acceso a herramientas de gestión para las PYMES**. Tu rol es la pieza clave para que esto suceda.\n\n"
            "Cada vez que conviertes un lead en un cliente, estás:\n"
            "- **Aumentando directamente los ingresos** de la compañía a través de un proceso estructurado.\n"
            "- **Alineando las soluciones del ERP con las necesidades reales** del mercado Pyme.\n\n"
            "- **Representando estratégicamente nuestro portafolio**, lo que genera la confianza necesaria para que un cliente nos elija."
        ),
        'description': 'Explica la conexión entre cerrar una venta y el cumplimiento de la misión general de la empresa. ¿Cómo una acción lleva a la otra?',
        'validation_criteria': {'keywords': ['ingresos', 'alineando', 'soluciones', 'representando', 'confianza']},
        'remediation_strategy': 'Revisar la sección "Aportes a la Organización" en el documento de conocimiento.'
    },
    'RAE4': {
        'stage': 'organizacion',
        'instructional_content': (
            "**Navegando la Organización: Escalando un Problema Técnico (RAE4):**\n\n"
            "En tu día a día, te encontrarás con diversas situaciones. Es vital saber a quién acudir. Si un cliente o prospecto presenta una **objeción o duda técnica compleja** que no puedes resolver, el flujo correcto es el siguiente:\n\n"
            "1. **No intentes adivinar:** Proporcionar información incorrecta puede dañar la confianza.\n"
            "2. **Canaliza al experto:** Debes escalar la consulta al **Departamento de Desarrollo / Producto**. Ellos tienen el conocimiento profundo para dar una respuesta precisa.\n"
            "3. **Documenta:** Registra la consulta y la respuesta en GEVI. Esto nos ayuda a construir una base de conocimiento."
        ),
        'description': 'Imagina que un cliente te pregunta si nuestro ERP se puede integrar con un sistema de contabilidad muy específico que no conoces. ¿Cuáles serían tus pasos a seguir?',
        'validation_criteria': {'keywords': ['desarrollo', 'producto', 'técnico', 'soporte', 'escalar', 'preguntar', 'consultar']},
        'remediation_strategy': 'Estudiar las interacciones con departamentos en la sección 3 (Alcance) y 4 (Entradas) del documento.'
    },
    'RAE5': {
        'stage': 'organizacion',
        'instructional_content': (
            "**Flujo de Entrega de un Nuevo Cliente (RAE5):**\n\n"
            "¡Felicidades, has cerrado una venta! Ahora empieza un proceso crucial: la transición del nuevo cliente al resto de la organización. El flujo es el siguiente:\n\n"
            "1. **Transición a Administración y Contabilidad (Paso 8):** Inmediatamente después del cierre, debes entregar toda la información del cliente (contrato, propuesta aceptada) al área de **facturación y contable** para que generen la factura y gestionen el pago.\n\n"
            "2. **Transición a Implementación (Paso 9):** Una vez gestionado lo administrativo, entregas la información al área **técnica o de soporte** para que agenden la instalación, configuración y capacitación del cliente."
        ),
        'description': '¿Por qué es importante que el equipo de Administración reciba la información del nuevo cliente antes que el equipo de Implementación? Explica el razonamiento detrás de este orden.',
        'validation_criteria': {'keywords': ['administrativo', 'contable', 'factura', 'pago', 'primero', 'antes', 'implementación']},
        'remediation_strategy': 'Revisar los pasos 8 y 9 de la sección 5 (Actividades / Descripción del flujo) del documento.'
    },
    'RAE6': {
        'stage': 'organizacion',
        'instructional_content': (
            "**Tus Aliados Clave para el Éxito (RAE6):**\n\n"
            "Tu éxito no depende solo de tu esfuerzo individual. Hay varios departamentos cuyo trabajo impacta directamente en tus resultados. Tres de los más importantes son:\n\n"
            "1. **Marketing:** Genera los leads que nutren tu embudo de ventas. Una buena alineación con sus campañas es fundamental.\n"
            "2. **Implementación / Soporte:** La calidad de su trabajo asegura la satisfacción y retención del cliente que trajiste. Una mala implementación puede arruinar una buena venta.\n\n"
            "3. **Desarrollo / Producto:** Mejoran y adaptan el software según las necesidades del mercado que tú reportas. Un buen producto es más fácil de vender."
        ),
        'description': 'Elige uno de los departamentos mencionados (Marketing, Implementación o Desarrollo) y explica con un ejemplo cómo una falla en su trabajo podría afectar directamente tu capacidad para cerrar una venta.',
        'validation_criteria': {'keywords': ['marketing', 'implementación', 'soporte', 'desarrollo', 'producto', 'afectar', 'problema', 'falla']},
        'remediation_strategy': 'Analizar las secciones 3 (Alcance) y 4 (Personas involucradas) del documento de conocimiento.'
    },
    'RAE7': {
        'stage': 'procesos',
        'instructional_content': (
            "**El Inicio del Proceso: Recepción y Registro de Leads (RAE7):**\n\n"
            "Todo comienza con un contacto. Los leads pueden llegar desde múltiples canales: **redes sociales, WhatsApp, página web, referidos, etc.** (Paso 1).\n\n"
            "Una vez recibido, tu primera tarea es **registrar y segmentar** ese lead (Paso 2). Esto significa:\n"
            "- Ingresar toda la información de contacto en **GEVI** o la base de datos de Excel.\n"
            "- Clasificar el lead por criterios clave como **sector, interés manifestado, canal de origen, tamaño de la empresa, etc.** Una buena clasificación nos permite personalizar la comunicación."
        ),
        'description': '¿Por qué es importante clasificar un lead por "canal de origen"? ¿Qué tipo de información útil te da ese dato para el proceso de venta?',
        'validation_criteria': {'keywords': ['registrar', 'segmentar', 'clasificar', 'gevi', 'excel', 'canales', 'origen', 'información']},
        'remediation_strategy': 'Revisar los pasos 1 y 2 de la sección 5 (Actividades / Descripción del flujo).'
    },
    'RAE8': {
        'stage': 'procesos',
        'instructional_content': (
            "**El Diagnóstico: Identificando Información Crítica (RAE8):**\n\n"
            "Una vez registrado el lead, realizas el **contacto inicial y diagnóstico** (Paso 3). El objetivo de esta llamada o mensaje no es vender, sino **entender**.\n\n"
            "La información crítica que debes obtener es:\n"
            "- **Necesidades del cliente:** ¿Qué problema específico quieren resolver?\n"
            "- **Tipo de empresa:** ¿A qué se dedican, cuántos empleados tienen?\n"
            "- **Procesos actuales:** ¿Cómo manejan su facturación, inventario, etc., en este momento? ¿Usan otro software, Excel, papel?\n"
            "- **Motivación de compra:** ¿Por qué están buscando una solución ahora?"
        ),
        'description': 'De la información a obtener en el primer contacto, ¿cuál crees que es la más importante para poder personalizar la futura demo del software? Justifica tu respuesta.',
        'validation_criteria': {'keywords': ['necesidades', 'procesos actuales', 'motivación', 'tipo de empresa', 'diagnóstico', 'personalizar']},
        'remediation_strategy': 'Estudiar el paso 3 de la sección 5 (Actividades / Descripción del flujo).'
    },
    'RAE9': {
        'stage': 'procesos',
        'instructional_content': (
            "**La Entrevista de Descubrimiento (RAE9):**\n\n"
            "La fase de **'Contacto inicial y diagnóstico' (Paso 3)** es, en esencia, una entrevista de descubrimiento. Es una conversación estructurada para descubrir si podemos ayudar al cliente.\n\n"
            "**Tus herramientas principales aquí son:**\n"
            "- **Teléfono y WhatsApp:** Para una comunicación directa y ágil.\n"
            "- **GEVI:** Para registrar cada interacción y los datos que vas descubriendo.\n\n"
            "El éxito de todo el proceso de venta depende de la calidad de este diagnóstico. Un buen descubrimiento te permite personalizar la demo y la propuesta comercial más adelante."
        ),
        'description': 'Explica con tus palabras por qué un buen diagnóstico inicial es la base para el éxito de toda la venta.',
        'validation_criteria': {'keywords': ['diagnóstico', 'descubrimiento', 'entender', 'necesidades', 'gevi', 'base', 'éxito']},
        'remediation_strategy': 'Analizar el paso 3 de la sección 5 (Actividades / Descripción del flujo).'
    },
    'RAE10': {
        'stage': 'procesos',
        'instructional_content': (
            "**Identificando los 'Pain Points' (RAE10):**\n\n"
            "Un 'pain point' o 'punto de dolor' es un problema específico y recurrente que afecta el negocio de un cliente. Tu objetivo en el diagnóstico (Paso 3) es identificar al menos 3 de estos.\n\n"
            "**Ejemplos de 'pain points' que nuestro ERP puede resolver:**\n"
            "- 'Perdemos mucho tiempo haciendo facturas a mano.'\n"
            "- 'No sabemos cuánto inventario tenemos en tiempo real.'\n"
            "- 'La información de nuestros clientes está desorganizada en varios archivos de Excel.'\n\n"
            "Identificar estos dolores te permite enfocar tu propuesta en la **solución** y no solo en las características del software."
        ),
        'description': 'Imagina un cliente que usa Excel para todo. Basado en los ejemplos, ¿qué posible "pain point" o problema crees que tiene y cómo se lo presentarías?',
        'validation_criteria': {'keywords': ['dolor', 'problema', 'necesidad', 'solución', 'diagnóstico', 'excel', 'tiempo', 'desorganizado']},
        'remediation_strategy': 'Reflexionar sobre el objetivo del paso 3 de la sección 5 (Actividades / Descripción del flujo).'
    },
    'RAE11': {
        'stage': 'procesos',
        'instructional_content': (
            "**Agendamiento Estratégico de la DEMO (RAE11):**\n\n"
            "Una vez que has diagnosticado las necesidades del cliente, el siguiente paso es el **agendamiento de la demostración (DEMO)** (Paso 4).\n\n"
            "**Aspectos clave para un agendamiento exitoso:**\n"
            "- **Coordinación:** Debes coordinar la fecha y hora no solo con el cliente, sino también con el **equipo técnico o de soporte** que podría apoyarte en la demo.\n"
            "- **Stakeholders:** Es crucial que en la demo estén presentes las personas que toman las decisiones (dueño, gerente) y quienes usarán el software (contador, jefe de bodega). Si falta alguien clave, la venta se puede estancar.\n"
            "- **Herramientas:** Utiliza **Google Calendar** para enviar la invitación formal y **WhatsApp/GEVI** para confirmar la asistencia."
        ),
        'description': 'Estás agendando una demo y el gerente te dice que él no puede asistir, pero que enviará al contador. ¿Qué riesgo identificas en esta situación y cómo lo manejarías?',
        'validation_criteria': {'keywords': ['coordinar', 'stakeholders', 'decisores', 'gerente', 'riesgo', 'manejar']},
        'remediation_strategy': 'Revisar el paso 4 de la sección 5 (Actividades / Descripción del flujo).'
    },
    'RAE12': {
        'stage': 'procesos',
        'instructional_content': (
            "**Manejo de Objeciones Post-DEMO (RAE12):**\n\n"
            "Después de la demostración, es normal que los clientes tengan dudas u objeciones. Tu manejo de esta etapa es crítico.\n\n"
            "1. **Seguimiento (Paso 5):** Realiza un seguimiento proactivo para consultar la percepción del cliente y resolver dudas iniciales.\n"
            "2. **Negociación (Paso 7):** Aquí es donde se manejan las objeciones más fuertes, usualmente sobre **precio o condiciones**. Debes estar preparado/a para defender el valor de la solución, negociar dentro de los márgenes permitidos y responder a cualquier inquietud final.\n\n"
            "Una objeción no es un 'no', es una solicitud de más información. Tu trabajo es proporcionar esa información y reafirmar la confianza."
        ),
        'description': 'Un cliente te dice: "Me gustó, pero es muy caro". ¿Cómo aplicarías el principio de "una objeción es una solicitud de más información" en tu respuesta?',
        'validation_criteria': {'keywords': ['seguimiento', 'negociación', 'objeciones', 'precio', 'caro', 'información', 'valor']},
        'remediation_strategy': 'Estudiar los pasos 5 and 7 de la sección 5 (Actividades / Descripción del flujo).'
    },
    'RAE13': {
        'stage': 'procesos',
        'instructional_content': (
            "**Elaboración de la Propuesta Comercial (RAE13):**\n\n"
            "Si el interés continúa después de la demo, es hora de formalizar la oferta mediante una **propuesta comercial** (Paso 6).\n\n"
            "**Componentes de una propuesta técnicamente correcta:**\n"
            "- **Alcance claro:** Especifica qué módulos del ERP se incluyen.\n"
            "- **Precios detallados:** Costo de licencia, implementación, soporte, etc.\n"
            "- **Condiciones de pago:** Plazos y métodos de pago.\n"
            "- **Soporte y capacitación:** Define qué incluye el servicio post-venta.\n\n"
            "Utiliza la **plantilla de cotización oficial** y asegúrate de que toda la información sea precisa. Un error aquí puede generar desconfianza o problemas futuros."
        ),
        'description': 'Además de los precios, ¿qué otro elemento de la propuesta crees que es CRÍTICO para evitar malentendidos con el cliente en el futuro? Justifica tu elección.',
        'validation_criteria': {'keywords': ['alcance', 'módulos', 'condiciones', 'soporte', 'malentendidos', 'crítico']},
        'remediation_strategy': 'Revisar el paso 6 de la sección 5 y la sección 6 (Salidas del proceso) del documento.'
    },
    'RAE14': {
        'stage': 'procesos',
        'instructional_content': (
            "**Personalización de la Propuesta (RAE14):**\n\n"
            "Una propuesta ganadora no es solo una lista de precios. Debe ser un reflejo del diagnóstico que hiciste al principio.\n\n"
            "**Personalizar la propuesta significa:**\n"
            "- **Conectar características con soluciones:** En lugar de solo decir 'Módulo de Facturación', explica cómo este módulo resolverá su problema de 'perder tiempo haciendo facturas a mano'.\n"
            "- **Usar el lenguaje del cliente:** Refleja los 'pain points' que ellos mismos te mencionaron.\n"
            "- **Enfocar en el ROI:** Destaca cómo la inversión en el ERP se traducirá en ahorros o ganancias para su negocio.\n\n"
            "La personalización demuestra que escuchaste y entendiste sus necesidades, diferenciándote de la competencia."
        ),
        'description': 'Resume en una frase el objetivo principal de "personalizar una propuesta". ¿Qué buscas lograr en la mente del cliente?',
        'validation_criteria': {'keywords': ['personalizar', 'diagnóstico', 'soluciones', 'pain points', 'necesidades', 'entender', 'escuchar']},
        'remediation_strategy': 'Reflexionar sobre cómo conectar el paso 3 (Diagnóstico) con el paso 6 (Propuesta).'
    },
    'RAE15': {
        'stage': 'procesos',
        'instructional_content': (
            "**La Fase de Negociación y Cierre (RAE15):**\n\n"
            "Esta es la etapa final para convertir la oportunidad en una venta (Paso 7). La negociación puede involucrar precio, condiciones de pago, o alcance del proyecto.\n\n"
            "**Principios clave para negociar manteniendo la rentabilidad:**\n"
            "- **Conoce tus límites:** Debes saber hasta dónde puedes ofrecer un descuento sin afectar la rentabilidad del proyecto. Esto se coordina con Gerencia Comercial.\n"
            "- **Negocia sobre valor, no sobre precio:** Antes de ceder en el precio, refuerza todo el valor que el cliente obtiene (eficiencia, ahorro de tiempo, mejor toma de decisiones).\n"
            "- **Busca un ganar-ganar:** Una buena negociación deja a ambas partes sintiendo que han hecho un buen trato.\n\n"
            "Una vez que la propuesta es aceptada, el cierre se formaliza con la **firma del contrato**."
        ),
        'description': 'Explica la diferencia entre "negociar sobre valor" y "negociar sobre precio". ¿Por qué es más efectivo lo primero?',
        'validation_criteria': {'keywords': ['negociar', 'cierre', 'rentabilidad', 'valor', 'precio', 'diferencia', 'efectivo']},
        'remediation_strategy': 'Estudiar el paso 7 de la sección 5 (Actividades / Descripción del flujo).'
    },
    'RAE16': {
        'stage': 'procesos',
        'instructional_content': (
            "**Identificando Señales de Compra (RAE16):**\n\n"
            "Durante la negociación y el seguimiento, los clientes emiten 'señales de compra' que indican que están listos para cerrar el trato. Identificarlas te permite saber cuándo presionar para el cierre.\n\n"
            "**Ejemplos de señales de compra:**\n"
            "- **Preguntas sobre el futuro:** '¿Cuánto tiempo tomaría la implementación?' o '¿Quién sería nuestro contacto de soporte?'\n"
            "- **Negociación de detalles menores:** Si discuten sobre una cláusula específica del contrato en lugar del precio general, es una buena señal.\n"
            "- **Lenguaje posesivo:** Cuando empiezan a hablar del software como 'nuestro sistema' o 'cuando tengamos el ERP'.\n\n"
            "Al detectar estas señales, puedes hacer una pregunta de cierre como: 'Entonces, ¿procedemos con la firma del contrato esta semana?'"
        ),
        'description': 'Además de los ejemplos dados, piensa en otra posible "señal de compra" que un cliente podría dar. ¿Qué te indicaría que está listo para firmar?',
        'validation_criteria': {'keywords': ['señales', 'compra', 'implementación', 'soporte', 'contrato', 'cierre', 'pregunta', 'indicar']},
        'remediation_strategy': 'Este es un concepto de ventas estándar aplicado al paso 7 (Negociación y Cierre).'
    },
    'RAE17': {
        'stage': 'procesos',
        'instructional_content': (
            "**La Entrega a Equipos Internos (RAE17):**\n\n"
            "Una 'entrega completa sin pérdida de información' es vital para una buena experiencia del cliente. Esto ocurre en los pasos 8 y 9.\n\n"
            "**Checklist para una entrega exitosa:**\n"
            "- **Al equipo Administrativo/Contable (Paso 8):** Debes entregar el contrato firmado, la propuesta final aceptada y los datos de facturación del cliente.\n"
            "- **Al equipo de Implementación (Paso 9):** Debes entregar un resumen del diagnóstico (necesidades y pain points), el alcance técnico detallado (módulos contratados) y los datos de contacto de los usuarios clave del cliente.\n\n"
            "La herramienta principal para esta transición es **WhatsApp** para la comunicación rápida y el correo electrónico para el envío formal de documentos."
        ),
        'description': '¿Qué podría pasar si omites entregar el "resumen del diagnóstico" al equipo de Implementación? ¿Cuál sería el impacto en el cliente?',
        'validation_criteria': {'keywords': ['entrega', 'transición', 'implementación', 'diagnóstico', 'impacto', 'problema', 'error']},
        'remediation_strategy': 'Revisar en detalle los pasos 8 y 9 de la sección 5 (Actividades / Descripción del flujo).'
    },
    'RAE18': {
        'stage': 'procesos',
        'instructional_content': (
            "**Coordinando Expectativas Cliente-Implementación (RAE18):**\n\n"
            "Uno de los mayores riesgos en la post-venta es que el cliente espere algo diferente a lo que el equipo de implementación va a entregar. Tu rol es ser el puente para evitar esto.\n\n"
            "**¿Cómo se logra?**\n"
            "En la transición al equipo de implementación (Paso 9), tu responsabilidad es asegurar una **'transmisión clara de los compromisos comerciales y funcionalidades adquiridas'**.\n\n"
            "Esto puede incluir una breve reunión de 'kick-off' donde participas tú, el cliente y el líder de implementación para repasar el alcance del proyecto y asegurar que todos están en la misma página. Esto gestiona las expectativas y previene malentendidos futuros."
        ),
        'description': 'En tus propias palabras, explica el propósito de una reunión de "kick-off" en la transición de un cliente. ¿Qué buscas evitar con ella?',
        'validation_criteria': {'keywords': ['expectativas', 'alinear', 'transmisión', 'kick-off', 'evitar', 'problemas', 'malentendidos']},
        'remediation_strategy': 'Analizar el "Alcance" (sección 3) y el paso 9 de la sección 5 (Actividades).'
    }
}

ONBOARDING_PLAN_DATA = [
    { 'day': 1, 'stage': 'cultura', 'agent': 'CultureGuide', 'title': 'Inmersión Cultural', 'raes': ['RAE1', 'RAE2', 'RAE3'], 'checkpoint': 80 },
    { 'day': 2, 'stage': 'organizacion', 'agent': 'OrgNavigator', 'title': 'Navegación Organizacional', 'raes': ['RAE4', 'RAE5', 'RAE6'], 'checkpoint': 90 },
    { 'day': 3, 'stage': 'procesos', 'agent': 'ProcessMaster', 'title': 'Dominio de Procesos (Parte 1)', 'raes': ['RAE7', 'RAE8', 'RAE9', 'RAE10', 'RAE11', 'RAE12'], 'checkpoint': 85 },
    { 'day': 4, 'stage': 'procesos', 'agent': 'ProcessMaster', 'title': 'Dominio de Procesos (Parte 2)', 'raes': ['RAE13', 'RAE14', 'RAE15', 'RAE16', 'RAE17', 'RAE18'], 'checkpoint': 85 },
    { 'day': 5, 'stage': 'certificacion', 'agent': 'AssessmentBot', 'title': 'Certificación Integral', 'raes': [], 'checkpoint': 85 },
]

def setup_database():
    """Crea las tablas de la base de datos si no existen y carga los RAEs."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Eliminar tablas si existen para aplicar cambios de esquema
    cursor.execute("DROP TABLE IF EXISTS user_progress")
    cursor.execute("DROP TABLE IF EXISTS rae_library")

    # Crear tabla user_progress
    cursor.execute("""
    CREATE TABLE user_progress (
        user_id TEXT PRIMARY KEY,
        user_name TEXT,
        current_stage TEXT,
        current_rae_id TEXT,
        rae_scores JSON,
        time_spent INTEGER,
        attempts_per_rae JSON,
        identified_gaps JSON,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Crear tabla rae_library
    cursor.execute("""
    CREATE TABLE rae_library (
        rae_id TEXT PRIMARY KEY,
        stage TEXT,
        instructional_content TEXT,
        description TEXT,
        validation_criteria JSON,
        remediation_strategy TEXT
    )
    """)

    # Poblar rae_library
    for rae_id, data in RAE_LIBRARY_DATA.items():
        cursor.execute("""
        INSERT INTO rae_library (rae_id, stage, instructional_content, description, validation_criteria, remediation_strategy)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (rae_id, data['stage'], data.get('instructional_content', ''), data['description'], json.dumps(data['validation_criteria']), data['remediation_strategy']))

    conn.commit()
    conn.close()
    print("Base de datos configurada exitosamente.")

class ProgressTracker:
    """Maneja la lógica de seguimiento del progreso del usuario."""
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def get_user_progress(self, user_id):
        """Recupera el progreso de un usuario."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_progress WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            # Convertir la tupla a un diccionario
            columns = [desc[0] for desc in cursor.description]
            progress_data = dict(zip(columns, row))

            # Deserializar campos JSON
            if 'rae_scores' in progress_data and progress_data['rae_scores']:
                progress_data['rae_scores'] = json.loads(progress_data['rae_scores'])
            if 'attempts_per_rae' in progress_data and progress_data['attempts_per_rae']:
                progress_data['attempts_per_rae'] = json.loads(progress_data['attempts_per_rae'])
            if 'identified_gaps' in progress_data and progress_data['identified_gaps']:
                progress_data['identified_gaps'] = json.loads(progress_data['identified_gaps'])

            return progress_data
        return None

    def create_new_user(self, user_id, user_name):
        """Inicializa el progreso para un nuevo usuario."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        initial_rae_scores = {rae_id: {"status": "pendiente", "score": 0} for rae_id in RAE_LIBRARY_DATA.keys()}
        initial_attempts = {rae_id: 0 for rae_id in RAE_LIBRARY_DATA.keys()}
        
        # Obtener el primer RAE del plan de onboarding
        first_stage_raes = ONBOARDING_PLAN_DATA[0]['raes']
        initial_current_rae_id = first_stage_raes[0] if first_stage_raes else None

        cursor.execute("""
        INSERT INTO user_progress (user_id, user_name, current_stage, current_rae_id, rae_scores, time_spent, attempts_per_rae, identified_gaps)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, user_name, 'cultura', initial_current_rae_id, json.dumps(initial_rae_scores), 0, json.dumps(initial_attempts), json.dumps([])))
        
        conn.commit()
        conn.close()
        print(f"Nuevo usuario '{user_id}' creado.")
        return self.get_user_progress(user_id)

    def update_user_progress(self, user_id, updates):
        """Actualiza el progreso de un usuario con un diccionario de cambios."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Construir la consulta de actualización dinámicamente
        set_clause = ", ".join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values())
        values.append(user_id)

        query = f"UPDATE user_progress SET {set_clause} WHERE user_id = ?"
        
        cursor.execute(query, values)
        
        conn.commit()
        conn.close()
        print(f"Progreso del usuario '{user_id}' actualizado.")

if __name__ == '__main__':
    # Este bloque se ejecuta solo cuando se corre el script directamente
    # Es útil para la configuración inicial
    setup_database()
    
    # Ejemplo de cómo usar el ProgressTracker
    tracker = ProgressTracker()
    user_id = 'ejecutiva_pymes_01'
    
    progress = tracker.get_user_progress(user_id)
    if not progress:
        progress = tracker.create_new_user(user_id)
    
    print("\nEjemplo de datos de progreso:")
    print(json.dumps(progress, indent=2))

    # Ejemplo de actualización
    updates = {
        "time_spent": 120,
        "current_stage": "organizacion"
    }
    tracker.update_user_progress(user_id, updates)
    
    updated_progress = tracker.get_user_progress(user_id)
    print("\nEjemplo de datos de progreso actualizados:")
    print(json.dumps(updated_progress, indent=2))