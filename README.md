# Modelado cualitativo de la retinosis pigmentaria mediante un circuito RLC en Simulink

**Modelado de Sistemas Fisiológicos — Proyecto final**
Departamento de Ingeniería Eléctrica y Electrónica · Ingeniería Biomédica
Tecnológico Nacional de México, campus Tijuana

**Profesor:** Dr. Paul Antonio Valle Trujillo
**Fecha de la bitácora:** 19 de noviembre de 2026

## Integrantes

| Nombre | Número de control |
|---|---|
| De La Cruz Bojorquez Kevin Dario | 20210777 |
| Del Toro Nuñez Eduardo | C23212399 |
| Rodriguez Padilla Kevin | 22210428 |

---

## Tabla de contenido

1. [Descripción del proyecto](#1-descripción-del-proyecto)
2. [Sistema fisiológico y enfermedad](#2-sistema-fisiológico-y-enfermedad)
3. [Circuito y analogía fisiológica](#3-circuito-y-analogía-fisiológica)
4. [Parámetros: control vs. caso](#4-parámetros-control-vs-caso)
5. [Señal de entrada](#5-señal-de-entrada)
6. [Análisis matemático](#6-análisis-matemático)
7. [Resultados de la simulación](#7-resultados-de-la-simulación)
8. [Limitaciones](#8-limitaciones)
9. [Conclusiones](#9-conclusiones)
10. [Estructura del repositorio](#10-estructura-del-repositorio)
11. [Cómo reproducir la simulación](#11-cómo-reproducir-la-simulación)
12. [Referencias](#12-referencias)

---

## 1. Descripción del proyecto

Este proyecto modela de forma **cualitativa** la respuesta eléctrica de un fotorreceptor de la retina y compara dos escenarios:

- **Control:** individuo sano.
- **Caso:** individuo con **retinosis pigmentaria**.

Se utiliza un circuito RLC construido en **Simulink**. Los valores de los componentes se eligieron de forma **heurística** para obtener salidas distintas entre control y caso, manteniendo la misma topología. Además del modelo, se desarrolló el **análisis matemático completo** del circuito (ecuaciones integro-diferenciales, función de transferencia, polos y error en estado estable).

Metas del proyecto:

1. Seleccionar el sistema fisiológico y la enfermedad: sistema nervioso y sensorial, retinosis en los fotorreceptores.
2. Construir el circuito y diferenciar los valores para el control y para el caso.
3. Utilizar un LLM para justificar el tipo de señal de entrada y realizar la analogía entre el circuito y el sistema fisiológico, diferenciando entre el individuo sano y el enfermo.

> **Aviso:** el modelo es didáctico. Los valores de los componentes son heurísticos, no mediciones, y obtener respuestas distintas entre control y caso **no demuestra** que el circuito reproduzca la enfermedad.

---

## 2. Sistema fisiológico y enfermedad

### Funcionamiento normal

En el sistema sensorial visual, los fotorreceptores (bastones y conos) transducen la luz en una señal eléctrica. En oscuridad, los canales activados por GMPc del segmento externo permanecen abiertos y generan la *corriente oscura*, que mantiene la célula relativamente despolarizada. Un fotón activa la rodopsina, la transducina y la fosfodiesterasa PDE6; la hidrólisis de GMPc cierra los canales y la célula se hiperpolariza de forma graduada, lo que reduce la liberación de glutamato. El segmento interno aporta la maquinaria metabólica, los canales de K⁺ y la corriente I<sub>h</sub> (HCN), activada por hiperpolarización, que acorta y modela la respuesta. Ambos segmentos se comunican por el cilio conector.

### Proceso representado

El circuito representa la **respuesta de voltaje de un fotorreceptor** (segmentos externo e interno) ante un **cambio sostenido de iluminación**. Esta es una suposición del modelo.

### Enfermedad: retinosis pigmentaria

Grupo de distrofias hereditarias de la retina. Degenera primero el bastón (ceguera nocturna, pérdida del campo periférico) y después el cono (pérdida de agudeza). Hay acortamiento de los segmentos externos, pérdida celular y un electrorretinograma con amplitud reducida y tiempos implícitos prolongados. Funcionalmente cabe esperar menor fotocorriente, menor sensibilidad y alteración de la membrana del fotorreceptor superviviente.

---

## 3. Circuito y analogía fisiológica

**Topología:** la fuente V<sub>e</sub> va en serie con R<sub>o</sub>; el primer nodo tiene C<sub>o</sub> a tierra; R<sub>c</sub> en serie; y el nodo de salida V<sub>s</sub> tiene C<sub>i</sub>, R<sub>i</sub> y la rama serie R<sub>h</sub>–L<sub>h</sub> en paralelo a tierra.

> 📌 *Agregar aquí la imagen del circuito de Simulink, por ejemplo:* `![Circuito](img/circuito.png)`

| Componente | Función en el circuito | Correspondencia fisiológica | Tipo de justificación |
|---|---|---|---|
| **V<sub>e</sub>** | Fuente de voltaje (escalón) | Estímulo luminoso efectivo | Didáctica: la luz modula una conductancia, no es una fuente de voltaje |
| **R<sub>o</sub>** | Resistencia serie de entrada | Resistencia efectiva del segmento externo (canales CNG abiertos) | Biofísica: la conductancia de canales es el análogo de 1/R |
| **C<sub>o</sub>** | Filtro pasa-bajas en el primer nodo | Capacitancia de membrana del segmento externo | Biofísica: la bicapa lipídica se comporta como capacitor; C ∝ área de membrana |
| **R<sub>c</sub>** | Resistencia serie entre nodos | Acoplamiento externo–interno (cilio conector) | Fenomenológica: valor eléctrico no medido |
| **C<sub>i</sub>** | Segundo filtro pasa-bajas | Capacitancia del segmento interno | Biofísica, igual que C<sub>o</sub> |
| **R<sub>i</sub>** | Fuga a tierra | Conductancia de fuga y de K⁺ del segmento interno | Biofísica: determina la resistencia de entrada |
| **R<sub>h</sub>–L<sub>h</sub>** | Rama abierta en alta frecuencia y en cortocircuito en CD | Corriente I<sub>h</sub> (HCN) y otras corrientes lentas dependientes de voltaje | Fenomenológica: la inductancia es un linealizado de una cinética lenta; no hay bobina real |
| **Tierra** | Referencia | Medio extracelular | Convención |
| **V<sub>s</sub>** | Voltaje del nodo final | Respuesta de voltaje normalizada del segmento interno | Didáctica: no es un mV real; la polaridad es opuesta a la hiperpolarización real |

---

## 4. Parámetros: control vs. caso

Todos los componentes cambian y la topología se conserva.

| Parámetro | Control | Caso | Efecto eléctrico / relación con la enfermedad | ¿Razonable? |
|---|---|---|---|---|
| R<sub>o</sub> | 470 Ω | 820 Ω | Mayor caída serie y menor ganancia; menos canales abiertos y menor fotocorriente | Sí, cualitativamente |
| C<sub>o</sub> | 10 nF | 6.8 nF | Menos membrana por acortamiento del segmento externo | Sí, es el cambio mejor fundamentado |
| R<sub>c</sub> | 47 Ω | 100 Ω | Mayor atenuación y retardo de acople externo–interno | Plausible, pero especulativo |
| C<sub>i</sub> | 22 nF | 15 nF | Reducción del área del segmento interno por degeneración | Sí |
| R<sub>i</sub> | 1 kΩ | 680 Ω | Más fuga: baja la ganancia y la resistencia de entrada | Plausible en una célula dañada o despolarizada |
| R<sub>h</sub> | 1.5 kΩ | 1.8 kΩ | Cambia I<sub>h</sub> | Sin sustento claro |
| L<sub>h</sub> | 150 mH | 180 mH | Cambia I<sub>h</sub>; la razón L<sub>h</sub>/R<sub>h</sub> se mantiene en 100 µs | Sin sustento claro |

---

## 5. Señal de entrada

| Señal | Ventajas | Limitaciones |
|---|---|---|
| **Escalón** ✅ | Análogo a luz sostenida; revela ganancia, transitorio y establecimiento | No muestra recuperación tras el estímulo |
| Pulso finito | Evalúa recuperación; semejante a un destello | Menos directo para la ganancia estática |
| Sinusoidal | Da la respuesta en frecuencia | Poco natural como estímulo visual |
| Rampa | Prueba seguimiento | Crece sin límite; sin análogo fisiológico claro |
| Pseudoaleatoria | Identificación de sistemas | Difícil de interpretar en un curso introductorio |

Se seleccionó el **escalón** por su correspondencia con la iluminación sostenida:

```
Ve(t) = A · u(t − t0),   A = 1 (normalizada),   t0 = 0.1 ms
```

Se simula de 0 a 1 ms (≈ 11 τ<sub>L</sub>). La amplitud es normalizada y la escala temporal del modelo (decenas de µs) es mucho más rápida que la de un fotorreceptor real (decenas a cientos de ms), por lo que se requeriría un reescalamiento temporal.

---

## 6. Análisis matemático

El desarrollo completo (a mano) está en [`docs/Analisis_Matemático_Completo.pdf`](docs/Analisis_Matem%C3%A1tico_Completo.pdf). Aquí se resume.

### 6.1 Ecuaciones integro-diferenciales (método de mallas)

Se definen cuatro corrientes de malla I₁, I₂, I₃ e I₄. Para cada elemento:

| Elemento | Ecuación |
|---|---|
| R<sub>o</sub> | v<sub>Ro</sub>(t) = R<sub>o</sub> · i₁(t) |
| C<sub>o</sub> | v<sub>Co</sub>(t) = (1/C<sub>o</sub>) ∫ (i₁ − i₂) dt |
| R<sub>c</sub> | v<sub>Rc</sub>(t) = R<sub>c</sub> · i₂(t) |
| C<sub>i</sub> | v<sub>Ci</sub>(t) = (1/C<sub>i</sub>) ∫ (i₂ − i₃) dt |
| R<sub>i</sub> | v<sub>Ri</sub>(t) = R<sub>i</sub> · (i₃ − i₄) |
| R<sub>h</sub> | v<sub>Rh</sub>(t) = R<sub>h</sub> · i₄(t) |
| L<sub>h</sub> | v<sub>Lh</sub>(t) = L<sub>h</sub> · di₄/dt |

**Malla 1:**

```
i₁(t) = (1/Ro) · [ Ve(t) − (1/Co)∫i₁ dt + (1/Co)∫i₂ dt ]
```

**Malla 2:**

```
i₂(t) = (1/Rc) · [ (1/Co)∫i₁ dt + (1/Ci)∫i₃ dt − (1/Ci + 1/Co)∫i₂ dt ]
```

**Malla 3:**

```
i₃(t) = i₄(t) + (1/(Ri·Ci)) · [ ∫i₂ dt − ∫i₃ dt ]
```

**Malla 4:**

```
i₄(t) = (1/(Ri + Rh)) · [ Ri·i₃(t) − Lh · di₄/dt ]
```

**Ecuación de salida:**

```
Vs(t) = Rh·i₄(t) + Lh · di₄/dt = Ri · (i₃(t) − i₄(t))
```

### 6.2 Transformada de Laplace y función de transferencia

Aplicando Laplace a las cuatro mallas y despejando sucesivamente I₃, I₂ e I₁ en términos de I₄, se obtiene:

```
Vs(s) = (Rh + s·Lh) · I₄(s)

          Ri · (Lh·s + Rh)
H(s) = ─────────────────────
               D(s)
```

donde **D(s)** es un polinomio de tercer orden:

```
D(s) = Co·Ci·Ro·Rc·Ri·Lh · s³  +  [ … ] · s²  +  [ … ] · s  +  [ Ro·Rh + Ro·Ri + Rc·Rh + Rc·Ri + Ri·Rh ]
```

> Los coeficientes completos de s² y s se encuentran en el PDF del análisis matemático.

### 6.3 Error en estado estable

Para una entrada escalón unitario:

```
e = lim(s→0) (1/s)·(s − H(s))  =  1 − G_CD

G_CD = Ri·Rh / (Ro·Rh + Ro·Ri + Rc·Rh + Rc·Ri + Ri·Rh)
```

| | Ganancia estática G<sub>CD</sub> | Error en estado estable |
|---|---|---|
| **Control** | 0.537 | 0.463 |
| **Caso** | 0.349 | 0.651 |

### 6.4 Polos del sistema

Calculados con Python (rad/s):

| Polo | Control | Caso |
|---|---|---|
| p₁ | −12 612.4 | −12 411.5 |
| p₂ | −93 250.5 | −120 381.5 |
| p₃ | −3 257 135.2 | −2 291 841.2 |

Todos los polos tienen parte real negativa, por lo que el sistema es **estable** en ambos escenarios. El polo dominante (el más cercano al origen) corresponde a la relajación lenta asociada al inductor.

### 6.5 Constantes de tiempo y ganancias analíticas

Con R<sub>p</sub> = R<sub>i</sub> ∥ R<sub>h</sub> (en CD el inductor es un corto):

| | G<sub>CD</sub> | G₀ (inductor abierto) | τ<sub>L</sub> (µs) |
|---|---|---|---|
| Control | 0.537 | 0.659 | 82 |
| Caso | 0.349 | 0.425 | 82 |

```
G0  = Ri / (Ro + Rc + Ri)
τL ≈ Lh / (Rh + Ri ∥ (Ro + Rc))
```

Estos valores son cálculos analíticos y coinciden con las mesetas de la simulación (≈ 0.535 y ≈ 0.35).

---

## 7. Resultados de la simulación

> 📌 *Agregar aquí la gráfica de Simulink, por ejemplo:* `![Respuesta al escalón](img/respuesta_escalon.png)`

La gráfica muestra la entrada V<sub>e</sub>(t) (escalón unitario en t = 0.1 ms), la salida del control y la salida del caso.

| Observación | Control | Caso |
|---|---|---|
| Pico del transitorio (aprox.) | ≈ 0.62 | ≈ 0.40 |
| Meseta (estado estable) | ≈ 0.535 | ≈ 0.35 |
| τ<sub>L</sub> | ≈ 82 µs | ≈ 82 µs |

**Interpretación:**

- **Amplitud:** en el caso la amplitud estática baja ≈ 35 %. Esto es coherente con la menor amplitud del electrorretinograma en la enfermedad, pero no equivale a una validación.
- **Transitorio:** ambas curvas muestran un pico y un descenso hacia la meseta (G₀ > G<sub>CD</sub>), atribuible al inductor y no a oscilaciones sostenidas. Es cualitativamente semejante a la respuesta con meseta de los fotorreceptores moldeada por I<sub>h</sub>.
- **Velocidad:** las constantes RC son similares (R<sub>o</sub>C<sub>o</sub>: 4.7 µs vs. 5.6 µs) y el tiempo de establecimiento es casi el mismo. La diferencia principal es de **amplitud, no de velocidad**, por lo que el modelo no reproduce el retraso del tiempo implícito del electrorretinograma.
- **Desfase y recuperación:** requieren entrada sinusoidal y pulso, respectivamente; no se pueden evaluar con el escalón.

---

## 8. Limitaciones

- El circuito es **lineal e invariante en el tiempo**.
- I<sub>h</sub> se aproxima de forma fenomenológica con la rama R<sub>h</sub>–L<sub>h</sub>.
- No se representan la cascada de fototransducción (adaptación y no linealidad), la dependencia de Ca²⁺, la cinética de canales, la heterogeneidad celular, el acople con células horizontales y bipolares, el metabolismo ni la muerte celular progresiva.
- No se distingue entre bastones y conos.
- La fuente de voltaje y la polaridad son didácticas.
- Los parámetros son heurísticos y falta validación con datos experimentales.

---

## 9. Conclusiones

- El circuito se relaciona de forma razonable con la membrana del fotorreceptor en los elementos R y C; R<sub>c</sub> y la rama R<sub>h</sub>–L<sub>h</sub> son aproximaciones fenomenológicas.
- Los cambios en R<sub>o</sub>, C<sub>o</sub>, C<sub>i</sub> y R<sub>i</sub> producen una atenuación coherente con la menor respuesta en la retinosis pigmentaria.
- Los cambios en R<sub>h</sub> y L<sub>h</sub> no tienen justificación firme y mantienen τ<sub>L</sub> casi igual, por lo que el modelo captura el cambio de amplitud pero no el retardo.
- Como mejora, se recomienda ajustar R<sub>c</sub>, C<sub>o</sub> o C<sub>i</sub> para lograr mayor lentitud y completar el análisis con un pulso.

---

## 10. Estructura del repositorio

> Ajustar según los archivos que se vayan subiendo.

```
.
├── README.md
├── docs/
│   ├── Proyecto_00_Bitacora.pdf           # Reporte entregado
│   └── Analisis_Matemático_Completo.pdf   # Ecuaciones, H(s), polos y error
├── simulink/                              # (pendiente) modelo .slx
├── scripts/                               # (pendiente) scripts de Python/MATLAB
└── img/                                   # (pendiente) circuito y gráficas
```

---

## 11. Cómo reproducir la simulación

> 📌 *Pendiente: completar cuando se suba el archivo de Simulink.*

1. Abrir el modelo en MATLAB/Simulink (versión: *por definir*).
2. Cargar los valores de la tabla de parámetros para **control** o **caso**.
3. Configurar la entrada como escalón unitario con t₀ = 0.1 ms y simular de 0 a 1 ms.
4. Comparar V<sub>s</sub>(t) del control y del caso.

---

## 12. Referencias

- Hartong, D. T., Berson, E. L., & Dryja, T. P. (2006). Retinitis pigmentosa. *The Lancet, 368*(9549), 1795–1809. https://doi.org/10.1016/S0140-6736(06)69740-7
- Kandel, E. R., Koester, J. D., Mack, S. H., & Siegelbaum, S. A. (Eds.). (2021). *Principles of neural science* (6th ed.). McGraw-Hill.
- Mauro, A., Conti, F., Dodge, F., & Schor, R. (1970). Subthreshold behavior and phenomenological impedance of the squid giant axon. *The Journal of General Physiology, 55*(4), 497–523. https://doi.org/10.1085/jgp.55.4.497
- Sothilingam, V., Michalakis, S., Garcia Garrido, M., Biel, M., Tanimoto, N., & Seeliger, M. W. (2016). HCN1 channels enhance rod system responsivity in the retina under conditions of light exposure. *PLOS ONE, 11*(1), e0147728. https://doi.org/10.1371/journal.pone.0147728
- Yau, K.-W., & Hardie, R. C. (2009). Phototransduction motifs and variations. *Cell, 139*(2), 246–264. https://doi.org/10.1016/j.cell.2009.09.029
