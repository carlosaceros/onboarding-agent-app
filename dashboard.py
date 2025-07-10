
import plotly.graph_objects as go
import json

def create_competency_spider_chart(rae_scores, rae_library):
    """Crea un gráfico de araña para visualizar las competencias."""
    
    # Agrupar RAEs por etapa y calcular el score promedio
    scores_by_stage = {}
    for rae_id, score_data in rae_scores.items():
        stage = rae_library.get(rae_id, {}).get('stage')
        if stage:
            if stage not in scores_by_stage:
                scores_by_stage[stage] = {'total': 0, 'count': 0}
            scores_by_stage[stage]['total'] += score_data.get('score', 0)
            scores_by_stage[stage]['count'] += 1

    labels = list(scores_by_stage.keys())
    values = []
    for stage in labels:
        if scores_by_stage[stage]['count'] > 0:
            avg_score = scores_by_stage[stage]['total'] / scores_by_stage[stage]['count']
            values.append(avg_score)
        else:
            values.append(0)

    fig = go.Figure(
        data=go.Scatterpolar(
            r=values,
            theta=labels,
            fill='toself',
            name='Competencia'
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        title="Mapa de Competencias"
    )
    return fig

def get_rae_status_list(rae_scores):
    """Obtiene una lista del estado de cada RAE para mostrar en el UI."""
    status_list = []
    for rae_id, data in rae_scores.items():
        status = data.get('status', 'pendiente').capitalize()
        icon = "✅" if status == 'Aprobado' else ("❌" if status == 'Fallido' else "⏳")
        status_list.append(f"{icon} **{rae_id}**: {status}")
    return status_list

# Ejemplo de uso (requiere datos simulados)
if __name__ == '__main__':
    # Datos simulados para la prueba
    from database import RAE_LIBRARY_DATA
    
    simulated_rae_scores = {
        'RAE1': {'status': 'aprobado', 'score': 100},
        'RAE2': {'status': 'aprobado', 'score': 90},
        'RAE3': {'status': 'fallido', 'score': 40},
        'RAE4': {'status': 'pendiente', 'score': 0},
        'RAE5': {'status': 'pendiente', 'score': 0},
        'RAE6': {'status': 'pendiente', 'score': 0},
    }
    
    simulated_rae_library = RAE_LIBRARY_DATA

    print("Generando gráfico de araña de ejemplo...")
    fig = create_competency_spider_chart(simulated_rae_scores, simulated_rae_library)
    # fig.show() # Esto abriría el gráfico en un navegador
    print("Gráfico generado. Para verlo, descomenta fig.show() en el script.")

    print("\nGenerando lista de estado de RAEs de ejemplo...")
    status_display = get_rae_status_list(simulated_rae_scores)
    for item in status_display:
        print(item)
