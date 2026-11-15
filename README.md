# Modelagem e Simulação de Redes de Petri — Mini Escavadeira Didática (ESP32)

Projeto desenvolvido para a disciplina **Informática Aplicada** — Engenharia Civil / Universidade do Estado da Bahia (UNEB).
**Docente:** Prof. Robson Marinho

## Equipe
* **Nícolas da Silva Dórea**
* **Guilherme Pires dos Santos Guimarães**
* **Jezreel Victor Sales Rocha**

---

## Descrição do Sistema
Prototipagem de uma **Mini Escavadeira Didática** controlada por microcontrolador **ESP32**, equipada com **1 sensor ultrassônico HC-SR04** (detecção de material na zona de escavação) e **4 servomotores** responsáveis pelos graus de liberdade do sistema:
1. **Base (Giro da Plataforma)**
2. **Lança (Braço Principal)**
3. **Braço Secundário**
4. **Caçamba (Coleta e Descarga)**

---

## Estrutura do Repositório
* `mini_escavadeira_lt.hps` / `.json`: Modelo da **Rede de Petri Lugar–Transição (Etapa 1)** com 10 lugares ($P_0$ a $P_7$, $PC$, $PO$) e 8 transições ($T_1$ a $T_8$), simulado no Web HP SIM.
* `simulacao_petri_escavadeira.py`: Implementação em Python das matrizes de entrada ($D^-$), saída ($D^+$) e incidência ($C = D^+ - D^-$), verificação algébrica de habilitação e evolução das marcações ($M_0 \rightarrow M_8$).
* `mini_escavadeira_cpn.cpn`: Modelo da **Rede de Petri Colorida — CPN (Etapa 2)** desenvolvido e simulado no CPN Tools 4.0.1, contendo 6 lugares, 4 transições, 3 *colorsets* (`DISTANCIA`, `COMANDO`, `ESTADO_ATUADORES`), 3 variáveis (`d`, `cmd`, `angulos`) e 2 funções ML (`validarColeta` e `calcularPostura`).
* `relatorio_tecnico_petri.md`: Documentação técnica completa das duas etapas.

---

## Como Executar
### 1. Simulação Matricial (Python)
```bash
python simulacao_petri_escavadeira.py
```

### 2. Rede de Petri Colorida (CPN Tools)
1. Abra o **CPN Tools 4.0.1**.
2. Carregue o arquivo `mini_escavadeira_cpn.cpn`.
3. Utilize a ferramenta **Simulation** (*Single Step*) para executar os 4 disparos do ciclo (`T1_Posicionar` $\rightarrow$ `T2_Coletar` $\rightarrow$ `T3_Descarregar` $\rightarrow$ `T4_Retornar`).
