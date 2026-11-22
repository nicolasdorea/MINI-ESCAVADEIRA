# Modelagem Formal por Redes de Petri — Mini Escavadeira Didática

Repositório dedicado à modelagem, análise estrutural e simulação formal do sistema de controle de uma **Mini Escavadeira Didática**, desenvolvido na **Universidade do Estado da Bahia (UNEB)**.

## Equipe

* **Nícolas da Silva Dórea**
* **Guilherme Pires dos Santos Guimarães**
* **Jezreel Victor Sales Rocha**

---

## Visão Geral do Sistema Físico

O protótipo eletromecânico é controlado por um microcontrolador **ESP32** integrado a um sensor ultrassônico **HC-SR04** e a **quatro servomotores** responsáveis pelos graus de liberdade do braço articulado:

1. **Base Giratória ($\theta_{\text{base}}$):** rotação horizontal entre a zona de coleta ($45^\circ$), posição neutra ($90^\circ$) e zona de descarga ($135^\circ$).
2. **Lança Principal ($\theta_{\text{lança}}$):** elevação e abaixamento do segmento primário ($75^\circ$ a $110^\circ$).
3. **Braço Secundário ($\theta_{\text{braço}}$):** extensão e recolhimento do alcance radial ($90^\circ$ a $130^\circ$).
4. **Caçamba ($\theta_{\text{caçamba}}$):** abertura para coleta/descarga ($25^\circ$ a $30^\circ$) e fechamento para retenção de carga ($120^\circ$).

---

## Estrutura do Repositório

```text
├── etapa1_rede_pt/
│   └── mini_escavadeira_pt.hps       # Modelo Lugar-Transição (Web HP SIM)
├── etapa2_cpn_tools/
│   └── mini_escavadeira_cpn.cpn      # Modelo Colorido Expandido (CPN Tools 4.0.1)
├── docs/
│   └── imagens/                      # Capturas de tela das simulações
└── README.md
```

---

## Etapa 1: Rede de Petri Lugar-Transição (P/T)

Modelada inicialmente no ambiente **Web HP SIM** para validar o fluxo sequencial de estados, exclusão mútua e propriedades estruturais básicas do ciclo operacional (Repouso $\rightarrow$ Posicionamento $\rightarrow$ Coleta $\rightarrow$ Descarga $\rightarrow$ Retorno):

* **Vivacidade (*Liveness*):** ausência de bloqueios (*deadlocks*) durante o ciclo nominal.
* **Limitação (*Boundedness*):** rede 1-limitada (segura), garantindo que apenas um estado operacional esteja ativo por vez.
* **Reversibilidade:** capacidade de retornar continuamente à marcação inicial ($M_0$).

---

## Etapa 2: Rede de Petri Colorida (CPN) Expandida

Refinada no **CPN Tools (v4.0.1)** com **8 lugares**, **6 transições** e **14 arcos direcionados**, representando individualmente as posturas angulares dos quatro servomotores por meio da tupla $(\theta_{\text{base}}, \theta_{\text{lança}}, \theta_{\text{braço}}, \theta_{\text{caçamba}})$ e incorporando intertravamento sensorial.

### Declarações Standard ML (SML)

```sml
colset STRING = string;
colset ESTADO_ATUADORES = product INT * INT * INT * INT;
colset COMANDO = string;
colset DISTANCIA = int;

var d : DISTANCIA;
var cmd : COMANDO;
var angulos : ESTADO_ATUADORES;

fun validarColeta(d : DISTANCIA) : bool = (d > 2 andalso d <= 12);

fun posturaMovimento(m : string) : ESTADO_ATUADORES =
  if m = "GIRO_COLETA" then (45, 90, 90, 30)
  else if m = "BAIXAR_LANCA" then (45, 110, 90, 30)
  else if m = "ESTENDER_BRACO" then (45, 110, 130, 30)
  else if m = "FECHAR_CACAMBA" then (45, 110, 130, 120)
  else if m = "ABRIR_CACAMBA" then (135, 75, 100, 25)
  else (90, 90, 90, 30);
```

### Lugares ($P$) e Marcação Inicial ($M_0$)

| Lugar | Color Set | Marcação Inicial ($M_0$) | Descrição Funcional |
| :--- | :--- | :--- | :--- |
| `P_Repouso` | `ESTADO_ATUADORES` | ``1`(90,90,90,30)`` | Posição neutra inicial e final de todos os 4 servomotores. |
| `P_Comando_ESP32` | `COMANDO` | ``1`"START"`` | Sinal de partida emitido pelo microcontrolador ESP32. |
| `P_Base_Coleta` | `ESTADO_ATUADORES` | Vazia | Confirma o giro da base para a área de coleta ($45^\circ$). |
| `P_Sensor_Ultrassonico` | `DISTANCIA` | ``1`8`` | Leitura de distância em centímetros medida pelo sensor HC-SR04. |
| `P_Lanca_Baixada` | `ESTADO_ATUADORES` | Vazia | Indica o abaixamento da lança principal ($110^\circ$). |
| `P_Braco_Estendido` | `ESTADO_ATUADORES` | Vazia | Indica a extensão do braço secundário ($130^\circ$). |
| `P_Carga_Retida` | `ESTADO_ATUADORES` | Vazia | Confirma o fechamento da caçamba ($120^\circ$) com o material retido. |
| `P_Zona_Descarga` | `ESTADO_ATUADORES` | Vazia | Indica o posicionamento na descarga ($135^\circ$) e abertura da caçamba ($25^\circ$). |

### Transições ($T$) e Expressões de Guarda

| Transição | Guarda | Postura Resultante $(\theta_1, \theta_2, \theta_3, \theta_4)$ | Ação Executada |
| :--- | :--- | :--- | :--- |
| `T1_Girar_Coleta` | `[cmd = "START"]` | `(45, 90, 90, 30)` | Inicia o ciclo e rotaciona a base para a zona de coleta. |
| `T2_Aproximar_Lanca` | `[validarColeta(d)]` | `(45, 110, 90, 30)` | Valida $2\text{ cm} < d \le 12\text{ cm}$ e abaixa a lança principal. |
| `T3_Estender_Braco` | — | `(45, 110, 130, 30)` | Estende o braço secundário até o ponto de apreensão. |
| `T4_Fechar_Cacamba` | — | `(45, 110, 130, 120)` | Fecha a caçamba para apreender o objeto. |
| `T5_Descarregar` | — | `(135, 75, 100, 25)` | Gira para a zona de descarte, recolhe lança/braço e abre a caçamba. |
| `T6_Retornar_Repouso` | — | `(90, 90, 90, 30)` | Retorna os quatro servomotores à postura inicial de repouso. |

---

## Como Executar a Simulação (CPN Tools)

1. Abra o **CPN Tools (v4.0.1)** e carregue o arquivo `etapa2_cpn_tools/mini_escavadeira_cpn.cpn`.
2. Aguarde a verificação automática de sintaxe (as abas e o nome do modelo devem ficar sublinhados em verde).
3. Abra a paleta **Simulation** no menu lateral esquerdo:
   * Clique no botão **Single Step** (ícone de triângulo preto com círculo verde) para disparar uma transição por vez e observar a atualização das tuplas de ângulos em cada lugar.
   * Clique em **Rewind** (ícone de dupla seta para a esquerda) para restaurar a marcação inicial ($M_0$).
4. **Teste de Intertravamento de Segurança:** altere a marcação inicial de `P_Sensor_Ultrassonico` para um valor fora da faixa operacional (por exemplo, ``1`25``) e observe que `T2_Aproximar_Lanca` permanece desabilitada pela guarda `[validarColeta(d)]`.