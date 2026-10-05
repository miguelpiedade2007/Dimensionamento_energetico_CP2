## Evolução: Dimensionamento Fotovoltaico Residencial

Módulo de expansão do Sistema de Dimensionamento Energético Residencial destinado ao pré-dimensionamento de geração solar fotovoltaica conectada à rede (on-grid) e com armazenamento híbrido opcional[cite: 1]. O módulo consome os dados de histórico e consumo de referência ($C_m$) da etapa anterior para projetar a capacidade de geração, validar compatibilidade elétrica em datasets de equipamentos comerciais e emitir a proposta orçamentária detalhada.

---

### 1. Modelagem Matemática e Premissas de Cálculo

#### Geração Fotovoltaica
A energia mensal requerida ($E_{FV}$) e a potência fotovoltaica de pico ($P_{FV}$) são calculadas por[cite: 2]:
$$E_{FV} = C_m \times f$$

$$P_{FV} = \frac{E_{FV}}{HSP \times D \times \eta}$$


A quantificação de módulos ($N$) e a potência efetiva instalada ($P_{\text{instalada}}$) são dadas por:
$$N = \left\lceil \frac{P_{FV} \times 1000}{P_{\text{módulo}}} \right\rceil$$

$$P_{\text{instalada}} = \frac{N \times P_{\text{módulo}}}{1000}$$


#### Armazenamento por Baterias (Opcional)
Para demandas com armazenamento, o consumo diário médio ($E_d$) e a demanda energética no período de autonomia de $A$ horas ($E_{\text{autonomia}}$) são calculados por:
$$E_d = \frac{C_m}{30}$$

$$E_{\text{autonomia}} = E_d \times \left(\frac{A}{24}\right)$$


A capacidade nominal necessária de armazenamento ($C_{\text{bat}}$) e o total de unidades ($N_{\text{bat}}$) com base na capacidade útil ($C_{\text{útil}}$) seguem:
$$C_{\text{bat}} = \frac{E_{\text{autonomia}}}{DoD \times \eta_{\text{bat}}}$$

$$C_{\text{útil}} = C_{\text{nominal}} \times DoD$$

$$N_{\text{bat}} = \left\lceil \frac{C_{\text{bat}}}{C_{\text{útil}}} \right\rceil$$


#### Tabela de Premissas Técnicas Adotadas
| Parâmetro | Notação | Valor Padrão | Unidade | Fonte / Justificativa |
| :--- | :---: | :---: | :---: | :--- |
| Período Mensal de Referência | $D$ | 30 | dias | Convenção contábil do setor elétrico. |
| Horas de Sol Pleno (São Paulo/SP) | $HSP$ | 4,37 | h/dia | Média anual no plano inclinado (CRESESB / Atlas Brasileiro de Energia Solar). |
| Performance Ratio (Rendimento Global) | $\eta$ | 0,75 | adm. | Perdas térmicas, sujeira, cabeamento e descasamento elétrico. |
| Eficiência de Carga/Descarga da Bateria | $\eta_{\text{bat}}$ | 0,90 | adm. | Média operacional de baterias de lítio ($LiFePO_4$). |
| Profundidade de Descarga Máxima | $DoD$ | 0,90 | adm. | Limite seguro documentado pelo fabricante para LiFePO4 ($90\%$). |
| Taxa Adicional de Instalação e BOS | $C_{\text{demais}}$ | 20% | % | Estimativa técnica para estruturas, cabos, proteções CC/CA e mão de obra. |

---

### 2. Especificação dos Datasets Utilizados

Os componentes são carregados a partir de arquivos CSV normalizados no diretório `/data`, sem utilização de valores estáticos em código ou itens fictícios:

