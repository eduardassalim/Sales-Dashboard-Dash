# Importa o framework Dash para criação de aplicações web interativas
import dash

# Importa componentes principais do Dash:
# dcc (Dash Core Components) e html (componentes HTML)
# Input e Output são usados para callbacks (reatividade)
from dash import dcc, html, Input, Output

# Bibliotecas de visualização
import plotly.express as px
import plotly.graph_objects as go

# Manipulação de dados
import pandas as pd
import numpy as np

# Manipulação de datas
from datetime import datetime, timedelta

# Geração de dados aleatórios
import random


# ── Dataset fictício ───────────────────────────────────────────────────────────

# Define sementes para reprodutibilidade (mesmos dados a cada execução)
random.seed(42)
np.random.seed(42)

# Listas de domínio (categorias)
produtos    = ["Notebook Pro", "Fone BT", "Teclado Mec.", "Monitor 4K", "Webcam HD", "Mouse Gamer"]
regioes     = ["Sul", "Sudeste", "Nordeste", "Centro-Oeste", "Norte"]
vendedores  = ["Ana Lima", "Bruno Melo", "Carla Dias", "Diego Reis", "Eva Nunes"]

# Gera um intervalo de datas diário ao longo de 2024
datas = pd.date_range(start="2024-01-01", end="2024-12-31", freq="D")

# Número de registros simulados
n = 900

# Criação do DataFrame com amostragem aleatória
df = pd.DataFrame({
    "data":      np.random.choice(datas, n),  # datas aleatórias
    "produto":   np.random.choice(produtos, n, p=[0.25, 0.20, 0.15, 0.18, 0.12, 0.10]),  # distribuição não uniforme
    "regiao":    np.random.choice(regioes,  n, p=[0.15, 0.35, 0.25, 0.15, 0.10]),
    "vendedor":  np.random.choice(vendedores, n),
    "qtd":       np.random.randint(1, 15, n),  # quantidade vendida
})

# Dicionário de preços por produto
precos = {
    "Notebook Pro": 3800,
    "Fone BT": 350,
    "Teclado Mec.": 480,
    "Monitor 4K": 2200,
    "Webcam HD": 280,
    "Mouse Gamer": 190
}

# Mapeia preço unitário
df["preco_unit"] = df["produto"].map(precos)

# Calcula receita total por linha
df["receita"] = df["qtd"] * df["preco_unit"]

# Cria coluna de mês (normalizada)
df["mes"] = df["data"].dt.to_period("M").dt.to_timestamp()

# Nome do mês formatado
df["mes_nome"] = df["data"].dt.strftime("%b/%Y")

# Cria coluna de trimestre (T1, T2, ...)
df["trimestre"] = "T" + df["data"].dt.quarter.astype(str)

# Ordena por data
df = df.sort_values("data").reset_index(drop=True)


# ── App ────────────────────────────────────────────────────────────────────────

# Inicializa aplicação Dash
app = dash.Dash(__name__, title="Sales Dashboard · 2024")


# ── Definição de tema (cores e estilo) ──
DARK   = "#0d1117"
PANEL  = "#161b22"
BORDER = "#21262d"
ACCENT = "#58a6ff"
GREEN  = "#3fb950"
AMBER  = "#d29922"
RED    = "#f85149"
TEXT   = "#e6edf3"
MUTED  = "#8b949e"
FONT   = "JetBrains Mono, Consolas, monospace"


# Função que cria um card de KPI
def kpi_card(title, value, delta=None, color=GREEN):

    # Elemento opcional de variação (delta)
    delta_el = html.Div(delta, style={
        "fontSize": "12px",
        "color": color,
        "marginTop": "4px",
        "fontFamily": FONT
    }) if delta else None

    # Estrutura visual do card
    return html.Div([
        html.P(title, style={
            "fontSize": "11px",
            "color": MUTED,
            "margin": "0 0 6px",
            "textTransform": "uppercase",
            "letterSpacing": "0.08em"
        }),
        html.H2(value, style={
            "fontSize": "28px",
            "fontWeight": "500",
            "margin": "0",
            "color": TEXT,
            "fontFamily": FONT
        }),
        delta_el
    ], style={
        "background": PANEL,
        "border": f"1px solid {BORDER}",
        "borderRadius": "8px",
        "padding": "18px 20px",
        "flex": "1",
        "minWidth": "180px"
    })


