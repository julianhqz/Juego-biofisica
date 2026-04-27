# Código Homeostasis
# App educativa en Streamlit para aprender sistemas humanos desde la física.
# Autor editable: Julián Andrés Hernández Quintero / curso de Biofísica

from __future__ import annotations

import base64
import json
from datetime import datetime
from html import escape
from typing import Dict, List, Tuple

import streamlit as st

st.set_page_config(
    page_title="Código Homeostasis",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Estilos visuales
# -----------------------------

CUSTOM_CSS = """
<style>
:root{
  --bg:#f8fafc;
  --ink:#0f172a;
  --muted:#475569;
  --blue:#2563eb;
  --cyan:#0891b2;
  --green:#16a34a;
  --amber:#d97706;
  --red:#dc2626;
  --card:#ffffff;
  --line:#e2e8f0;
}
[data-testid="stAppViewContainer"]{
  background: radial-gradient(circle at top left, #dbeafe 0, transparent 28%),
              linear-gradient(180deg,#f8fafc 0%,#eef2ff 100%);
}
[data-testid="stSidebar"]{
  background: linear-gradient(180deg,#0f172a 0%,#172554 100%);
}
[data-testid="stSidebar"] *{color:#f8fafc !important;}
.block-container{padding-top:1.4rem;padding-bottom:3rem;}
.hero-card{
  padding: 1.4rem 1.5rem;
  border-radius: 24px;
  color: white;
  background: linear-gradient(135deg,#0f172a 0%,#1d4ed8 58%,#06b6d4 100%);
  box-shadow: 0 16px 36px rgba(15,23,42,.22);
  border: 1px solid rgba(255,255,255,.12);
}
.hero-card h1{font-size:2.35rem;margin:0 0 .45rem 0;line-height:1.05;}
.hero-card p{font-size:1.02rem;margin:.2rem 0;color:#dbeafe;line-height:1.55;max-width:1050px;}
.card{
  background:rgba(255,255,255,.88);
  border:1px solid var(--line);
  border-radius:22px;
  padding:1.05rem 1.15rem;
  box-shadow:0 10px 24px rgba(15,23,42,.07);
  margin-bottom:1rem;
}
.metric-card{
  background:#0f172a;
  color:white;
  border-radius:18px;
  padding:1rem;
  border:1px solid rgba(255,255,255,.08);
  box-shadow:0 8px 18px rgba(15,23,42,.14);
}
.metric-card small{color:#93c5fd;font-size:.82rem;display:block;margin-bottom:.25rem;}
.metric-card strong{font-size:1.35rem;}
.badge{
  display:inline-block;
  padding:.35rem .7rem;
  border-radius:999px;
  font-size:.85rem;
  font-weight:700;
  margin:.12rem .18rem .12rem 0;
  border:1px solid #bfdbfe;
  color:#1e3a8a;
  background:#dbeafe;
}
.badge-green{background:#dcfce7;color:#166534;border-color:#bbf7d0;}
.badge-amber{background:#fef3c7;color:#92400e;border-color:#fde68a;}
.badge-red{background:#fee2e2;color:#991b1b;border-color:#fecaca;}
.feedback{
  border-left:5px solid #2563eb;
  background:#eff6ff;
  padding:.9rem 1rem;
  border-radius:16px;
  line-height:1.55;
}
.case-box{
  background:linear-gradient(180deg,#fff7ed,#fffbeb);
  border:1px solid #fed7aa;
  border-radius:20px;
  padding:1rem 1.1rem;
  color:#7c2d12;
}
.svg-wrap{
  background:linear-gradient(180deg,#ffffff,#eff6ff);
  border:1px solid #dbeafe;
  border-radius:22px;
  padding:.8rem;
  min-height:360px;
  display:flex;
  align-items:center;
  justify-content:center;
  box-shadow:inset 0 0 26px rgba(37,99,235,.05);
}
.step-label{font-weight:800;color:#1e3a8a;margin-bottom:.35rem;}
hr{border:none;border-top:1px solid #e2e8f0;margin:1.2rem 0;}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------
# Datos del juego
# -----------------------------

CONCEPTS = {
    "Gradiente": "Diferencia entre dos puntos: presión, concentración, voltaje, temperatura o carga mecánica. Sin diferencia no hay dirección clara del movimiento.",
    "Flujo": "Movimiento efectivo de aire, sangre, iones, información, calor, fuerza o fluidos corporales.",
    "Presión": "Fuerza distribuida sobre una superficie o dentro de un compartimento; puede impulsar, distender o comprimir.",
    "Resistencia": "Oposición al movimiento o transferencia; puede ser vascular, respiratoria, mecánica, eléctrica, sináptica o tisular.",
    "Energía": "Capacidad de producir cambio o trabajo: ATP, energía elástica, gradientes electroquímicos, calor o trabajo mecánico.",
    "Temperatura": "Modifica la velocidad de reacciones, viscosidad, conducción, extensibilidad y respuesta molecular.",
    "Membrana": "Barrera selectiva y activa que filtra, transduce señales y regula la comunicación con el entorno.",
    "Retroalimentación": "Comparación entre estado actual y necesidad funcional; corrige o amplifica la respuesta del sistema.",
}

SYSTEMS: Dict[str, Dict] = {
    "Musculoesquelético": {
        "emoji": "🦴",
        "subtitle": "Palancas, fuerza, rigidez, deformación y control de carga.",
        "mission": "Un estudiante realiza salto vertical repetido. Al final aparece fatiga, pérdida de potencia y menor control de aterrizaje.",
        "goal": "Restaurar fuerza útil y estabilidad mecánica sin aumentar demasiado la sobrecarga.",
        "concept_map": {
            "Gradiente": "Diferencias de tensión, longitud muscular, carga y deformación tisular.",
            "Flujo": "Transmisión de fuerza a través de cadenas cinéticas, tendones y articulaciones.",
            "Presión": "Presión articular, compresión tisular y distribución de fuerzas de contacto.",
            "Resistencia": "Rigidez, fricción, inercia, masa externa y oposición del tejido al movimiento.",
            "Energía": "ATP para contracción y energía elástica almacenada en tendones.",
            "Temperatura": "Afecta viscosidad, extensibilidad y velocidad de contracción.",
            "Membrana": "Sarcolema y membranas celulares regulan excitabilidad e intercambio iónico.",
            "Retroalimentación": "Propiocepción y control motor ajustan postura, fuerza y precisión.",
        },
        "variables": {
            "activacion": (0, 100, 65, "Activación neural"),
            "rigidez": (0, 100, 42, "Rigidez/resistencia mecánica"),
            "temperatura": (20, 42, 34, "Temperatura funcional"),
            "propiocepcion": (0, 100, 70, "Retroalimentación propioceptiva"),
        },
        "correct_concepts": ["Resistencia", "Energía", "Retroalimentación"],
    },
    "Neuromuscular": {
        "emoji": "⚡",
        "subtitle": "Membranas excitables, gradientes iónicos, sinapsis y contracción.",
        "mission": "La señal nerviosa llega débil al músculo. La contracción ocurre tarde y con poca eficacia.",
        "goal": "Aumentar la transmisión neuromuscular efectiva y reducir el riesgo de fallo de conducción.",
        "concept_map": {
            "Gradiente": "Gradientes electroquímicos de sodio, potasio, calcio y cloro.",
            "Flujo": "Flujo de iones y propagación del potencial de acción.",
            "Presión": "Menor papel directo, aunque hay tensión local y microambientes tisulares.",
            "Resistencia": "Resistencia de membrana y resistencia sináptica a la transmisión.",
            "Energía": "ATP para bombas iónicas, reciclaje vesicular y acoplamiento excitación-contracción.",
            "Temperatura": "Modifica velocidad de conducción y cinética de canales.",
            "Membrana": "Base de la excitabilidad, umbral, despolarización y repolarización.",
            "Retroalimentación": "Reflejos e inhibición/facilitación ajustan el output motor.",
        },
        "variables": {
            "gradiente": (0, 100, 75, "Gradiente iónico"),
            "membrana": (0, 100, 84, "Integridad de membrana"),
            "resistencia": (0, 100, 28, "Resistencia sináptica"),
            "temperatura": (20, 42, 36, "Temperatura"),
        },
        "correct_concepts": ["Gradiente", "Membrana", "Flujo"],
    },
    "Cardiopulmonar": {
        "emoji": "🫁",
        "subtitle": "Presión, flujo, resistencia, membrana alveolocapilar e intercambio gaseoso.",
        "mission": "Durante ejercicio, el estudiante presenta aumento del trabajo respiratorio y menor eficiencia de intercambio gaseoso.",
        "goal": "Optimizar flujo ventilatorio/perfusional y mantener intercambio gaseoso suficiente.",
        "concept_map": {
            "Gradiente": "Diferencias de presión para ventilación/circulación y concentración para O2/CO2.",
            "Flujo": "Flujo aéreo, sanguíneo y difusión de gases.",
            "Presión": "Presión alveolar, intrapleural, arterial, venosa y capilar.",
            "Resistencia": "Resistencia de vía aérea y resistencia vascular.",
            "Energía": "Trabajo respiratorio y cardíaco para mover gases y fluidos.",
            "Temperatura": "Influye en viscosidad, demanda metabólica y cinética del intercambio.",
            "Membrana": "La membrana alveolocapilar determina la eficiencia de difusión.",
            "Retroalimentación": "Quimiorreceptores ajustan ventilación, frecuencia cardíaca y tono vascular.",
        },
        "variables": {
            "presion": (0, 100, 68, "Gradiente de presión"),
            "resistencia": (0, 100, 34, "Resistencia aérea/vascular"),
            "membrana": (0, 100, 80, "Eficiencia de membrana"),
            "retro": (0, 100, 70, "Respuesta quimiorrefleja"),
        },
        "correct_concepts": ["Presión", "Resistencia", "Membrana"],
    },
    "Endocrino": {
        "emoji": "🧪",
        "subtitle": "Señales químicas, receptores, resistencia periférica y retrocontrol.",
        "mission": "El sistema secreta hormona, pero el tejido blanco responde poco y el eje empieza a oscilar.",
        "goal": "Lograr efecto biológico suficiente con retroalimentación negativa estable.",
        "concept_map": {
            "Gradiente": "Diferencias de concentración hormonal entre glándula, sangre y tejido diana.",
            "Flujo": "Transporte hormonal por circulación y cascadas intracelulares.",
            "Presión": "Papel indirecto; el flujo sanguíneo condiciona la entrega hormonal.",
            "Resistencia": "Disminución de respuesta del tejido blanco ante una señal disponible.",
            "Energía": "Síntesis, secreción y transducción consumen energía.",
            "Temperatura": "Modula cinética enzimática, afinidad y tasa metabólica.",
            "Membrana": "Receptores de membrana y transportadores definen respuesta celular.",
            "Retroalimentación": "Control negativo de ejes; evita oscilaciones excesivas.",
        },
        "variables": {
            "secrecion": (0, 100, 70, "Secreción hormonal"),
            "receptores": (0, 100, 74, "Disponibilidad de receptores"),
            "resistencia": (0, 100, 32, "Resistencia periférica"),
            "retro": (0, 100, 78, "Retroalimentación negativa"),
        },
        "correct_concepts": ["Resistencia", "Membrana", "Retroalimentación"],
    },
    "Vestibulococlear": {
        "emoji": "👂",
        "subtitle": "Ondas, fluidos, membranas, gradientes iónicos y estabilización sensorial.",
        "mission": "Tras un giro rápido, aparece conflicto sensorial: la mirada no se estabiliza y aumenta la sensación de mareo.",
        "goal": "Mejorar orientación estable mediante señal vestibular, integración visual y menor retardo correctivo.",
        "concept_map": {
            "Gradiente": "Gradientes iónicos entre endolinfa y perilinfa; diferencias de aceleración/frecuencia.",
            "Flujo": "Desplazamiento de endolinfa y transmisión de ondas mecánicas.",
            "Presión": "Ondas de presión sonora y desplazamientos hidráulicos.",
            "Resistencia": "Resistencia viscosa del fluido y mecánica de membranas/células ciliadas.",
            "Energía": "Conversión de energía mecánica en señal eléctrica neural.",
            "Temperatura": "Cambia viscosidad del fluido y respuesta vestibular.",
            "Membrana": "Membrana basilar, tectoria y estructuras sensoriales transducen señal.",
            "Retroalimentación": "Reflejo vestibuloocular y ajustes posturales estabilizan mirada y equilibrio.",
        },
        "variables": {
            "presion": (0, 100, 62, "Energía mecánica/presión"),
            "flujo": (0, 100, 60, "Flujo de endolinfa"),
            "membrana": (0, 100, 78, "Sensibilidad de membrana"),
            "retardo": (0, 100, 28, "Retardo correctivo"),
        },
        "correct_concepts": ["Flujo", "Membrana", "Retroalimentación"],
    },
}

# -----------------------------
# SVG anatómicos originales
# -----------------------------

def svg_system(system: str, values: Dict[str, float]) -> str:
    """Devuelve un SVG original, esquemático y anatómico-funcional."""
    blue = "#2563eb"
    cyan = "#06b6d4"
    green = "#22c55e"
    red = "#ef4444"
    amber = "#f59e0b"
    violet = "#8b5cf6"
    slate = "#334155"

    if system == "Musculoesquelético":
        activation = values.get("activacion", 60)
        stiffness = values.get("rigidez", 40)
        temp = values.get("temperatura", 34)
        prop = values.get("propiocepcion", 70)
        muscle_w = 175 + activation * 0.9 - stiffness * 0.45
        heat = 18 + (temp - 20) * 3.5
        return f"""
        <svg viewBox='0 0 720 430' xmlns='http://www.w3.org/2000/svg'>
          <defs>
            <linearGradient id='bone' x1='0' x2='1'><stop stop-color='#e2e8f0'/><stop offset='1' stop-color='#cbd5e1'/></linearGradient>
            <linearGradient id='muscle' x1='0' x2='1'><stop stop-color='#fb923c'/><stop offset='1' stop-color='#ef4444'/></linearGradient>
          </defs>
          <rect width='720' height='430' rx='28' fill='#f8fbff'/>
          <text x='34' y='42' fill='{slate}' font-size='24' font-weight='800'>Sistema musculoesquelético</text>
          <rect x='70' y='202' width='190' height='30' rx='15' fill='url(#bone)' stroke='#94a3b8'/>
          <rect x='460' y='202' width='190' height='30' rx='15' fill='url(#bone)' stroke='#94a3b8'/>
          <circle cx='360' cy='217' r='48' fill='#dbeafe' stroke='{blue}' stroke-width='5'/>
          <path d='M250 217 C 310 150, 410 150, 470 217 C 410 284, 310 284, 250 217 Z' fill='url(#muscle)' opacity='.88'/>
          <rect x='285' y='185' width='{max(80, muscle_w):.0f}' height='64' rx='32' fill='#dc2626' opacity='.75'/>
          <path d='M360 92 L360 157' stroke='{blue}' stroke-width='9' stroke-linecap='round'/>
          <polygon points='360,166 342,138 378,138' fill='{blue}'/>
          <text x='380' y='117' fill='{blue}' font-size='18' font-weight='700'>activación neural</text>
          <path d='M604 118 C 540 145, 505 166, 472 206' stroke='{red}' stroke-width='{6 + stiffness/15:.1f}' fill='none' stroke-linecap='round'/>
          <text x='505' y='100' fill='#991b1b' font-size='18' font-weight='700'>resistencia</text>
          <circle cx='110' cy='340' r='{heat:.0f}' fill='{amber}' opacity='.28'/>
          <circle cx='110' cy='340' r='26' fill='{amber}' opacity='.85'/>
          <text x='150' y='348' fill='#92400e' font-size='17' font-weight='700'>temperatura funcional</text>
          <path d='M215 326 C 280 {300-prop*.35:.0f}, 430 {300-prop*.35:.0f}, 505 326' stroke='{green}' stroke-width='8' fill='none' stroke-linecap='round'/>
          <text x='285' y='383' fill='#166534' font-size='17' font-weight='700'>retroalimentación propioceptiva</text>
        </svg>"""

    if system == "Neuromuscular":
        grad = values.get("gradiente", 75)
        membrane = values.get("membrana", 80)
        resist = values.get("resistencia", 25)
        temp = values.get("temperatura", 36)
        pulse = 10 + grad * 0.18
        syn = max(18, 95 - resist * 0.65)
        return f"""
        <svg viewBox='0 0 720 430' xmlns='http://www.w3.org/2000/svg'>
          <rect width='720' height='430' rx='28' fill='#f8fbff'/>
          <text x='34' y='42' fill='{slate}' font-size='24' font-weight='800'>Sistema neuromuscular</text>
          <circle cx='112' cy='205' r='52' fill='#ddd6fe' stroke='{violet}' stroke-width='5'/>
          <path d='M160 205 C 245 125, 315 125, 385 205 S 520 285, 610 205' stroke='{violet}' stroke-width='18' fill='none' stroke-linecap='round'/>
          <rect x='555' y='165' width='105' height='80' rx='24' fill='#fed7aa' stroke='#fb923c' stroke-width='5'/>
          <line x1='520' y1='144' x2='520' y2='266' stroke='#94a3b8' stroke-width='4' stroke-dasharray='8 8'/>
          <circle cx='230' cy='157' r='{pulse:.1f}' fill='{green}' opacity='.75'/>
          <circle cx='330' cy='204' r='{pulse:.1f}' fill='{green}' opacity='.75'/>
          <circle cx='440' cy='247' r='{pulse:.1f}' fill='{green}' opacity='.75'/>
          <rect x='48' y='316' width='{membrane*2.1:.0f}' height='19' rx='9' fill='{cyan}'/>
          <text x='48' y='304' fill='#0369a1' font-size='17' font-weight='700'>integridad de membrana</text>
          <rect x='495' y='315' width='{syn:.0f}' height='19' rx='9' fill='{red}'/>
          <text x='495' y='304' fill='#991b1b' font-size='17' font-weight='700'>resistencia sináptica</text>
          <circle cx='610' cy='92' r='{18+(temp-20)*.9:.0f}' fill='{amber}' opacity='.55'/>
          <text x='517' y='96' fill='#92400e' font-size='17' font-weight='700'>temperatura</text>
        </svg>"""

    if system == "Cardiopulmonar":
        pressure = values.get("presion", 65)
        resistance = values.get("resistencia", 35)
        membrane = values.get("membrana", 80)
        retro = values.get("retro", 70)
        flow_w = max(8, 9 + pressure * .18 - resistance * .08)
        airway = max(10, 34 - resistance * .18)
        return f"""
        <svg viewBox='0 0 720 430' xmlns='http://www.w3.org/2000/svg'>
          <rect width='720' height='430' rx='28' fill='#f8fbff'/>
          <text x='34' y='42' fill='{slate}' font-size='24' font-weight='800'>Sistema cardiopulmonar</text>
          <path d='M275 110 C 190 60, 110 114, 120 220 C 127 315, 215 345, 285 284 Z' fill='#bfdbfe' stroke='{blue}' stroke-width='5'/>
          <path d='M445 110 C 530 60, 610 114, 600 220 C 593 315, 505 345, 435 284 Z' fill='#bfdbfe' stroke='{blue}' stroke-width='5'/>
          <ellipse cx='360' cy='245' rx='62' ry='82' fill='#fecaca' stroke='{red}' stroke-width='5'/>
          <path d='M360 88 L360 204' stroke='#64748b' stroke-width='{airway:.1f}' stroke-linecap='round'/>
          <path d='M360 170 C 310 185, 285 210, 245 245' stroke='{cyan}' stroke-width='{flow_w:.1f}' fill='none' stroke-linecap='round'/>
          <path d='M360 170 C 410 185, 435 210, 475 245' stroke='{cyan}' stroke-width='{flow_w:.1f}' fill='none' stroke-linecap='round'/>
          <path d='M307 252 C 335 210, 385 210, 413 252' stroke='{red}' stroke-width='12' fill='none' stroke-linecap='round'/>
          <rect x='70' y='342' width='{membrane*2.2:.0f}' height='20' rx='10' fill='{green}'/>
          <text x='70' y='330' fill='#166534' font-size='17' font-weight='700'>membrana alveolocapilar</text>
          <path d='M560 96 C 604 {96+retro*.25:.0f}, 610 {160+retro*.15:.0f}, 560 204' stroke='{amber}' stroke-width='7' fill='none' stroke-linecap='round'/>
          <text x='495' y='82' fill='#92400e' font-size='17' font-weight='700'>retrocontrol</text>
        </svg>"""

    if system == "Endocrino":
        secretion = values.get("secrecion", 70)
        receptors = values.get("receptores", 74)
        resistance = values.get("resistencia", 32)
        retro = values.get("retro", 78)
        dots = int(max(4, secretion / 8))
        circles = "".join([f"<circle cx='{190+i*24}' cy='{210 + ((i%2)*18)}' r='8' fill='{violet}' opacity='.82'/>" for i in range(dots)])
        return f"""
        <svg viewBox='0 0 720 430' xmlns='http://www.w3.org/2000/svg'>
          <rect width='720' height='430' rx='28' fill='#f8fbff'/>
          <text x='34' y='42' fill='{slate}' font-size='24' font-weight='800'>Sistema endocrino</text>
          <rect x='70' y='150' width='118' height='120' rx='32' fill='#fbcfe8' stroke='#db2777' stroke-width='5'/>
          <text x='88' y='136' fill='#9d174d' font-size='18' font-weight='800'>glándula</text>
          <rect x='186' y='207' width='350' height='28' rx='14' fill='#fee2e2' stroke='#fca5a5'/>
          {circles}
          <rect x='535' y='145' width='125' height='135' rx='34' fill='#dbeafe' stroke='{blue}' stroke-width='5'/>
          <rect x='560' y='175' width='{receptors:.0f}' height='16' rx='8' fill='{green}'/>
          <rect x='560' y='218' width='{resistance:.0f}' height='16' rx='8' fill='{red}'/>
          <text x='558' y='166' fill='#166534' font-size='16' font-weight='700'>receptores</text>
          <text x='558' y='211' fill='#991b1b' font-size='16' font-weight='700'>resistencia</text>
          <path d='M600 300 C 520 {350-retro*.25:.0f}, 210 {350-retro*.25:.0f}, 130 286' stroke='{green}' stroke-width='8' fill='none' stroke-linecap='round'/>
          <text x='238' y='382' fill='#166534' font-size='17' font-weight='700'>retroalimentación negativa</text>
        </svg>"""

    # Vestibulococlear
    pressure = values.get("presion", 62)
    flow = values.get("flujo", 60)
    membrane = values.get("membrana", 78)
    delay = values.get("retardo", 28)
    wave = 24 + pressure * .25
    flow_w = 5 + flow * .08
    return f"""
    <svg viewBox='0 0 720 430' xmlns='http://www.w3.org/2000/svg'>
      <rect width='720' height='430' rx='28' fill='#f8fbff'/>
      <text x='34' y='42' fill='{slate}' font-size='24' font-weight='800'>Sistema vestibulococlear</text>
      <path d='M78 210 C 126 {210-wave:.0f}, 174 {210+wave:.0f}, 222 210 S 318 {210-wave:.0f}, 366 210' stroke='{cyan}' stroke-width='7' fill='none' stroke-linecap='round'/>
      <text x='80' y='160' fill='#0369a1' font-size='17' font-weight='700'>onda de presión</text>
      <circle cx='475' cy='215' r='92' fill='#dbeafe' stroke='{blue}' stroke-width='6'/>
      <path d='M427 215 C 442 162, 510 162, 525 215 C 510 268, 442 268, 427 215' fill='none' stroke='{violet}' stroke-width='{flow_w:.1f}' stroke-linecap='round'/>
      <rect x='560' y='166' width='36' height='98' rx='18' fill='{amber}'/>
      <line x1='578' y1='166' x2='578' y2='110' stroke='{amber}' stroke-width='7' stroke-linecap='round'/>
      <circle cx='578' cy='98' r='{14+membrane*.08:.1f}' fill='{green}' opacity='.9'/>
      <text x='526' y='318' fill='#6d28d9' font-size='17' font-weight='700'>flujo de endolinfa</text>
      <path d='M612 96 C 660 {96+delay*.45:.0f}, 660 {175+delay*.25:.0f}, 612 245' stroke='{red}' stroke-width='6' fill='none' stroke-dasharray='9 8'/>
      <text x='598' y='78' fill='#991b1b' font-size='17' font-weight='700'>retardo</text>
    </svg>"""


def compute_results(system: str, v: Dict[str, float]) -> Dict[str, float | str | List[str]]:
    if system == "Musculoesquelético":
        fuerza = 0.68 * v["activacion"] - 0.32 * v["rigidez"] + 1.1 * (v["temperatura"] - 25)
        estabilidad = 0.48 * v["propiocepcion"] + 0.25 * v["activacion"] - 0.36 * v["rigidez"] + 25
        sobrecarga = 22 + 0.58 * v["rigidez"] + 0.20 * v["activacion"] - 0.38 * v["propiocepcion"]
        score = clamp((fuerza + estabilidad + (100 - sobrecarga)) / 3)
        explanation = "La fuerza útil aumenta con activación neural y temperatura funcional, pero cae si la rigidez/resistencia mecánica consume demasiada energía. La propiocepción mejora la estabilidad porque convierte información sensorial en correcciones motoras."
    elif system == "Neuromuscular":
        conduccion = 0.44 * v["gradiente"] + 0.35 * v["membrana"] - 0.35 * v["resistencia"] + 0.85 * (v["temperatura"] - 20)
        transmision = 0.50 * v["gradiente"] + 0.38 * v["membrana"] - 0.55 * v["resistencia"] + 12
        sobrecarga = 18 + 0.45 * v["resistencia"] - 0.18 * v["membrana"]
        score = clamp((conduccion + transmision + (100 - sobrecarga)) / 3)
        fuerza = conduccion
        estabilidad = transmision
        explanation = "El sistema depende de gradientes iónicos y membranas excitables. Si aumenta la resistencia sináptica, el flujo de información baja aunque el nervio tenga señal disponible."
    elif system == "Cardiopulmonar":
        flujo = 1.05 * v["presion"] - 0.62 * v["resistencia"] + 18
        intercambio = 0.42 * v["membrana"] + 0.32 * v["presion"] - 0.26 * v["resistencia"] + 16
        trabajo = 20 + 0.45 * v["presion"] + 0.38 * v["resistencia"] - 0.22 * v["retro"]
        score = clamp((flujo + intercambio + (100 - trabajo)) / 3)
        fuerza = flujo
        estabilidad = intercambio
        sobrecarga = trabajo
        explanation = "El gradiente de presión impulsa aire y sangre, pero la resistencia puede neutralizar ese beneficio. La membrana alveolocapilar determina si el flujo se transforma en intercambio gaseoso útil."
    elif system == "Endocrino":
        señal = 0.42 * v["secrecion"] + 0.40 * v["receptores"] - 0.55 * v["resistencia"] + 18
        control = 0.55 * v["retro"] + 0.25 * v["receptores"] - 0.30 * v["resistencia"] + 18
        oscilacion = 30 + 0.45 * v["resistencia"] - 0.38 * v["retro"]
        score = clamp((señal + control + (100 - oscilacion)) / 3)
        fuerza = señal
        estabilidad = control
        sobrecarga = oscilacion
        explanation = "La secreción hormonal no garantiza efecto biológico. El tejido debe tener receptores disponibles y baja resistencia periférica; la retroalimentación negativa evita oscilaciones del eje."
    else:
        transduccion = 0.35 * v["presion"] + 0.32 * v["flujo"] + 0.42 * v["membrana"] - 0.28 * v["retardo"]
        orientacion = 0.36 * v["flujo"] + 0.34 * v["membrana"] + 0.20 * v["presion"] - 0.45 * v["retardo"] + 22
        mareo = 25 + 0.58 * v["retardo"] - 0.20 * v["flujo"] - 0.16 * v["membrana"]
        score = clamp((transduccion + orientacion + (100 - mareo)) / 3)
        fuerza = transduccion
        estabilidad = orientacion
        sobrecarga = mareo
        explanation = "La señal nace por conversión mecanoeléctrica: presión y flujo desplazan membranas sensoriales. Si el retardo correctivo aumenta, la retroalimentación sensoriomotora llega tarde y aparece inestabilidad."

    return {
        "indicador_1": clamp(fuerza),
        "indicador_2": clamp(estabilidad),
        "riesgo": clamp(sobrecarga),
        "score": clamp(score),
        "estado": state_label(score),
        "explanation": explanation,
    }


def clamp(x: float, lo: float = 0, hi: float = 100) -> float:
    return max(lo, min(hi, float(x)))


def state_label(score: float) -> str:
    if score >= 80:
        return "Sistema estabilizado"
    if score >= 60:
        return "Sistema compensado, pero vulnerable"
    if score >= 40:
        return "Sistema en riesgo de descompensación"
    return "Sistema descompensado"


def badge_class(score: float) -> str:
    if score >= 80:
        return "badge badge-green"
    if score >= 60:
        return "badge badge-amber"
    return "badge badge-red"


def make_report(student: str, group: str, system: str, values: Dict[str, float], concepts: List[str], answer: str, result: Dict) -> str:
    data = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "estudiante": student,
        "grupo": group,
        "sistema": system,
        "mision": SYSTEMS[system]["mission"],
        "objetivo": SYSTEMS[system]["goal"],
        "variables": values,
        "conceptos_elegidos": concepts,
        "puntaje": round(result["score"], 1),
        "estado": result["estado"],
        "explicacion_estudiante": answer,
        "retroalimentacion_automatica": result["explanation"],
    }
    lines = [
        "# Reporte de misión - Código Homeostasis",
        f"Fecha: {data['fecha']}",
        f"Estudiante: {student or 'No registrado'}",
        f"Grupo: {group or 'No registrado'}",
        f"Sistema: {system}",
        "",
        "## Misión",
        data["mision"],
        "",
        "## Objetivo funcional",
        data["objetivo"],
        "",
        "## Variables ajustadas",
    ]
    for k, val in values.items():
        lines.append(f"- {k}: {val}")
    lines += [
        "",
        "## Conceptos seleccionados",
        ", ".join(concepts) if concepts else "Sin selección",
        "",
        "## Resultado",
        f"Puntaje: {data['puntaje']}/100",
        f"Estado: {data['estado']}",
        "",
        "## Explicación del estudiante",
        answer or "Sin respuesta escrita.",
        "",
        "## Retroalimentación automática",
        data["retroalimentacion_automatica"],
        "",
        "## Datos JSON para trazabilidad",
        "```json",
        json.dumps(data, ensure_ascii=False, indent=2),
        "```",
    ]
    return "\n".join(lines)


def concept_score(system: str, chosen: List[str]) -> Tuple[int, List[str]]:
    expected = SYSTEMS[system]["correct_concepts"]
    hits = [c for c in chosen if c in expected]
    return int(round(100 * len(hits) / len(expected))), expected


def render_metric_cards(result: Dict[str, float | str]) -> None:
    c1, c2, c3, c4 = st.columns(4)
    cards = [
        (c1, "Indicador funcional 1", f"{result['indicador_1']:.1f}%"),
        (c2, "Indicador funcional 2", f"{result['indicador_2']:.1f}%"),
        (c3, "Riesgo/costo fisiológico", f"{result['riesgo']:.1f}%"),
        (c4, "Puntaje de misión", f"{result['score']:.1f}/100"),
    ]
    for col, label, value in cards:
        col.markdown(f"<div class='metric-card'><small>{label}</small><strong>{value}</strong></div>", unsafe_allow_html=True)

# -----------------------------
# Interfaz
# -----------------------------

st.markdown(
    """
    <div class='hero-card'>
      <h1>🧬 Código Homeostasis</h1>
      <p>Juego serio para aprender sistemas humanos desde la física: gradiente, flujo, presión, resistencia, energía, temperatura, membrana y retroalimentación.</p>
      <p>La misión no es memorizar órganos: es estabilizar sistemas vivos usando razonamiento físico.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.title("Panel del jugador")
    student = st.text_input("Nombre del estudiante", placeholder="Ej.: Laura Pérez")
    group = st.text_input("Grupo", placeholder="Ej.: Fisioterapia 2A")
    st.divider()
    system = st.radio(
        "Selecciona un sistema",
        list(SYSTEMS.keys()),
        format_func=lambda x: f"{SYSTEMS[x]['emoji']} {x}",
    )
    st.divider()
    mode = st.radio("Modo", ["Misión", "Mapa de conceptos", "Comparador transversal"], index=0)

system_data = SYSTEMS[system]
st.markdown(
    f"""
    <div class='card'>
      <h2>{system_data['emoji']} {escape(system)}</h2>
      <p><strong>{escape(system_data['subtitle'])}</strong></p>
      <span class='badge'>Gradiente</span><span class='badge'>Flujo</span><span class='badge'>Presión</span><span class='badge'>Resistencia</span>
      <span class='badge'>Energía</span><span class='badge'>Temperatura</span><span class='badge'>Membrana</span><span class='badge'>Retroalimentación</span>
    </div>
    """,
    unsafe_allow_html=True,
)

if mode == "Mapa de conceptos":
    st.subheader("Mapa biofísico del sistema")
    cols = st.columns(2)
    items = list(system_data["concept_map"].items())
    for idx, (concept, desc) in enumerate(items):
        with cols[idx % 2]:
            st.markdown(f"<div class='card'><div class='step-label'>{concept}</div>{desc}</div>", unsafe_allow_html=True)

elif mode == "Comparador transversal":
    st.subheader("El mismo concepto cambia de significado según el sistema")
    selected_concept = st.selectbox("Concepto transversal", list(CONCEPTS.keys()))
    st.markdown(f"<div class='feedback'><strong>{selected_concept}:</strong> {CONCEPTS[selected_concept]}</div>", unsafe_allow_html=True)
    st.write("")
    for sys_name, sys_data in SYSTEMS.items():
        st.markdown(
            f"<div class='card'><strong>{sys_data['emoji']} {sys_name}</strong><br>{sys_data['concept_map'][selected_concept]}</div>",
            unsafe_allow_html=True,
        )

else:
    st.subheader("Misión activa")
    st.markdown(
        f"<div class='case-box'><strong>Caso:</strong> {escape(system_data['mission'])}<br><br><strong>Objetivo:</strong> {escape(system_data['goal'])}</div>",
        unsafe_allow_html=True,
    )
    st.write("")

    left, right = st.columns([1.1, 0.9], gap="large")

    values: Dict[str, float] = {}
    with right:
        st.markdown("### Ajusta las variables del sistema")
        for key, (lo, hi, default, label) in system_data["variables"].items():
            values[key] = st.slider(label, min_value=lo, max_value=hi, value=default, step=1)

        chosen_concepts = st.multiselect(
            "¿Qué conceptos físicos explican mejor esta misión?",
            list(CONCEPTS.keys()),
            default=system_data["correct_concepts"][:2],
        )
        student_answer = st.text_area(
            "Explicación breve del estudiante",
            placeholder="Explica qué se mueve, qué lo impulsa, qué se opone y cómo se regula.",
            height=130,
        )

    result = compute_results(system, values)

    with left:
        st.markdown("<div class='svg-wrap'>" + svg_system(system, values) + "</div>", unsafe_allow_html=True)

    st.write("")
    render_metric_cards(result)
    st.write("")

    cscore, expected = concept_score(system, chosen_concepts)
    state_html = f"<span class='{badge_class(result['score'])}'>{result['estado']}</span>"
    st.markdown(
        f"<div class='feedback'>{state_html}<br><br><strong>Retroalimentación:</strong> {result['explanation']}<br><br>"
        f"<strong>Precisión conceptual:</strong> {cscore}/100. Conceptos esperados para esta misión: {', '.join(expected)}.</div>",
        unsafe_allow_html=True,
    )

    report = make_report(student, group, system, values, chosen_concepts, student_answer, result)
    st.download_button(
        "📥 Descargar reporte de misión (.md)",
        data=report.encode("utf-8"),
        file_name=f"reporte_codigo_homeostasis_{system.lower().replace('é','e').replace(' ','_')}.md",
        mime="text/markdown",
        use_container_width=True,
    )

    with st.expander("Ver rúbrica rápida de evaluación"):
        st.markdown(
            """
            | Criterio | Puntaje sugerido |
            |---|---:|
            | Identifica el sistema y el problema funcional | 20 |
            | Reconoce los conceptos físicos dominantes | 25 |
            | Ajusta variables sin descompensar el sistema | 25 |
            | Explica causa-efecto con lenguaje biofísico | 20 |
            | Propone una analogía o transferencia clínica | 10 |
            """
        )

st.caption("Imágenes anatómicas esquemáticas generadas como SVG originales dentro de la aplicación. No usan atlas ni material protegido por derechos de autor.")