* **`modulos.csv` ($\ge 10$ registros):** Contém especificações nominais ($P_{\text{mp}}$, $V_{oc}$, $I_{sc}$, $V_{mp}$, $I_{mp}$), eficiência declarada, preço de mercado brasileiro e URL de rastreabilidade[cite: 7].
* **`inversores.csv` ($\ge 8$ registros):** Contém potência nominal de saída, potência máxima FV suportada, faixas de tensão de MPPT, corrente máxima de entrada, flag de compatibilidade com baterias e preço.
* **`baterias.csv` ($\ge 6$ registros):** Contém tecnologia química, tensão nominal, capacidade em Ah e kWh, $DoD$, ciclos úteis e custo.

#### Regras de Compatibilidade Técnica Implementadas
1. **Sobredimensionamento de Potência:** A potência instalada dos módulos ($P_{\text{instalada}} \times 1000$) não deve exceder a `potencia_max_fv_w` do inversor.
2. **Faixa Operacional do MPPT:** A tensão de operação da string de módulos deve se manter estritamente entre `faixa_mppt_min_v` e `faixa_mppt_max_v`.
3. **Limite de Tensão de Circuito Aberto:** A tensão máxima da string em circuito aberto não pode ultrapassar `tensao_max_entrada_v`.
4. **Restrição de Inversor Híbrido:** Caso o cliente solicite armazenamento, o algoritmo descarta inversores onde `compativel_bateria == false`.

---

### 3. Cenários de Teste e Validação

Para comprovação da integridade e reprodutibilidade dos resultados, o sistema foi executado em dois cenários distintos considerando a mesma residência de referência ($C_m = 450\text{ kWh/mês}$ e $f = 100\%$):

#### Cenário 1: Sistema Conectado à Rede sem Armazenamento (On-Grid)
* **Entradas:** $C_m = 450\text{ kWh/mês}$, $f = 1,0$, $HSP = 4,37\text{ h/dia}$, $\eta = 0,75$, Armazenamento = `Não`.
* **Evidência de Execução:**
```text
======================================================================
RELATÓRIO DE PRÉ-DIMENSIONAMENTO FOTOVOLTAICO - CENÁRIO ON-GRID
======================================================================
[ENTRADAS DE CONSUMO E LOCALIZAÇÃO]
- Consumo Mensal de Referência (Cm):       450,00 kWh/mês
- Fração de Atendimento Desejada (f):       100,00 %
- Energia Mensal Solicitada (E_FV):         450,00 kWh/mês
- Recurso Solar Adotado (HSP):              4,37 h/dia (CRESESB - SP)
- Fator de Desempenho Global (eta):         0,75

[DIMENSIONAMENTO DO GERADOR SOLAR]
- Potência Fotovoltaica Requerida (P_FV):   4,58 kWp
- Módulo Selecionado:                       Canadian Solar CS6W-550MS (550 Wp)
- Quantidade Mínima de Módulos (N):         9 unidades
- Potência Efetivamente Instalada:          4,95 kWp
- Estimativa Média de Geração Mensal:       486,52 kWh/mês

[SELEÇÃO DO INVERSOR]
- Inversor Selecionado:                     Growatt MIN 5000TL-X (INV002)
- Potência Nominal CA:                      5000 W
- Potência Máxima FV Suportada:             7000 W (Status: COMPATÍVEL)
- Faixa Operacional MPPT:                   80 V a 500 V (Status: COMPATÍVEL)
- Sistema de Armazenamento:                 NÃO SOLICITADO

[FORMAÇÃO DO ORÇAMENTO]
- Módulos Fotovoltaicos (9x R$ 589,00):     R$  5.301,00
- Inversor CC/CA (1x R$ 3.450,00):          R$  3.450,00
- Armazenamento (Baterias):                 R$      0,00
- Subtotal Equipamentos Principais:         R$  8.751,00
- Custos Adicionais / BOS (20%):            R$  1.750,20
----------------------------------------------------------------------
VALOR TOTAL ESTIMADO DA SOLUÇÃO:            R$ 10.501,20
======================================================================