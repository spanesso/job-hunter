# Llenado de formularios ATS — técnicas validadas

Notas prácticas de uso real con Chrome MCP. Actualiza este archivo cuando
descubras un comportamiento nuevo; es más valioso que una lista teórica.

## Principios

1. **Navega directo a la URL del formulario** (p. ej. `/application` en
   Ashby, `/c/new` en Recruitee, `/apply` en Lever) en vez de hacer clic en
   "Apply" desde la descripción: evita bloqueos de permisos en clics de
   primer contacto.
2. **Lee todos los campos antes de llenar** (`read_page` / `find`).
3. **Verifica, no asumes.** Después de llenar, confirma con captura (o
   leyendo el DOM) que radios, desplegables y archivos quedaron como
   querías. Después de enviar, confirma con captura la pantalla de éxito:
   `get_page_text` puede devolver el texto anterior al envío.
4. **Un clic de verificación por control** cuando uses coordenadas: si una
   lista desplegable se desplaza, el clic cae en otra opción (ejemplo real:
   se eligió "In 2 months" en vez de "In 2 weeks").

## Controles comunes

| Control | Técnica que funciona | Qué falla |
|---|---|---|
| Texto / email / tel | `form_input` con el `ref` | Asignar `.value` por JS sin disparar `input` |
| Textarea larga (React) | `focus()` + `document.execCommand('insertText', false, valor)` | `nativeInputValueSetter` solo: React lo ve vacío |
| Radio buttons React | Clic real sobre el radio, o secuencia `mousedown → mouseup → click → change` | `.click()` solo o `dispatchEvent(new Event('change'))` |
| Botones Yes/No (Ashby) | Clic real; confirmar con captura | Marcarlos por JS: se ven marcados pero el formulario responde "campo requerido" |
| Combobox / autocompletado (ubicación) | Clic en el campo → escribir texto → esperar ~1.5 s → elegir la opción de la lista | Asignar el valor por JS: la lista no aparece |
| Select estilo React-Select (Greenhouse) | Clic en el campo, **escribir el texto de la opción y Enter** | Clics por coordenadas sobre la lista |
| Subida de CV | `file_upload` con el `ref` del `input[type=file]` | Clic en el botón (abre un diálogo nativo que no se ve) |
| Casillas de consentimiento | Clic y comprobar `checked` con JS | Suponer que el clic funcionó |

## Por ATS

- **Ashby** (`jobs.ashbyhq.com`): el formulario tarda en cargar ("Fetching
  application form"); espera unos segundos antes de leer. Hay un campo
  oculto de reCAPTCHA v3 invisible que se resuelve solo: ignóralo.
  Pregunta frecuente de consentimiento de WhatsApp: ver "Respuestas
  fijas" en `perfil.md`.
- **Greenhouse** (`job-boards.greenhouse.io`): el formulario va en la misma
  página de la oferta. País del teléfono es un selector aparte. Muchos
  selects son React-Select (ver tabla). Hay casillas de consentimiento de
  datos obligatorias y otras opcionales.
- **Recruitee** (`*.recruitee.com`): usar `/c/new`; la confirmación es la
  URL `/applied` con "All done!". El selector de país del teléfono requiere
  clic real. Cuidado con las preguntas Sí/No: el `ref` de "Yes" y "No" a
  veces vienen invertidos; verifica con captura.
- **Rippling** (`ats.rippling.com`): funciona bien; autocompleta nombre y
  ubicación al subir el CV.
- **Lever** (`jobs.lever.co`): muchos formularios llevan **hCaptcha** → no
  se puede automatizar; márcalo como "intervención manual".
- **Workable** (`apply.workable.com`): algunos formularios traen
  verificación **Cloudflare** → intervención manual. Los enlaces antiguos
  caducan: verifica que la oferta siga abierta.
- **SmartRecruiters** (`oneclick-ui`): usa shadow DOM; `find`/`read_page`
  no exponen los inputs ni el `input[type=file]`, así que `file_upload`
  no es posible. Márcalo como "intervención manual". También puede limitar
  la tasa de envíos ("try again in ...").
- **Zoho Recruit**: CAPTCHA de imagen → intervención manual.
- **GetOnBoard, Globant, BairesDev**: exigen login → el usuario inicia
  sesión manualmente.

## Elegibilidad: lee antes de postular

"Remote" no significa "elegible desde cualquier país". Antes de llenar,
busca en la descripción restricciones de nacionalidad, residencia o zona
horaria (p. ej. "must be a US/Canada resident", "nacionalidad mexicana e
INE físico"). Si no las cumples, **descarta y registra la razón**: no
postules afirmando algo falso.

## Búsqueda por APIs públicas (más fiable que el buscador web)

Las búsquedas web devuelven muchos enlaces caducados. Los ATS publican
listados abiertos en JSON, sin login:

- Greenhouse: `https://boards-api.greenhouse.io/v1/boards/{empresa}/jobs`
- Ashby: `https://api.ashbyhq.com/posting-api/job-board/{empresa}`
- Lever: `https://api.lever.co/v0/postings/{empresa}?mode=json`
- Recruitee: `https://{empresa}.recruitee.com/api/offers/`

`scripts/escanear-ats.py` consulta una lista de empresas y filtra por
palabras clave del título. Después filtra a mano por ubicación/elegibilidad:
la mayoría de roles "remote" están limitados a EE. UU./UE/Canadá.
