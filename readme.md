# Sistema de Gestão de Linha de Autocarros

Projeto final da unidade curricular de **Algoritmos e Estruturas de Dados**,
Licenciatura em Engenharia Informática.

**Docente:** Catarina Cruz
**Ano Letivo:** 2025/2026
**Data de entrega:** 8 de junho de 2026

**Grupo:**
- Caio Rosa (Nº 160173003)
- Lucélia Ferreira (Nº 240001227)
- Nadine Jeremias (Nº 240001501)

---

## Execução

### Requisitos
- Python 3.11 ou superior
- Dependências em `requirements.txt`

### Instalação
```bash
pip install -r requirements.txt
```

### Executar o programa
```bash
python -m src.main
```

### Executar a suite de testes
```bash
python -m pytest -v
```

### Executar o *benchmark* dos algoritmos de ordenação
```bash
python -m src.algoritmos.benchmark
```

Imprime tabela comparativa no terminal e guarda o gráfico em
`relatorio/imagens/benchmark_ordenacao.png`.

---

## Estrutura

```
projeto_aed/
├── ESPECIFICACAO.md          # Documento técnico
├── README.md                 # Este ficheiro
├── requirements.txt
├── pytest.ini
├── src/
│   ├── estruturas/           # Estruturas de dados (Fase 1)
│   │   ├── no.py             # Nó genérico
│   │   ├── lista_ligada.py   # Lista ligada simples
│   │   ├── fila.py           # Fila FIFO
│   │   └── grafo.py          # Grafo (lista de adjacência)
│   ├── dominio/              # Entidades de negócio (Fase 2)
│   │   ├── passageiro.py     # Passageiro (imutável)
│   │   ├── paragem.py        # Paragem (fachada sobre Fila)
│   │   ├── autocarro.py      # Autocarro (capacidade + posição)
│   │   └── linha.py          # Linha (sequência + construção do grafo)
│   ├── algoritmos/           # Algoritmos (Fase 3)
│   │   ├── ordenacao.py      # Bubble, Insertion, Selection Sort
│   │   ├── pesquisa.py       # BFS sobre grafo
│   │   └── benchmark.py      # Comparação empírica dos algoritmos
│   ├── simulacao/            # Motor de simulação (Fase 4)
│   │   └── simulador.py      # Simulador de movimento do autocarro
│   ├── interface/            # Interface CLI (Fase 4)
│   │   ├── menu.py           # Menu textual em português
│   │   └── visualizacao.py   # Visualização topológica
│   └── main.py               # Ponto de entrada
├── relatorio/
│   └── imagens/
│       └── benchmark_ordenacao.png
└── testes/
    ├── test_lista_ligada.py
    ├── test_fila.py
    ├── test_grafo.py
    ├── test_passageiro.py
    ├── test_paragem.py
    ├── test_autocarro.py
    ├── test_linha.py
    ├── test_ordenacao.py
    ├── test_pesquisa.py
    ├── test_benchmark.py
    ├── test_simulador.py
    └── test_menu.py
```

---

## Demonstração completa do menu

Esta secção apresenta um guião passo a passo que percorre todas as
funcionalidades do sistema. O cenário simula uma linha real de
autocarro que atravessa Salvaterra de Magos, Foros de Salvaterra,
Glória do Ribatejo, Benavente e Samora Correia, com os elementos do
grupo (Caio, Lucélia e Nadine) entre os passageiros.

Para reproduzir, execute `python -m src.main` e introduza as entradas
indicadas. As respostas esperadas do programa estão registadas em
caixas de saída.

### Passo 1 — Criar a linha de autocarro

Escolha a opção **1** no menu. O sistema pedirá o nome da linha e a
capacidade do autocarro.

```
> Escolha uma opção: 1
> Nome da linha: Linha 421
> Capacidade do autocarro: 4
  Linha 'Linha 421' criada com autocarro de capacidade 4.
```

A capacidade foi deliberadamente mantida em 4 para que, mais à frente,
um dos passageiros fique em espera por falta de lugar — demonstrando o
tratamento correto da lotação esgotada.

### Passo 2 — Adicionar as cinco paragens