# Função para rótulos de seção
def section_label(text):
    return html.P(f"// {text}", style={
        "fontSize": "11px",
        "color": ACCENT,
        "textTransform": "uppercase",
        "letterSpacing": "0.1em",
        "margin": "28px 0 12px",
        "fontFamily": FONT
    })


# ── Layout ─────────────────────────────────────────────────────────────────────

# Define a estrutura visual da aplicação
app.layout = html.Div([

    # Barra superior
    html.Div([
        html.Span("> sales.dashboard", style={"color": ACCENT, "fontFamily": FONT}),
        html.Span("2024 · dados fictícios", style={"color": MUTED}),
    ], style={"display": "flex", "justifyContent": "space-between"}),

    # Filtros
    html.Div([
        dcc.Dropdown(id="filtro-regiao",
                     options=[{"label": r, "value": r} for r in ["Todas"] + regioes],
                     value="Todas"),

        dcc.Dropdown(id="filtro-produto",
                     options=[{"label": p, "value": p} for p in ["Todos"] + produtos],
                     value="Todos"),

        dcc.Dropdown(id="filtro-tri",
                     options=[{"label": t, "value": t} for t in ["Todos", "T1", "T2", "T3", "T4"]],
                     value="Todos"),
    ]),

    # Conteúdo principal
    html.Div([

        section_label("kpis"),
        html.Div(id="kpi-row"),

        section_label("receita mensal"),
        html.Div([
            dcc.Graph(id="grafico-mensal"),
            dcc.Graph(id="grafico-produto"),
        ]),

        section_label("performance"),
        html.Div([
            dcc.Graph(id="grafico-regiao"),
            dcc.Graph(id="grafico-vendedores"),
        ]),
    ])
])


# ── Callback ───────────────────────────────────────────────────────────────────

# Define reatividade (entrada → saída)
@app.callback(
    Output("kpi-row", "children"),
    Output("grafico-mensal", "figure"),
    Output("grafico-produto", "figure"),
    Output("grafico-regiao", "figure"),
    Output("grafico-vendedores", "figure"),
    Input("filtro-regiao", "value"),
    Input("filtro-produto", "value"),
    Input("filtro-tri", "value"),
)
def atualizar(regiao, produto, tri):

    # Copia DataFrame
    dff = df.copy()

    # Aplica filtros
    if regiao != "Todas":
        dff = dff[dff["regiao"] == regiao]

    if produto != "Todos":
        dff = dff[dff["produto"] == produto]

    if tri != "Todos":
        dff = dff[dff["trimestre"] == tri]


    # ── KPIs ──

    receita_total = dff["receita"].sum()
    qtd_total = dff["qtd"].sum()
    num_pedidos = len(dff)

    # Evita divisão por zero
    ticket_medio = receita_total / len(dff) if len(dff) > 0 else 0

    # Cria cards
    kpis = html.Div([
        kpi_card("Receita total", f"R$ {receita_total:,.0f}"),
        kpi_card("Pedidos", f"{num_pedidos}"),
        kpi_card("Unidades", f"{qtd_total}"),
        kpi_card("Ticket médio", f"R$ {ticket_medio:,.0f}"),
    ])


    # ── Gráfico mensal ──

    mensal = dff.groupby("mes")["receita"].sum().reset_index()

    fig_mensal = go.Figure()
    fig_mensal.add_trace(go.Scatter(
        x=mensal["mes"],
        y=mensal["receita"],
        mode="lines+markers"
    ))


    # ── Receita por produto ──

    por_prod = dff.groupby("produto")["receita"].sum().reset_index()

    fig_prod = go.Figure(go.Bar(
        x=por_prod["receita"],
        y=por_prod["produto"],
        orientation="h"
    ))


    # ── Receita por região ──

    por_reg = dff.groupby("regiao")["receita"].sum().reset_index()

    fig_reg = go.Figure(go.Bar(
        x=por_reg["regiao"],
        y=por_reg["receita"]
    ))


    # ── Receita por vendedor ──

    por_vend = dff.groupby("vendedor")["receita"].sum().reset_index()

    fig_vend = go.Figure(go.Bar(
        x=por_vend["receita"],
        y=por_vend["vendedor"],
        orientation="h"
    ))


    # Retorna tudo para o frontend
    return kpis, fig_mensal, fig_prod, fig_reg, fig_vend


# ── Execução ───────────────────────────────────────────────────────────────────

# Inicia o servidor local
if __name__ == "__main__":
    app.run(debug=True)
