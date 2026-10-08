# job-hunter

> Un skill de [Claude Code](https://claude.com/claude-code) que actúa como
> tu **head hunter personal**: prepara tu CV, busca vacantes con análisis
> honesto de compatibilidad, y te asiste para postularte — con verificación
> real en el navegador.

---

## ¿Qué es esto?

`job-hunter` es un skill para Claude Code. Una vez instalado, convierte a
Claude en un reclutador senior que trabaja **para ti**, no para la empresa.
Te dice lo que no quieres oír cuando tu CV o una vacante lo justifican, y
documenta su recomendación — aunque la decisión final siempre sea tuya.

Funciona en **3 fases**, cada una con puntos de aprobación explícitos antes
de avanzar:

```
┌─────────────────────────────────────────────────────────────┐
│  FASE 1            FASE 2              FASE 3               │
│  Preparar CV  ──►  Buscar vacantes ──► Postularse           │
│                                                             │
│  Diagnóstico       Análisis match      Formularios          │
│  Reescritura       Lista aprobada      Cover letters        │
│  PDF bilingüe      por el usuario      Registro Excel       │
└─────────────────────────────────────────────────────────────┘
```

---

## Inicio rápido

### 1. Instalar

```bash
git clone https://github.com/spanesso/job-hunter.git .claude/skills/job-hunter
```

Eso es todo. Claude Code detecta el skill automáticamente.

### 2. Requisitos previos

| Requisito | Para qué | Lo instala el skill |
|-----------|----------|-------------|
| [Claude Code](https://claude.com/claude-code) | Correr el skill | — (ver paso 1) |
| Python 3 | Generar los PDFs del CV | El skill corre `pip install` automático |
| Chrome MCP (`claude-in-chrome` o `chrome-devtools`) | Navegar y postularse | El skill detecta cuál tenés |

El skill verifica e instala las dependencias Python automáticamente al
arrancar. Solo hay dos pasos manuales inevitables: instalar Python 3 por
primera vez, y configurar el Chrome MCP la primera vez.

---

#### Instalar Python 3 (solo si no lo tenés)

Abrí una terminal y ejecutá el comando de tu sistema operativo:

```bash
# macOS (con Homebrew)
brew install python3

# macOS (sin Homebrew — descargá el instalador)
# → https://www.python.org/downloads/macos/

# Ubuntu / Debian
sudo apt update && sudo apt install python3 python3-pip

# Windows
# → https://www.python.org/downloads/windows/
# Durante la instalación, marcá "Add Python to PATH"
```

Para verificar que quedó bien: `python3 --version` debe mostrar 3.8 o mayor.

---

#### Instalar el Chrome MCP (solo la primera vez)

Elegí **una** de las dos opciones según lo que prefieras:

**Opción A — `claude-in-chrome` (extensión de Chrome)**

1. Abrí Chrome y andá a `chrome://extensions/`
2. Activá **Modo desarrollador** (arriba a la derecha).
3. Descargá o cloná la extensión desde su repositorio y cargala con
   "Cargar descomprimida".
4. Una vez instalada, hacé click en el ícono de la extensión y autorizá
   el acceso a los sitios donde querés postularte.
5. En tu proyecto, agregá esto en `.mcp.json`:
   ```json
   {
     "mcpServers": {
       "claude-in-chrome": {
         "command": "npx",
         "args": ["-y", "@anthropic-ai/claude-in-chrome-mcp"]
       }
     }
   }
   ```

**Opción B — `chrome-devtools` MCP (vía protocolo DevTools)**

1. Abrí Chrome con el puerto de depuración habilitado:
   ```bash
   # macOS
   open -a "Google Chrome" --args --remote-debugging-port=9222

   # Windows
   chrome.exe --remote-debugging-port=9222

   # Linux
   google-chrome --remote-debugging-port=9222
   ```
2. En tu proyecto, agregá esto en `.mcp.json`:
   ```json
   {
     "mcpServers": {
       "chrome-devtools": {
         "command": "npx",
         "args": ["-y", "@anthropic-ai/mcp-chrome-devtools"],
         "env": { "CHROME_DEBUGGING_PORT": "9222" }
       }
     }
   }
   ```
3. Reiniciá Claude Code — debería detectar Chrome automáticamente.

> El skill corre `scripts/verificar-chrome.sh` al arrancar para confirmar
> que la conexión funciona. Si algo falla, te indica exactamente qué revisar.

---

### 3. Activar

Dentro de una sesión de Claude Code, simplemente escribe:

```
/job-hunter
```

O en lenguaje natural:
```
Ayúdame a mejorar mi CV para buscar trabajo
Busca vacantes de desarrollador iOS senior
Postúlame a esta vacante: https://...
```

---

## Flujo completo paso a paso

### Paso 0 — Idioma de respuesta

Lo primero que hace el skill es preguntarte en qué idioma querés que
responda. Lo recuerda entre sesiones — solo lo pregunta una vez.

---

### Fase 1 — Preparar tu CV

**1.1 Diagnóstico**
Claude analiza tu CV actual (`.docx`, `.pdf` o `.md`) como lo vería un
reclutador en 6 segundos. Te da:
- Probabilidad estimada de pasar filtro ATS (Alta / Media / Baja + razón)
- Lista de problemas de formato y contenido
- Preguntas para completar logros que faltan

> ⛔ No toca nada hasta que vos aprobés el diagnóstico.

**1.2 Reestructuración**
Aplica solo los cambios que aprobaste. Cada logro debe estar respaldado por
algo que confirmaste — no se inventan métricas.

**1.3 Foto de perfil** (opcional)
Si subís una foto, Claude analiza composición y entrega prompts para
generarla con otra herramienta.

**1.4 Diseño**
Elegís uno o más de los 3 diseños:

| Diseño | Cuándo usarlo | Riesgo ATS |
|--------|--------------|------------|
| **A — ATS-First** | Portales (LinkedIn, Indeed, Computrabajo) | Mínimo |
| **B — Balanced** | Envío directo a reclutadores | Bajo |
| **C — Portfolio** | Hiring managers, ferias, impresión | Alto — ⚠️ nunca para portales |

**1.5 Generación y aprobación de PDFs**

El skill genera **siempre dos versiones**:
- CV en tu idioma nativo
- CV en inglés

Ambas se guardan primero en `cv/output/` (borradores). Claude te muestra
la ruta exacta de cada una y pide tu aprobación individual.

> ⚠️ **Hasta que no aprobés los dos PDFs, las Fases 2 y 3 están
> bloqueadas.** Los PDFs aprobados se copian a `cv/aprobados/` — esos
> son los únicos que se envían en postulaciones.

Los CVs generados **no contienen** menciones a Claude, ChatGPT ni ninguna
advertencia de generación por IA, para no ser rechazados por filtros
automáticos.

---

### Fase 2 — Buscar vacantes

**Prerrequisito:** Chrome MCP verificado + PDFs aprobados en `cv/aprobados/`.

**2.0 ¿Qué puesto buscamos hoy?**
Antes de buscar, Claude lee tu CV, extrae tus aptitudes y tecnologías, y
genera una lista de títulos de cargo sugeridos con checkboxes. Vos elegís
uno o varios, y/o escribís el tuyo. Sin confirmación, no hay búsqueda.

**2.1 Configuración**
Define portales, filtros de modalidad/ubicación, y salario objetivo
en **dos monedas**:
- Moneda de tu país (p. ej. 12.500.000 COP/mes)
- USD (p. ej. 4.000 USD/mes)

**2.2 Búsqueda con subagentes (paralela)**
Cada portal se ejecuta en un **subagente fork separado**, en paralelo.
El contexto principal no recibe el tráfico de Chrome — solo el resultado
consolidado. Menos tokens consumidos, misma información útil.
Cada subagente calcula el match real y escribe su resultado en archivos
locales; el agente principal los une y te muestra el resumen.

> ⛔ Vos marcás qué postular y qué descartar antes de continuar.

**Fuentes de búsqueda**: portales web + APIs públicas de Greenhouse, Ashby,
Lever y Recruitee (ofertas vigentes, no enlaces vencidos).

---

### Fase 3 — Postularse

**Prerrequisito:** vacantes aprobadas en Fase 2.

**Modo supervisado** (por defecto): subagente llena → agente principal muestra resumen → vos aprobás → subagente envía.  
**Modo autónomo** (si lo confirmás): subagente llena y envía sin pausa. Máximo 10 por sesión.

**Cada postulación corre en su propio subagente fork** — el contexto
principal solo ve el resultado final (éxito / fallo / campos llenados),
no todo el detalle de la navegación.

Por cada postulación:
1. El subagente navega a la vacante con Chrome MCP.
2. Llena los campos con tu perfil (`perfil.md`).
3. Si pide **cover letter**: lo genera y lo sube como PDF — nunca lo deja vacío.
4. Sube el PDF del CV desde `cv/aprobados/` en el idioma que corresponda.
5. Aplica las **respuestas fijas** automáticamente:
   - WhatsApp / email: **siempre Sí** (para que te puedan contactar)
   - Disponibilidad: el valor que guardaste en `perfil.md`
   - Salario: moneda local o USD según el formulario
6. **Antes de enviar**, detecta si hay un checkbox "I'm not a robot"
   (reCAPTCHA v2). Si lo encuentra, el skill no puede marcarlo — te avisa:

   > ⚠️ **ACCIÓN REQUERIDA — Checkbox "I'm not a robot"**
   > Todo el formulario ya está lleno. Solo falta ese checkbox.
   > Abrí la URL, marcalo, y avisame — yo hago click en Enviar.

   Una vez que confirmás, el skill retoma y envía. Si preferís omitir
   esa vacante, queda guardada como `pendiente_captcha` para después.
7. Confirma con captura que el envío fue exitoso.
8. Registra la postulación en `postulaciones/registro.xlsx` inmediatamente.

---

## Tu workspace

Todo tu estado vive en `job-hunter-workspace/`, **fuera** de este repo.
Tus datos personales nunca se mezclan con el código del skill.

```
job-hunter-workspace/
├── cv/
│   ├── cv-[idioma].md          ← fuente de verdad (tu idioma)
│   ├── cv-en.md                ← fuente de verdad (inglés)
│   ├── output/                 ← PDFs en proceso / borradores
│   ├── aprobados/              ← ★ solo estos se envían
│   │   ├── cv-[idioma]-aprobado.pdf
│   │   └── cv-en-aprobado.pdf
│   └── perfil.md               ← tu perfil + respuestas fijas
├── busqueda/
│   ├── config.md
│   ├── vacantes-nuevas.md
│   └── vacantes-descartadas.md
├── postulaciones/
│   ├── registro.xlsx           ← log de cada postulación
│   └── cover-letters/
└── logs/
    └── sesion-YYYY-MM-DD.md
```

### perfil.md — el archivo más importante

Se crea desde `templates/perfil.md`. Contiene todo lo que no tenés que
repetir en cada sesión:

```markdown
## Idioma de respuesta
- Idioma preferido: Español

## Preferencias de búsqueda
- Salario en moneda local: 12.500.000 COP/mes
- Salario en USD: 4.000 USD/mes

## Respuestas fijas
- WhatsApp / SMS: Yes
- Email: Yes
- Disponibilidad: 1 semana
- Visa sponsorship: No
```

El skill las lee al inicio y no vuelve a preguntar. Si falta algo, pregunta
una vez y lo guarda.

---

## Lo que el skill NO hace

- No instala MCPs ni crea cuentas en portales por vos.
- No resuelve CAPTCHAs de bloqueo (hCaptcha en Lever, Cloudflare en Workable).
- No puede marcar el checkbox "I'm not a robot" (reCAPTCHA v2 — corre en
  un iframe sandboxed de Google que el Chrome MCP no puede tocar). En cambio,
  te avisa, te pasa la URL y espera a que lo hagas vos.
- No inventa logros ni métricas que no confirmaste.
- No genera imágenes (solo prompts para que las generes con otra herramienta).
- No envía nada sin que lo veás primero (en modo supervisado).
- No avanza de Fase si faltan aprobaciones.

---

## Estructura del repositorio

```
job-hunter/
├── SKILL.md                    ← lógica completa: fases, gates, stop conditions
├── references/
│   ├── ats-2026.md             ← reglas de parseo ATS actualizadas
│   ├── prerequisitos-chrome.md ← setup y troubleshooting Chrome MCP
│   ├── portales-soportados.md  ← notas por portal (LinkedIn, Ashby, Lever…)
│   ├── ats-formularios.md      ← técnicas de llenado + APIs públicas de ATS
│   ├── estructura-cv.md        ← estructura y reglas de contenido del CV
│   └── cover-letter-guide.md   ← cómo escribir cover letters que funcionan
├── templates/
│   ├── perfil.md               ← plantilla de perfil + respuestas fijas
│   ├── design-a.html           ← ATS-First
│   ├── design-b.html           ← Balanced
│   ├── design-c.html           ← Portfolio-Ready
│   └── cover-letter.html
├── scripts/
│   ├── generar-pdf.py          ← markdown → PDF con el template elegido
│   ├── verificar-chrome.sh     ← verifica conexión al Chrome MCP
│   ├── escanear-ats.py         ← escanea APIs públicas de ATS
│   └── test-parseo.py          ← test de parseo ATS sobre el PDF generado
└── evals/
    └── evals.json              ← casos de prueba del skill
```

---

## Preguntas frecuentes

**¿Puedo usar solo la Fase 1 (CV) sin hacer búsqueda ni postulación?**  
Sí. Las fases son independientes. Podés terminar en 1.5 con tus PDFs
aprobados y usar esos archivos como querás.

**¿Qué pasa si el portal pide login?**  
El skill se detiene y vos iniciás sesión manualmente. Nunca crea cuentas
en tu nombre.

**¿Funciona con cualquier CV?**  
Sí: `.docx`, `.pdf` o `.md`. Si el archivo tiene protección de copia o
parseo complicado, Claude te avisa.

**¿Los PDFs aprobados se reemplazan automáticamente si corrijo el CV?**  
No. Si editás el CV después de aprobar, tenés que pasar de nuevo por el
gate de aprobación. Así evitás enviar una versión que no revisaste.

**¿Qué pasa con el checkbox "I'm not a robot"?**  
El Chrome MCP no puede interactuar con el reCAPTCHA v2 porque corre
dentro de un iframe sandboxed de Google. El skill detecta el checkbox
antes de intentar enviar, para el envío, y te muestra una advertencia
con la URL del formulario. Vos lo marcás manualmente, avisás, y el skill
retoma y hace click en Enviar. Si preferís, también podés omitir esa
vacante — queda guardada como `pendiente_captcha` en tu registro.

**¿El skill guarda mis datos personales en el repositorio?**  
No. Todo tu workspace vive fuera del repo. Este repositorio no contiene
ningún dato personal.

---

## Contribuir

Issues y PRs son bienvenidos, especialmente para:
- Nuevas notas de compatibilidad en `portales-soportados.md`.
- Actualizaciones a `ats-2026.md` cuando cambien las reglas de parseo.
- Nuevos templates de diseño.
- Compatibilidad con nuevos ATS o portales.

---

## Licencia

MIT — ver [LICENSE](LICENSE).