Repita a opção **2** para cada paragem, pela ordem do percurso.

```
> Escolha uma opção: 2
> Nome da nova paragem: Salvaterra de Magos
  Paragem 'Salvaterra de Magos' adicionada ao fim da linha.

> Escolha uma opção: 2
> Nome da nova paragem: Foros de Salvaterra
  Paragem 'Foros de Salvaterra' adicionada ao fim da linha.

> Escolha uma opção: 2
> Nome da nova paragem: Glória do Ribatejo
  Paragem 'Glória do Ribatejo' adicionada ao fim da linha.

> Escolha uma opção: 2
> Nome da nova paragem: Benavente
  Paragem 'Benavente' adicionada ao fim da linha.

> Escolha uma opção: 2
> Nome da nova paragem: Samora Correia
  Paragem 'Samora Correia' adicionada ao fim da linha.
```

### Passo 3 — Mostrar o estado da linha

A opção **7** permite verificar o percurso construído.

```
> Escolha uma opção: 7
  Linha: Linha 421
  Número de paragens: 5
  Autocarro: lotação 0/4, posição: -
  Percurso:
    - Salvaterra de Magos       (0 em espera)
    - Foros de Salvaterra       (0 em espera)
    - Glória do Ribatejo        (0 em espera)
    - Benavente                 (0 em espera)
    - Samora Correia            (0 em espera)
```

O autocarro encontra-se ainda fora da linha (posição "-"), pois não
foi efetuada nenhuma simulação.

### Passo 4 — Adicionar passageiros às paragens

A opção **4** permite adicionar um passageiro à fila de uma paragem
existente. Note-se que dois passageiros são adicionados a Salvaterra
de Magos: o Caio entra primeiro na fila, a Lucélia em seguida — a
disciplina FIFO garantirá que o Caio embarcará primeiro.

```
> Escolha uma opção: 4
> Nome da paragem: Salvaterra de Magos
> Nome do passageiro: Caio
  Passageiro 'Caio' adicionado à fila de 'Salvaterra de Magos' (agora 1 em espera).

> Escolha uma opção: 4
> Nome da paragem: Salvaterra de Magos
> Nome do passageiro: Lucélia
  Passageiro 'Lucélia' adicionado à fila de 'Salvaterra de Magos' (agora 2 em espera).

> Escolha uma opção: 4
> Nome da paragem: Foros de Salvaterra
> Nome do passageiro: Nadine
  Passageiro 'Nadine' adicionado à fila de 'Foros de Salvaterra' (agora 1 em espera).

> Escolha uma opção: 4
> Nome da paragem: Benavente
> Nome do passageiro: Ana
  Passageiro 'Ana' adicionado à fila de 'Benavente' (agora 1 em espera).

> Escolha uma opção: 4
> Nome da paragem: Benavente
> Nome do passageiro: Bruno
  Passageiro 'Bruno' adicionado à fila de 'Benavente' (agora 2 em espera).
```

### Passo 5 — Ordenar as paragens pelo número de passageiros

A opção **6** permite escolher um critério de ordenação (por nome ou
por número de passageiros, decrescente) e um dos três algoritmos
implementados. Aqui ordenamos por número de passageiros, com
**Insertion Sort**.

```
> Escolha uma opção: 6
  Critério:
    1) por nome
    2) por número de passageiros (decrescente)
  Escolha: 2
  Algoritmo:
    1) Bubble Sort
    2) Insertion Sort
    3) Selection Sort
  Escolha: 2
  Resultado:
    Salvaterra de Magos       (2 em espera)
    Benavente                 (2 em espera)
    Foros de Salvaterra       (1 em espera)
    Glória do Ribatejo        (0 em espera)
    Samora Correia            (0 em espera)
```

Observe-se a propriedade da **estabilidade** do Insertion Sort:
Salvaterra e Benavente têm ambas dois passageiros em espera; como
Salvaterra foi inserida primeiro na linha, mantém-se à frente.

### Passo 6 — Simular o percurso completo

A opção **5** faz o autocarro avançar uma paragem, com desembarque de
quem entrou primeiro e embarque do primeiro em espera (até à
capacidade do autocarro). Repete-se cinco vezes para percorrer toda a
linha.

