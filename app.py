import math
from datetime import datetime

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Rehab Quest: Biofísica en acción",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# ESTILO VISUAL
# ============================================================

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 3rem;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e3a8a 100%);
    }
    [data-testid="stSidebar"] * {
        color: white;
    }
    .hero {
        background: radial-gradient(circle at top left, #dbeafe 0%, #f8fafc 43%, #ffffff 100%);
        border: 1px solid #dbeafe;
        border-radius: 30px;
        padding: 30px;
        box-shadow: 0 16px 42px rgba(15, 23, 42, .10);
        margin-bottom: 18px;
    }
    .hero h1 {
        font-size: clamp(2.0rem, 4.5vw, 4.3rem);
        line-height: .95;
        letter-spacing: -0.055em;
        margin-bottom: 12px;
    }
    .hero p {
        color: #334155;
        font-size: 1.06rem;
        line-height: 1.65;
        max-width: 1100px;
    }
    .pill {
        display: inline-block;
        padding: 8px 12px;
        border-radius: 999px;
        background: #e0f2fe;
        color: #075985;
        border: 1px solid #bae6fd;
        margin: 4px 6px 4px 0;
        font-weight: 700;
        font-size: .88rem;
    }
    .mission-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 24px;
        padding: 22px;
        box-shadow: 0 12px 30px rgba(15, 23, 42, .07);
        margin-bottom: 14px;
    }
    .concept-title {
        font-size: 2.1rem;
        font-weight: 900;
        line-height: 1;
        letter-spacing: -0.045em;
        margin: 0 0 10px;
        color: #0f172a;
    }
    .tiny-label {
        text-transform: uppercase;
        letter-spacing: .12em;
        color: #64748b;
        font-weight: 800;
        font-size: .76rem;
    }
    .score-card {
        border-radius: 24px;
        padding: 22px;
        color: white;
        background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 100%);
        box-shadow: 0 16px 36px rgba(29, 78, 216, .22);
    }
    .score-number {
        font-size: 4.2rem;
        font-weight: 950;
        line-height: .95;
        letter-spacing: -.06em;
    }
    .metric-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        padding: 14px 16px;
        margin-bottom: 10px;
    }
    .metric-box strong {
        font-size: 1.25rem;
        color: #0f172a;
    }
    .good-box {
        background: #ecfdf5;
        border: 1px solid #bbf7d0;
        border-radius: 18px;
        padding: 16px;
        color: #14532d;
    }
    .warn-box {
        background: #fffbeb;
        border: 1px solid #fde68a;
        border-radius: 18px;
        padding: 16px;
        color: #78350f;
    }
    .danger-box {
        background: #fef2f2;
        border: 1px solid #fecaca;
        border-radius: 18px;
        padding: 16px;
        color: #7f1d1d;
    }
    .svg-wrap {
        background: linear-gradient(180deg, #f8fafc 0%, #eef6ff 100%);
        border: 1px solid #dbeafe;
        border-radius: 28px;
        padding: 16px;
        min-height: 420px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .footer {
        color: #475569;
        font-size: .92rem;
        line-height: 1.55;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# UTILIDADES
# ============================================================

def clamp(value, low=0, high=100):
    return max(low, min(high, value))


def score_0_5(index_value):
    """
    Convierte un índice de éxito 0-100 en una escala 0-5.
    La escala está pensada como evaluación formativa, no punitiva.
    """
    return round(clamp(index_value, 0, 100) / 20, 1)


def score_label(score):
    if score >= 4.5:
        return "Dominio excelente"
    if score >= 3.5:
        return "Buen control fisiológico"
    if score >= 2.5:
        return "Equilibrio parcial"
    if score >= 1.5:
        return "Sistema inestable"
    return "Fallo crítico"


def score_color_class(score):
    if score >= 3.5:
        return "good-box"
    if score >= 2.0:
        return "warn-box"
    return "danger-box"


def bar_svg(value, label, color="#2563eb"):
    value = clamp(value)
    return f"""
    <div class='metric-box'>
        <div class='tiny-label'>{label}</div>
        <strong>{value:.1f}%</strong>
        <svg viewBox="0 0 420 22" width="100%" height="22" role="img" aria-label="{label}">
            <rect x="0" y="4" width="420" height="14" rx="7" fill="#e2e8f0"></rect>
            <rect x="0" y="4" width="{4.2 * value:.1f}" height="14" rx="7" fill="{color}"></rect>
        </svg>
    </div>
    """


# ============================================================
# DATOS DEL JUEGO
# ============================================================

CONCEPTS = {
    "Gradiente": {
        "emoji": "⛰️",
        "tagline": "La diferencia que da dirección al movimiento.",
        "rehab": "Clave para entender difusión de gases, movimiento de fluidos, potenciales eléctricos, edema, intercambio capilar y trabajo muscular.",
        "mission": "Una persona realiza ejercicio suave, pero su tejido no recibe oxígeno suficiente. Debes crear una diferencia útil sin descompensar el sistema.",
        "variables": {
            "Diferencia entre zonas": (0, 100, 62),
            "Permeabilidad funcional": (0, 100, 58),
            "Distancia de intercambio": (0, 100, 42),
            "Demanda del tejido": (0, 100, 55),
        },
        "goal": "Lograr que el intercambio útil supere la demanda, sin volver excesivo el estrés del tejido.",
    },
    "Flujo": {
        "emoji": "🌊",
        "tagline": "Lo importante no es solo que algo pueda moverse, sino que se mueva.",
        "rehab": "Fundamental para razonar sobre circulación, ventilación, drenaje, movimiento de calor, deslizamiento fascial y conducción de señales.",
        "mission": "El sistema necesita transportar recursos y retirar desechos. Ajusta el motor del flujo sin producir turbulencia o gasto excesivo.",
        "variables": {
            "Impulso del flujo": (0, 100, 64),
            "Resistencia del conducto": (0, 100, 36),
            "Viscosidad o fricción": (0, 100, 34),
            "Capacidad del canal": (0, 100, 70),
        },
        "goal": "Conseguir transporte suficiente con el menor costo posible.",
    },
    "Presión": {
        "emoji": "🫀",
        "tagline": "Una fuerza distribuida que puede impulsar, comprimir o deformar.",
        "rehab": "Sirve para explicar ventilación, retorno venoso, presión arterial, presión intraarticular, compresión terapéutica y carga sobre tejidos.",
        "mission": "Debes usar presión para movilizar un fluido sin sobrecargar las paredes del sistema.",
        "variables": {
            "Presión impulsora": (0, 100, 58),
            "Elasticidad del tejido": (0, 100, 63),
            "Área de distribución": (0, 100, 52),
            "Fragilidad del tejido": (0, 100, 35),
        },
        "goal": "Impulsar movimiento sin causar sobrepresión o deformación excesiva.",
    },
    "Resistencia": {
        "emoji": "🧱",
        "tagline": "La oposición que obliga al sistema a gastar más energía.",
        "rehab": "Aparece en vía aérea, vasos, articulaciones, tejidos blandos, conducción nerviosa, entrenamiento de fuerza y movilidad funcional.",
        "mission": "El cuerpo intenta mover aire, sangre, señales o segmentos corporales, pero algo se opone. Reduce lo innecesario y conserva lo útil.",
        "variables": {
            "Oposición interna": (0, 100, 56),
            "Fuerza disponible": (0, 100, 60),
            "Estrategia de movimiento": (0, 100, 50),
            "Rigidez protectora": (0, 100, 45),
        },
        "goal": "Bajar la resistencia inútil sin eliminar la estabilidad protectora.",
    },
    "Energía": {
        "emoji": "⚡",
        "tagline": "La moneda que permite cambiar, mover, reparar y sostener.",
        "rehab": "Ayuda a comprender fatiga, metabolismo, eficiencia del movimiento, recuperación, termorregulación y dosificación del ejercicio.",
        "mission": "Tu paciente debe completar una tarea funcional. Administra energía para producir trabajo sin caer en fatiga temprana.",
        "variables": {
            "ATP disponible": (0, 100, 62),
            "Eficiencia mecánica": (0, 100, 55),
            "Carga de la tarea": (0, 100, 58),
            "Recuperación entre esfuerzos": (0, 100, 50),
        },
        "goal": "Maximizar trabajo útil, controlar la fatiga y sostener la tarea.",
    },
    "Temperatura": {
        "emoji": "🌡️",
        "tagline": "El regulador silencioso de la velocidad biológica.",
        "rehab": "Modifica viscosidad tisular, velocidad nerviosa, metabolismo, inflamación, extensibilidad y respuesta al ejercicio o a agentes físicos.",
        "mission": "Ajusta el estado térmico para mejorar función sin llevar al tejido a lentitud extrema o estrés térmico.",
        "variables": {
            "Temperatura local": (20, 42, 34),
            "Flujo sanguíneo local": (0, 100, 55),
            "Actividad metabólica": (0, 100, 50),
            "Sensibilidad del tejido": (0, 100, 40),
        },
        "goal": "Mantener una zona térmica funcional que favorezca conducción, metabolismo y extensibilidad.",
    },
    "Membrana": {
        "emoji": "🫧",
        "tagline": "La frontera inteligente que selecciona, detecta y responde.",
        "rehab": "Es esencial para explicar excitabilidad celular, intercambio alveolocapilar, absorción, edema, receptores, canales iónicos y señalización.",
        "mission": "El sistema necesita dejar pasar lo necesario y bloquear lo que altera el equilibrio.",
        "variables": {
            "Selectividad": (0, 100, 62),
            "Permeabilidad": (0, 100, 55),
            "Integridad estructural": (0, 100, 72),
            "Carga externa": (0, 100, 45),
        },
        "goal": "Lograr intercambio regulado, no paso indiscriminado.",
    },
    "Retroalimentación": {
        "emoji": "🔁",
        "tagline": "La conversación interna que evita el caos.",
        "rehab": "Permite explicar equilibrio, control postural, regulación ventilatoria, dolor, tono, homeostasis, aprendizaje motor y adaptación al entrenamiento.",
        "mission": "El sistema se está alejando del objetivo. Ajusta sensores, respuesta y velocidad de corrección.",
        "variables": {
            "Precisión sensorial": (0, 100, 64),
            "Velocidad de respuesta": (0, 100, 58),
            "Intensidad correctiva": (0, 100, 52),
            "Ruido o interferencia": (0, 100, 38),
        },
        "goal": "Corregir desviaciones sin producir oscilaciones exageradas.",
    },
}


# ============================================================
# CÁLCULOS POR CONCEPTO
# ============================================================

def compute_concept(concept, v):
    if concept == "Gradiente":
        gradient = v["Diferencia entre zonas"]
        perm = v["Permeabilidad funcional"]
        dist = v["Distancia de intercambio"]
        demand = v["Demanda del tejido"]
        exchange = clamp(0.52 * gradient + 0.36 * perm - 0.42 * dist + 28)
        stress = clamp(0.35 * gradient + 0.2 * demand + 0.25 * dist)
        success = clamp(100 - abs(exchange - demand) * 1.25 - max(0, stress - 70) * 1.1)
        metrics = {
            "Intercambio útil": exchange,
            "Demanda cubierta": clamp(exchange - demand + 70),
            "Estrés tisular": stress,
            "Éxito fisiológico": success,
        }
        explanation = (
            "El gradiente crea dirección para el intercambio. Si la diferencia entre zonas aumenta, "
            "el movimiento mejora; pero si la distancia es grande o la demanda supera la oferta, "
            "el tejido queda en déficit. En rehabilitación, esta lógica ayuda a pensar oxigenación, edema, "
            "intercambio capilar y recuperación tisular."
        )
        return metrics, success, explanation

    if concept == "Flujo":
        drive = v["Impulso del flujo"]
        resistance = v["Resistencia del conducto"]
        viscosity = v["Viscosidad o fricción"]
        capacity = v["Capacidad del canal"]
        flow = clamp(0.72 * drive + 0.42 * capacity - 0.55 * resistance - 0.35 * viscosity + 35)
        cost = clamp(0.38 * drive + 0.48 * resistance + 0.33 * viscosity)
        success = clamp(flow - max(0, cost - 58) * 1.15)
        metrics = {
            "Flujo efectivo": flow,
            "Costo energético": cost,
            "Transporte neto": clamp(flow - cost * 0.25 + 25),
            "Éxito fisiológico": success,
        }
        explanation = (
            "El flujo depende de un impulso que moviliza y de resistencias que frenan. "
            "Más impulso no siempre resuelve el problema: si la resistencia o la viscosidad son altas, "
            "el costo sube. Esto sirve para razonar ventilación, retorno venoso, drenaje, perfusión y movilidad."
        )
        return metrics, success, explanation

    if concept == "Presión":
        pressure = v["Presión impulsora"]
        elasticity = v["Elasticidad del tejido"]
        area = v["Área de distribución"]
        fragility = v["Fragilidad del tejido"]
        movement = clamp(0.65 * pressure + 0.28 * elasticity + 0.25 * area)
        overload = clamp(0.55 * pressure + 0.45 * fragility - 0.35 * area - 0.25 * elasticity + 30)
        success = clamp(movement - max(0, overload - 55) * 1.25)
        metrics = {
            "Movimiento producido": movement,
            "Sobrecarga por presión": overload,
            "Distribución segura": clamp(area + elasticity * 0.35 - fragility * 0.25),
            "Éxito fisiológico": success,
        }
        explanation = (
            "La presión puede impulsar fluidos o deformar tejidos. El mismo aumento de presión puede ser útil "
            "o riesgoso según la elasticidad, el área de distribución y la fragilidad. Esta lógica es clave "
            "para compresión, ventilación, carga articular, retorno venoso y prevención de lesión por presión."
        )
        return metrics, success, explanation

    if concept == "Resistencia":
        opposition = v["Oposición interna"]
        force = v["Fuerza disponible"]
        strategy = v["Estrategia de movimiento"]
        protective = v["Rigidez protectora"]
        useful_stability = clamp(0.45 * protective + 0.35 * strategy)
        mobility = clamp(0.62 * force + 0.45 * strategy - 0.55 * opposition - 0.18 * protective + 35)
        cost = clamp(0.5 * opposition + 0.22 * force + 0.32 * protective)
        success = clamp(mobility + useful_stability * 0.25 - max(0, cost - 62) * 1.15)
        metrics = {
            "Movilidad funcional": mobility,
            "Estabilidad útil": useful_stability,
            "Costo de vencer resistencia": cost,
            "Éxito fisiológico": success,
        }
        explanation = (
            "No toda resistencia es mala: algo de rigidez protege y estabiliza. El problema aparece cuando la oposición "
            "impide flujo, movimiento o señal. El razonamiento rehabilitador debe distinguir resistencia útil de resistencia "
            "innecesaria."
        )
        return metrics, success, explanation

    if concept == "Energía":
        atp = v["ATP disponible"]
        efficiency = v["Eficiencia mecánica"]
        load = v["Carga de la tarea"]
        recovery = v["Recuperación entre esfuerzos"]
        work = clamp(0.45 * atp + 0.5 * efficiency + 0.25 * recovery - 0.18 * load + 20)
        fatigue = clamp(0.55 * load - 0.25 * atp - 0.28 * recovery + 45)
        success = clamp(work - max(0, fatigue - 52) * 1.25)
        metrics = {
            "Trabajo útil": work,
            "Fatiga acumulada": fatigue,
            "Reserva funcional": clamp(atp * 0.42 + recovery * 0.45 + efficiency * 0.22),
            "Éxito fisiológico": success,
        }
        explanation = (
            "La energía no solo importa para hacer fuerza. También sostiene bombas iónicas, reparación, metabolismo y control térmico. "
            "En rehabilitación, dosificar carga y descanso evita que una tarea correcta se convierta en fatiga incapacitante."
        )
        return metrics, success, explanation

    if concept == "Temperatura":
        temp = v["Temperatura local"]
        flow = v["Flujo sanguíneo local"]
        metabolism = v["Actividad metabólica"]
        sensitivity = v["Sensibilidad del tejido"]
        thermal_zone = clamp(100 - abs(temp - 36.5) * 13)
        function = clamp(0.48 * thermal_zone + 0.25 * flow + 0.22 * metabolism - 0.18 * sensitivity + 15)
        risk = clamp(abs(temp - 36.5) * 8 + 0.25 * sensitivity + max(0, metabolism - 70) * 0.25)
        success = clamp(function - max(0, risk - 45) * 1.2)
        metrics = {
            "Zona térmica funcional": thermal_zone,
            "Función biológica": function,
            "Riesgo térmico": risk,
            "Éxito fisiológico": success,
        }
        explanation = (
            "La temperatura cambia la velocidad de los procesos biológicos. Puede facilitar extensibilidad, conducción y metabolismo, "
            "pero también aumentar riesgo si el tejido es sensible o la carga metabólica es alta. El reto es encontrar la zona funcional, "
            "no simplemente calentar o enfriar."
        )
        return metrics, success, explanation

    if concept == "Membrana":
        selectivity = v["Selectividad"]
        permeability = v["Permeabilidad"]
        integrity = v["Integridad estructural"]
        external = v["Carga externa"]
        regulated_exchange = clamp(0.36 * selectivity + 0.34 * permeability + 0.42 * integrity - 0.18 * external + 18)
        leak = clamp(0.45 * permeability + 0.42 * external - 0.42 * selectivity - 0.34 * integrity + 45)
        success = clamp(regulated_exchange - max(0, leak - 48) * 1.25)
        metrics = {
            "Intercambio regulado": regulated_exchange,
            "Fuga o paso no controlado": leak,
            "Barrera funcional": clamp(selectivity * 0.42 + integrity * 0.5 - external * 0.18 + 20),
            "Éxito fisiológico": success,
        }
        explanation = (
            "Una membrana sana no es una pared cerrada: es una frontera selectiva. Permite intercambio, detecta señales y protege. "
            "Si aumenta la permeabilidad sin selectividad o cae la integridad, el sistema pierde control. Esto conecta con edema, "
            "excitabilidad, intercambio gaseoso y señalización."
        )
        return metrics, success, explanation

    if concept == "Retroalimentación":
        sensory = v["Precisión sensorial"]
        speed = v["Velocidad de respuesta"]
        correction = v["Intensidad correctiva"]
        noise = v["Ruido o interferencia"]
        control = clamp(0.42 * sensory + 0.34 * speed + 0.32 * correction - 0.48 * noise + 28)
        oscillation = clamp(0.42 * correction + 0.38 * noise - 0.28 * sensory - 0.18 * speed + 38)
        success = clamp(control - max(0, oscillation - 45) * 1.2)
        metrics = {
            "Control adaptativo": control,
            "Oscilación del sistema": oscillation,
            "Calidad de corrección": clamp(sensory * 0.35 + speed * 0.3 + correction * 0.25 - noise * 0.25 + 25),
            "Éxito fisiológico": success,
        }
        explanation = (
            "La retroalimentación compara, corrige y aprende. Si los sensores fallan, la respuesta llega tarde o la corrección es exagerada, "
            "el sistema oscila. Esta idea es decisiva en equilibrio, control postural, ventilación, dolor, tono y aprendizaje motor."
        )
        return metrics, success, explanation

    return {}, 0, "Sin explicación disponible."


# ============================================================
# IMÁGENES SVG ORIGINALES
# ============================================================

def concept_svg(concept, values, metrics):
    success = metrics.get("Éxito fisiológico", 50)
    accent = "#16a34a" if success >= 70 else "#d97706" if success >= 40 else "#dc2626"

    if concept == "Gradiente":
        diff = values["Diferencia entre zonas"]
        dist = values["Distancia de intercambio"]
        return f"""
        <div class='svg-wrap'>
        <svg viewBox="0 0 720 460" width="100%" role="img" aria-label="Gradiente fisiológico">
          <defs><linearGradient id="gradA" x1="0" x2="1"><stop offset="0%" stop-color="#1d4ed8"/><stop offset="100%" stop-color="#bae6fd"/></linearGradient></defs>
          <rect x="40" y="70" width="260" height="290" rx="34" fill="#dbeafe" stroke="#2563eb" stroke-width="4"/>
          <rect x="420" y="70" width="260" height="290" rx="34" fill="#f8fafc" stroke="#94a3b8" stroke-width="4"/>
          <rect x="328" y="{90 + dist*.8}" width="{28 + dist*.35}" height="{250 - dist}" rx="18" fill="#e2e8f0" stroke="#64748b" stroke-width="3"/>
          <path d="M300 220 C 345 {120 + dist*.6}, 380 {120 + dist*.6}, 420 220" stroke="url(#gradA)" stroke-width="{12 + diff*.10}" fill="none"/>
          <polygon points="420,220 390,204 390,236" fill="#1d4ed8"/>
          <text x="82" y="132" font-size="26" font-weight="800" fill="#1e3a8a">Zona alta</text>
          <text x="457" y="132" font-size="26" font-weight="800" fill="#334155">Zona baja</text>
          <text x="225" y="415" font-size="24" font-weight="800" fill="{accent}">Éxito: {score_0_5(success)}/5</text>
          <circle cx="118" cy="190" r="18" fill="#2563eb"/><circle cx="172" cy="235" r="15" fill="#2563eb"/>
          <circle cx="230" cy="180" r="20" fill="#2563eb"/><circle cx="510" cy="235" r="10" fill="#93c5fd"/>
        </svg></div>"""

    if concept == "Flujo":
        flow = metrics["Flujo efectivo"]
        resistance = values["Resistencia del conducto"]
        return f"""
        <div class='svg-wrap'><svg viewBox="0 0 720 460" width="100%" role="img" aria-label="Flujo fisiológico">
          <path d="M80 235 C190 120, 310 330, 440 210 S610 205, 660 150" stroke="#cbd5e1" stroke-width="{70-resistance*.35}" fill="none" stroke-linecap="round"/>
          <path d="M80 235 C190 120, 310 330, 440 210 S610 205, 660 150" stroke="#0ea5e9" stroke-width="{14+flow*.13}" fill="none" stroke-linecap="round"/>
          <polygon points="660,150 620,142 636,178" fill="#0ea5e9"/>
          <circle cx="130" cy="218" r="18" fill="#2563eb"/><circle cx="245" cy="217" r="14" fill="#2563eb"/><circle cx="378" cy="247" r="16" fill="#2563eb"/><circle cx="540" cy="183" r="13" fill="#2563eb"/>
          <rect x="250" y="80" width="{80+resistance}" height="54" rx="18" fill="#fecaca" stroke="#dc2626" stroke-width="3"/>
          <text x="267" y="115" font-size="20" font-weight="800" fill="#991b1b">resistencia</text>
          <text x="225" y="415" font-size="24" font-weight="800" fill="{accent}">Éxito: {score_0_5(success)}/5</text>
        </svg></div>"""

    if concept == "Presión":
        pressure = values["Presión impulsora"]
        overload = metrics["Sobrecarga por presión"]
        return f"""
        <div class='svg-wrap'><svg viewBox="0 0 720 460" width="100%" role="img" aria-label="Presión fisiológica">
          <ellipse cx="360" cy="230" rx="{135+pressure*.55}" ry="{85+pressure*.22}" fill="#fee2e2" stroke="#ef4444" stroke-width="{4+overload*.04}"/>
          <circle cx="360" cy="230" r="{32+pressure*.25}" fill="#fca5a5"/>
          <g stroke="#dc2626" stroke-width="7" stroke-linecap="round"><line x1="360" y1="80" x2="360" y2="145"/><line x1="360" y1="380" x2="360" y2="315"/><line x1="130" y1="230" x2="225" y2="230"/><line x1="590" y1="230" x2="495" y2="230"/></g>
          <text x="260" y="64" font-size="24" font-weight="900" fill="#991b1b">presión distribuida</text>
          <text x="225" y="415" font-size="24" font-weight="800" fill="{accent}">Éxito: {score_0_5(success)}/5</text>
        </svg></div>"""

    if concept == "Resistencia":
        opposition = values["Oposición interna"]
        mobility = metrics["Movilidad funcional"]
        return f"""
        <div class='svg-wrap'><svg viewBox="0 0 720 460" width="100%" role="img" aria-label="Resistencia fisiológica">
          <rect x="70" y="190" width="580" height="85" rx="42" fill="#e0f2fe" stroke="#0284c7" stroke-width="4"/>
          <rect x="305" y="180" width="{60+opposition*1.6}" height="105" rx="28" fill="#fed7aa" stroke="#d97706" stroke-width="4"/>
          <path d="M105 232 H{295 + mobility*2.2}" stroke="#2563eb" stroke-width="18" stroke-linecap="round"/>
          <polygon points="{295 + mobility*2.2},232 {265 + mobility*2.2},212 {265 + mobility*2.2},252" fill="#2563eb"/>
          <text x="255" y="145" font-size="26" font-weight="900" fill="#9a3412">oposición al movimiento</text>
          <text x="225" y="415" font-size="24" font-weight="800" fill="{accent}">Éxito: {score_0_5(success)}/5</text>
        </svg></div>"""

    if concept == "Energía":
        fatigue = metrics["Fatiga acumulada"]
        work = metrics["Trabajo útil"]
        return f"""
        <div class='svg-wrap'><svg viewBox="0 0 720 460" width="100%" role="img" aria-label="Energía fisiológica">
          <rect x="120" y="105" width="480" height="130" rx="40" fill="#fef3c7" stroke="#d97706" stroke-width="5"/>
          <rect x="150" y="135" width="{work*4.0}" height="70" rx="28" fill="#f59e0b"/>
          <polygon points="340,70 282,235 360,210 320,390 440,175 364,198" fill="#fde047" stroke="#ca8a04" stroke-width="5"/>
          <circle cx="570" cy="115" r="{18+fatigue*.18}" fill="#fecaca" stroke="#dc2626" stroke-width="4"/>
          <text x="513" y="120" font-size="18" font-weight="800" fill="#991b1b">fatiga</text>
          <text x="225" y="415" font-size="24" font-weight="800" fill="{accent}">Éxito: {score_0_5(success)}/5</text>
        </svg></div>"""

    if concept == "Temperatura":
        temp = values["Temperatura local"]
        y = 350 - (temp - 20) * 11
        return f"""
        <div class='svg-wrap'><svg viewBox="0 0 720 460" width="100%" role="img" aria-label="Temperatura fisiológica">
          <rect x="120" y="70" width="110" height="300" rx="55" fill="#e2e8f0" stroke="#64748b" stroke-width="5"/>
          <rect x="150" y="{y}" width="50" height="{370-y}" rx="25" fill="{accent}"/>
          <circle cx="175" cy="365" r="65" fill="{accent}"/>
          <path d="M360 150 C430 80, 530 95, 590 170 C645 242, 590 340, 488 340 C390 340, 330 250, 360 150Z" fill="#dbeafe" stroke="#2563eb" stroke-width="5"/>
          <path d="M410 245 C460 205, 500 270, 555 220" stroke="#0ea5e9" stroke-width="{8+metrics['Función biológica']*.08}" fill="none"/>
          <text x="365" y="115" font-size="24" font-weight="900" fill="#1e3a8a">tejido en respuesta térmica</text>
          <text x="225" y="415" font-size="24" font-weight="800" fill="{accent}">Éxito: {score_0_5(success)}/5</text>
        </svg></div>"""

    if concept == "Membrana":
        leak = metrics["Fuga o paso no controlado"]
        regulated = metrics["Intercambio regulado"]
        return f"""
        <div class='svg-wrap'><svg viewBox="0 0 720 460" width="100%" role="img" aria-label="Membrana fisiológica">
          <rect x="95" y="95" width="530" height="255" rx="56" fill="#f8fafc" stroke="#94a3b8" stroke-width="4"/>
          <line x1="360" y1="95" x2="360" y2="350" stroke="#7c3aed" stroke-width="{8+values['Integridad estructural']*.08}" stroke-dasharray="18 10"/>
          <circle cx="220" cy="180" r="18" fill="#2563eb"/><circle cx="255" cy="250" r="14" fill="#2563eb"/>
          <circle cx="{405+regulated*.85}" cy="210" r="14" fill="#16a34a"/><circle cx="{405+leak*.45}" cy="270" r="10" fill="#dc2626"/>
          <path d="M280 215 C 315 175, 335 175, 360 215 C 390 255, 420 250, 455 225" stroke="#16a34a" stroke-width="8" fill="none"/>
          <text x="250" y="70" font-size="26" font-weight="900" fill="#5b21b6">frontera selectiva</text>
          <text x="225" y="415" font-size="24" font-weight="800" fill="{accent}">Éxito: {score_0_5(success)}/5</text>
        </svg></div>"""

    if concept == "Retroalimentación":
        control = metrics["Control adaptativo"]
        oscillation = metrics["Oscilación del sistema"]
        return f"""
        <div class='svg-wrap'><svg viewBox="0 0 720 460" width="100%" role="img" aria-label="Retroalimentación fisiológica">
          <circle cx="360" cy="225" r="112" fill="#dbeafe" stroke="#2563eb" stroke-width="5"/>
          <circle cx="360" cy="225" r="{30+control*.45}" fill="none" stroke="#16a34a" stroke-width="9"/>
          <path d="M360 90 C520 90, 585 230, 485 330" stroke="#2563eb" stroke-width="9" fill="none"/><polygon points="485,330 485,290 520,312" fill="#2563eb"/>
          <path d="M360 360 C200 360, 135 220, 235 120" stroke="#7c3aed" stroke-width="9" fill="none"/><polygon points="235,120 235,160 200,138" fill="#7c3aed"/>
          <path d="M210 {230-oscillation*.5} C270 {170+oscillation*.3}, 450 {310-oscillation*.3}, 520 {230+oscillation*.5}" stroke="#dc2626" stroke-width="5" fill="none" stroke-dasharray="12 10"/>
          <text x="252" y="222" font-size="26" font-weight="900" fill="#1e3a8a">detectar</text><text x="372" y="262" font-size="26" font-weight="900" fill="#166534">corregir</text>
          <text x="225" y="415" font-size="24" font-weight="800" fill="{accent}">Éxito: {score_0_5(success)}/5</text>
        </svg></div>"""

    return ""


# ============================================================
# ESTADO
# ============================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "student_name" not in st.session_state:
    st.session_state.student_name = ""


# ============================================================
# INTERFAZ
# ============================================================

with st.sidebar:
    st.markdown("## 🧠 Rehab Quest")
    st.markdown("### Biofísica en acción")
    st.write("Juego serio para comprender principios físicos que sostienen la fisiología humana útil en rehabilitación.")
    st.divider()

    student_name = st.text_input("Nombre del estudiante o grupo", value=st.session_state.student_name)
    st.session_state.student_name = student_name.strip()

    concept = st.radio(
        "Elige una estación",
        list(CONCEPTS.keys()),
        format_func=lambda x: f"{CONCEPTS[x]['emoji']} {x}",
        index=0,
    )

    st.divider()
    if st.button("🧹 Reiniciar historial", use_container_width=True):
        st.session_state.history = []
        st.rerun()


data = CONCEPTS[concept]

st.markdown(
    f"""
    <div class='hero'>
        <span class='pill'>Juego serio</span>
        <span class='pill'>Rehabilitación</span>
        <span class='pill'>Biofísica aplicada</span>
        <h1>{data['emoji']} Rehab Quest:<br>biofísica en acción</h1>
        <p>
        En este juego no memorizas definiciones: calibras fenómenos fisiológicos. Cada estación representa un principio físico
        que un rehabilitador necesita reconocer para entender movimiento, control, intercambio, fatiga, ventilación, circulación,
        señalización celular y adaptación funcional.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


left, right = st.columns([1.08, 0.92], gap="large")

with left:
    st.markdown("<div class='mission-card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='tiny-label'>Estación activa</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='concept-title'>{data['emoji']} {concept}</div>", unsafe_allow_html=True)
    st.markdown(f"**Idea clave:** {data['tagline']}")
    st.markdown(f"**Por qué importa en rehabilitación:** {data['rehab']}")
    st.markdown(f"**Misión:** {data['mission']}")
    st.markdown(f"**Meta del reto:** {data['goal']}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### 🎛️ Calibra el sistema")
    values = {}
    cols = st.columns(2)
    for i, (var, params) in enumerate(data["variables"].items()):
        min_v, max_v, default = params
        with cols[i % 2]:
            values[var] = st.slider(var, min_value=min_v, max_value=max_v, value=default, step=1)

    metrics, success, explanation = compute_concept(concept, values)
    score = score_0_5(success)

    register = st.button("✅ Registrar intento", type="primary", use_container_width=True)

    if register:
        st.session_state.history.append(
            {
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "estudiante_grupo": st.session_state.student_name or "Sin nombre",
                "concepto": concept,
                "puntaje_0_5": score,
                "clasificacion": score_label(score),
                **{f"variable_{k}": v for k, v in values.items()},
                **{f"metrica_{k}": round(v, 1) for k, v in metrics.items()},
            }
        )
        st.success(f"Intento registrado: {score}/5 — {score_label(score)}")

with right:
    st.markdown(concept_svg(concept, values, metrics), unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class='score-card'>
            <div class='tiny-label' style='color:#bfdbfe'>Puntaje de éxito</div>
            <div class='score-number'>{score}/5</div>
            <div style='font-size:1.1rem;font-weight:800;margin-top:8px'>{score_label(score)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

m1, m2 = st.columns([0.9, 1.1], gap="large")

with m1:
    st.markdown("### 📊 Lectura del sistema")
    colors = ["#2563eb", "#0891b2", "#7c3aed", "#16a34a"]
    html_metrics = ""
    for idx, (name, value) in enumerate(metrics.items()):
        html_metrics += bar_svg(value, name, colors[idx % len(colors)])
    st.markdown(html_metrics, unsafe_allow_html=True)

with m2:
    st.markdown("### 🧩 Retroalimentación formativa")
    st.markdown(
        f"""
        <div class='{score_color_class(score)}'>
            <strong>{score_label(score)} — {score}/5.</strong><br><br>
            {explanation}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### Preguntas para discusión")
    st.markdown(
        f"""
        1. ¿Qué variable física tuvo mayor impacto en el resultado de **{concept.lower()}**?
        2. ¿Qué pasaría si se exagera la corrección?
        3. ¿Cómo se observaría este fenómeno en una situación real de rehabilitación?
        4. ¿Qué decisión clínica o pedagógica tomarías para mejorar el puntaje?
        """
    )


st.divider()

st.markdown("## 🏁 Historial de intentos")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "⬇️ Descargar resultados en CSV",
        data=csv,
        file_name="resultados_rehab_quest_biofisica.csv",
        mime="text/csv",
        use_container_width=True,
    )

    avg = round(df["puntaje_0_5"].mean(), 2)
    best = df.sort_values("puntaje_0_5", ascending=False).iloc[0]
    report = f"""# Reporte de Rehab Quest: Biofísica en acción

Fecha de descarga: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Estudiante o grupo: {st.session_state.student_name or "Sin nombre"}

## Resumen

- Intentos registrados: {len(df)}
- Promedio de puntaje: {avg}/5
- Mejor estación: {best["concepto"]}
- Mejor puntaje: {best["puntaje_0_5"]}/5 ({best["clasificacion"]})

## Interpretación docente

El puntaje de éxito de 0 a 5 representa qué tan bien el estudiante calibró las variables físicas del fenómeno fisiológico.
No debe interpretarse como una nota aislada, sino como evidencia de razonamiento: identifica relaciones entre impulso,
oposición, intercambio, control, energía y estabilidad funcional.

## Recomendación

Solicitar al estudiante que explique por escrito por qué movió cada variable y cómo trasladaría esa relación a una situación
de rehabilitación real.
"""
    st.download_button(
        "⬇️ Descargar reporte en Markdown",
        data=report.encode("utf-8"),
        file_name="reporte_rehab_quest_biofisica.md",
        mime="text/markdown",
        use_container_width=True,
    )
else:
    st.info("Aún no hay intentos registrados. Calibra una estación y presiona **Registrar intento**.")


st.markdown(
    """
    <p class='footer'>
    Diseño didáctico: aplicación orientada a aprendizaje activo. Las imágenes son esquemas originales generados con SVG
    para representar fenómenos fisiológicos de manera conceptual, no como atlas anatómico diagnóstico.
    </p>
    """,
    unsafe_allow_html=True,
)
