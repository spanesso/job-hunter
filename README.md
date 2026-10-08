# job-hunter

Un skill de [Claude Code](https://claude.com/claude-code) que actúa como
un **head hunter personal**: diagnostica tu CV con ojo de reclutador, lo
reconstruye en 3 diseños pensados para sobrevivir filtros ATS *y*
revisión humana, busca vacantes con análisis de match honesto (no
aspiracional), y te asiste en la postulación vía automatización de
navegador.

No es un asistente que hace lo que le pides sin filtro. Es un reclutador
senior que te dice lo que no quieres oír cuando tu CV o una vacante lo
justifican — y documenta esa recomendación, aunque la decisión final sea
siempre tuya.

## Qué hace

- **Diagnóstico brutal del CV**: qué vería un reclutador en los primeros
  6 segundos, qué falta, qué sobra, y una estimación honesta de tu
  probabilidad de pasar el filtro ATS y la revisión humana.
- **3 diseños de CV** generados del mismo markdown fuente:
  - **A — ATS-First**: máxima compatibilidad de parseo, para portales.
  - **B — Balanced**: profesional con personalidad, para envío directo.
  - **C — Portfolio-Ready**: visual, con sidebar, solo para envío humano
    directo (nunca para portales ATS).
- **Búsqueda de vacantes** con análisis de match real: requisitos duros
  vs. deseables, red flags ("rockstar/ninja", salario ausente,
  requisitos contradictorios), y una recomendación honesta de postularte
  o no.
- **Cover letters que venden**: abren con el problema de la empresa,
  conectan una experiencia específica del candidato, cierran con un
  call-to-action — nunca repiten el CV en prosa.
- **Postulación asistida** vía Chrome MCP, con registro inmediato de
  cada envío en un Excel (tu base de datos de seguimiento).
- **Respuestas fijas** en `perfil.md` (consentimientos, disponibilidad,
  CV por idioma): se definen una vez y se aplican a todos los formularios.
- **CV por idioma**: detecta el idioma de cada vacante y sube el PDF
  correspondiente.
- **Búsqueda por APIs públicas** de Greenhouse, Ashby, Lever y Recruitee
  (ofertas vigentes, no enlaces caducados) con `scripts/escanear-ats.py`.
- **Verificación y honestidad**: confirma cada campo y la pantalla de éxito,
  descarta vacantes cuyos requisitos de elegibilidad no cumples y reporta
  como supuesto cualquier dato que no esté respaldado.

## Qué NO hace

- No instala MCPs por ti. No crea cuentas en portales en tu nombre. No
  resuelve CAPTCHAs. No inventa métricas o logros que no confirmaste. No
  genera imágenes (solo prompts para que las generes tú con otra
  herramienta).

## Requisitos

- [Claude Code](https://claude.com/claude-code).
- Un MCP de automatización de Chrome (p.ej. `claude-in-chrome` o
  `chrome-devtools`) — solo necesario para las fases de búsqueda y
  postulación. Ver `references/prerequisitos-chrome.md`.
- Python 3 con `markdown`, `weasyprint` y `pypdf`:
  ```bash
  pip install markdown weasyprint pypdf
  ```

## Instalación

Copia (o clona) esta carpeta dentro de `.claude/skills/job-hunter/` en el
proyecto o directorio donde quieras usarlo:

```bash
git clone https://github.com/spanesso/job-hunter.git .claude/skills/job-hunter
```

Claude Code lo detectará automáticamente como skill disponible.

## Uso

Simplemente pide, dentro de una sesión de Claude Code:

> "Ayúdame a mejorar mi CV para buscar trabajo" / "Busca vacantes de
> [tu perfil]" / "Postúlame a esta vacante: [URL]"

El skill avanza en 3 fases (CV → búsqueda → postulación), cada una con
puntos de aprobación explícitos (*gates*) antes de generar archivos
finales o enviar una postulación real. Nada se envía sin que lo veas
primero, salvo que tú mismo confirmes el modo autónomo.

## Estructura

```
job-hunter/
├── SKILL.md                        # Lógica del skill: las 3 fases, gates, stop conditions
├── references/
│   ├── ats-2026.md                 # Reglas de parseo ATS vigentes
│   ├── prerequisitos-chrome.md     # Setup y troubleshooting del Chrome MCP
│   ├── portales-soportados.md      # Notas de compatibilidad por portal
│   ├── ats-formularios.md          # Técnicas de llenado por ATS y búsqueda por APIs
│   ├── estructura-cv.md            # Estructura y reglas de contenido del CV
│   └── cover-letter-guide.md       # Cómo escribir cover letters efectivas
├── templates/
│   ├── perfil.md                   # Plantilla de perfil + respuestas fijas
│   ├── design-a.html / design-b.html / design-c.html
│   └── cover-letter.html
├── scripts/
│   ├── generar-pdf.py              # Markdown → PDF con el template elegido
│   ├── verificar-chrome.sh         # Checklist de conexión al Chrome MCP
│   ├── escanear-ats.py             # Escanea listados públicos de ATS por keywords
│   └── test-parseo.py              # Test automatizado de parseo ATS
└── evals/
    └── evals.json                  # Casos de prueba para validar el comportamiento del skill
```

Todo el estado de tu búsqueda (tu CV en markdown, tus vacantes, tu
registro de postulaciones) vive en un `job-hunter-workspace/` **fuera**
de este repo — tus datos personales nunca se mezclan con el código del
skill.

## Contribuir

Issues y PRs son bienvenidos, especialmente para:
- Nuevas notas de compatibilidad en `portales-soportados.md` cuando
  encuentres el comportamiento de un portal nuevo.
- Actualizaciones a `ats-2026.md` cuando cambien las reglas de parseo.
- Nuevos templates de diseño.

## Licencia

MIT — ver [LICENSE](LICENSE).