```
> Escolha uma opção: 5
  [CHEGADA] Chegada a Salvaterra de Magos (a bordo: 0/4; em espera: 2)
  [       ] Ninguém para desembarcar em Salvaterra de Magos
  [SOBE   ] Caio embarcou em Salvaterra de Magos

> Escolha uma opção: 5
  [CHEGADA] Chegada a Foros de Salvaterra (a bordo: 1/4; em espera: 1)
  [DESCE  ] Caio desceu em Foros de Salvaterra
  [SOBE   ] Nadine embarcou em Foros de Salvaterra

> Escolha uma opção: 5
  [CHEGADA] Chegada a Glória do Ribatejo (a bordo: 1/4; em espera: 0)
  [DESCE  ] Nadine desceu em Glória do Ribatejo
  [       ] Ninguém em espera em Glória do Ribatejo

> Escolha uma opção: 5
  [CHEGADA] Chegada a Benavente (a bordo: 0/4; em espera: 2)
  [       ] Ninguém para desembarcar em Benavente
  [SOBE   ] Ana embarcou em Benavente

> Escolha uma opção: 5
  [CHEGADA] Chegada a Samora Correia (a bordo: 1/4; em espera: 0)
  [DESCE  ] Ana desceu em Samora Correia
  [       ] Ninguém em espera em Samora Correia
```

Pontos a destacar nesta simulação:
- Em Salvaterra de Magos sobe o **Caio** (o primeiro a chegar), mas a
  **Lucélia** fica em espera, pois a política de embarque é de um
  passageiro por chegada (requisito do enunciado).
- Em Foros de Salvaterra, o **Caio** desce (primeiro a entrar é o
  primeiro a sair) e entra a **Nadine**, demonstrando a disciplina
  FIFO no autocarro.
- Em Benavente, embarca a **Ana** (que chegou primeiro); o **Bruno**
  permanece em espera, ilustrando a gestão da fila ao longo do tempo.

### Passo 7 — Calcular o percurso entre duas paragens (BFS)

A opção **8** invoca o algoritmo de pesquisa em largura sobre o grafo
da rede, devolvendo o caminho com menor número de arestas.

```
> Escolha uma opção: 8
> Paragem de origem: Salvaterra de Magos
> Paragem de destino: Samora Correia
  Caminho (4 arestas):
    Salvaterra de Magos -> Foros de Salvaterra -> Glória do Ribatejo -> Benavente -> Samora Correia
```

### Passo 8 — Comparar os algoritmos de ordenação (extra)

A opção **9** executa o módulo de *benchmark*, que aplica os três
algoritmos a entradas crescentes (50, 100, 250, 500, 1000 e 2000
elementos) em três cenários (aleatório, já ordenado, ordem inversa),
imprime a tabela de tempos e guarda o gráfico comparativo em
`relatorio/imagens/benchmark_ordenacao.png`.

```
> Escolha uma opção: 9
  A executar comparação (pode demorar alguns segundos)...
  Cenário: Aleatório
       n         Bubble Sort      Insertion Sort      Selection Sort
  ------------------------------------------------------------------
      50      0.18 ±  0.04 ms      0.08 ±  0.02 ms      0.14 ±  0.07 ms
     ...
    2000    304.35 ± 10.69 ms    118.16 ±  2.21 ms    161.35 ±  1.88 ms

  Gráfico guardado em: relatorio/imagens/benchmark_ordenacao.png
```

### Passo 9 — Sair

A opção **0** encerra o programa.

```
> Escolha uma opção: 0
  Até à próxima.
```

---

## Estado de Progresso

| Fase | Estado |
|---|---|
| 0 — Especificação técnica | ✅ Concluída |
| 1 — Estruturas de dados | ✅ Concluída |
| 2 — Modelo de domínio | ✅ Concluída |
| 3 — Algoritmos | ✅ Concluída |
| 4 — Simulação e CLI | ✅ Concluída |
| 5 — Extras | ✅ Concluída parcialmente (*benchmark* concluído; visualização topológica como trabalho futuro) |
| 6 — Relatório | ✅ Concluído |

**Cobertura de testes:** 100%