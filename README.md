# 📊 Sales Dashboard · 2024

Dashboard interativo desenvolvido com **Dash** e **Plotly** para análise de vendas a partir de um dataset fictício. O projeto simula um cenário real de business intelligence com filtros dinâmicos e visualizações analíticas.

---

## 🚀 Visão Geral

Este projeto implementa um dashboard web que permite:

* Filtrar dados por **região**, **produto** e **trimestre**
* Visualizar métricas agregadas (KPIs)
* Analisar receita ao longo do tempo
* Comparar desempenho por produto, região e vendedor

O sistema utiliza dados simulados para demonstrar práticas comuns de análise de dados e construção de interfaces analíticas.

---

## 🧱 Arquitetura

A aplicação segue o modelo reativo do **Dash**, baseado em:

* **Layout declarativo** (componentes HTML + gráficos)
* **Callbacks** (funções reativas que atualizam a interface)
* **Pipeline de dados** (transformações com Pandas)

Fluxo simplificado:

```
Entrada (Dropdowns) → Callback → Processamento (Pandas) → Visualização (Plotly)
```

---

## 📁 Estrutura do Código

### 1. Geração de Dados

* Dataset sintético criado com `numpy` e `pandas`
* Distribuições não uniformes simulam cenários reais
* Variáveis principais:

  * `produto`
  * `regiao`
  * `vendedor`
  * `qtd` (quantidade)
  * `receita`

Transformações importantes:

* Cálculo de receita (`qtd × preço`)
* Extração de mês e trimestre
* Ordenação temporal

---

### 2. Layout

Definido com componentes do Dash:

* `html.Div`: estrutura geral
* `dcc.Dropdown`: filtros interativos
* `dcc.Graph`: gráficos Plotly

Seções principais:

* Navbar
* Filtros
* KPIs
* Gráficos analíticos

---

### 3. KPIs

Indicadores principais:

* **Receita total**
* **Número de pedidos**
* **Unidades vendidas**
* **Ticket médio**

Implementados via função reutilizável `kpi_card()`.

---

### 4. Callback (Lógica Reativa)

A função `atualizar()`:

* Recebe filtros como entrada
* Filtra o DataFrame
* Calcula métricas
* Gera gráficos
* Retorna componentes atualizados

Entradas:

```python
Input("filtro-regiao", "value")
Input("filtro-produto", "value")
Input("filtro-tri", "value")
```

Saídas:

* KPIs
* 4 gráficos

---

### 5. Visualizações

#### 📈 Receita Mensal

* Série temporal
* Linha com marcadores
* Área preenchida

#### 📊 Receita por Produto

* Gráfico de barras horizontal
* Ordenado por valor

#### 🌎 Receita por Região

* Destaque automático da maior região

#### 🧑‍💼 Top Vendedores

* Ranking por receita
* Escala de cor proporcional

---

## 🎨 Design

Tema inspirado em interfaces de desenvolvimento:

* Fundo escuro (dark mode)
* Tipografia monoespaçada
* Paleta:

  * Azul (destaque)
  * Verde (positivo)
  * Amarelo (neutro)
  * Vermelho (alerta)

---

## ▶️ Como Executar

### 1. Instalar dependências

```bash
pip install dash plotly pandas numpy
```

### 2. Rodar aplicação

```bash
python app.py
```

### 3. Acessar no navegador

```
http://127.0.0.1:8050
```

---

## 📌 Possíveis Extensões

* Integração com banco de dados real
* Deploy (Render / Railway / Docker)
* Autenticação de usuários
* Exportação de relatórios
* Uso de dados em tempo real (streaming)

---

## 🧠 Decisões Técnicas

Esta seção documenta escolhas de arquitetura e implementação com foco em clareza, desempenho e escalabilidade.

### 1. Uso de Dataset Sintético

A geração controlada de dados com `numpy` e `random` permite:

* Reprodutibilidade (via seed)
* Controle de distribuição (simulação de cenários reais)
* Independência de fontes externas

Essa abordagem é comum em prototipagem e validação de dashboards antes da integração com dados reais.

---

### 2. Escolha do Dash

O Dash foi utilizado por integrar:

* Backend (Python)
* Frontend (componentes declarativos)
* Sistema reativo nativo (callbacks)

Alternativas como React + API exigiriam maior complexidade de setup.

---

### 3. Modelo Reativo (Callbacks)

A aplicação segue o paradigma de programação reativa:

* Inputs (Dropdowns) disparam atualizações
* A função `atualizar()` centraliza a lógica
* Outputs são renderizados automaticamente

Vantagem: evita manipulação manual de estado e DOM.

---

### 4. Uso de Pandas para Transformação

Operações como:

* `groupby`
* agregações (`sum`)
* filtragem condicional

foram escolhidas por sua eficiência e legibilidade.

Essa decisão segue práticas consolidadas em análise de dados (cf. McKinney, *Python for Data Analysis*).

---

### 5. Plotly Graph Objects vs Express

Foi adotado `plotly.graph_objects` em vez de `plotly.express` para:

* Maior controle visual
* Customização fina de layout
* Consistência estética entre gráficos

---

### 6. Separação de Responsabilidades

O código é organizado em:

* Geração de dados
* Definição de layout
* Lógica (callback)
* Funções auxiliares (ex: `kpi_card`)

Isso melhora:

* Manutenção
* Reuso
* Legibilidade

---

### 7. Tratamento de Edge Cases

Exemplo:

* Evita divisão por zero no cálculo de ticket médio

```python
ticket_medio = receita_total / len(dff) if len(dff) > 0 else 0
```

---

### 8. Design System

A definição de constantes de cor e tipografia permite:

* Consistência visual
* Facilidade de alteração global
* Aproximação de um design system

---

### 9. Performance

* Uso de `df.copy()` evita efeitos colaterais
* Filtragem incremental reduz custo computacional
* Dataset em memória (adequado para protótipos)

Para produção, seria recomendável:

* Cache de consultas
* Paginação ou agregação prévia
* Uso de banco de dados

---

### 10. Escalabilidade

O projeto pode evoluir para:

* Arquitetura modular (separação em múltiplos arquivos)
* Integração com APIs
* Deploy em ambiente cloud

---

## 📚 Conceitos Aplicados

* Programação reativa
* Data visualization
* Agregação de dados (groupby)
* UX para dashboards
* Separação entre dados, lógica e apresentação

---

## ⚠️ Observação

Os dados utilizados são **fictícios** e foram gerados apenas para fins educacionais.

---

## 👩‍💻 Autoria

Projeto desenvolvido para fins de estudo e portfólio em Ciência de Dados.
