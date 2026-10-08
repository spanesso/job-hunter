# Changelog

## 1.4.1
- **Fase 3 — detección de reCAPTCHA "I'm not a robot"**: el subagente escanea
  el formulario antes de enviar buscando el checkbox de reCAPTCHA v2. Si lo
  encuentra, detiene el envío y escribe `estado: requiere_captcha_manual`. El
  agente principal muestra una advertencia clara con la URL y espera a que el
  usuario marque el checkbox manualmente. Después de la confirmación, el agente
  hace click en enviar. Si el usuario omite la vacante, queda registrada como
  `pendiente_captcha` en `registro.xlsx`.
- **Sección 2.3**: diferencia explícita entre el checkbox reCAPTCHA v2 (campo
  dentro del formulario, requiere intervención manual puntual) y los CAPTCHAs
  de bloqueo como hCaptcha/Cloudflare (bloquean la navegación entera).

## 1.4.0
- **Prerequisitos automáticos**: el skill verifica e instala `markdown`,
  `weasyprint` y `pypdf` con `pip install` al arrancar la Fase 1. Si Python 3
  no está instalado, entrega el comando exacto por OS. Para el Chrome MCP,
  detecta automáticamente cuál está disponible y guía la configuración solo
  si ninguno responde. Solo se le pide acción al usuario en los dos casos
  genuinamente manuales (instalar Python por primera vez, autorizar la extensión).
- **Fase 2 — subagentes por portal**: cada portal de búsqueda corre en un
  fork separado (Agent con subagent_type: "fork"). Los forks navegan, calculan
  match y escriben resultados en archivos locales; el agente principal consolida.
  Menos tokens en el contexto principal.
- **Fase 3 — subagente por vacante**: cada formulario corre en su propio fork.
  En modo supervisado, el fork escribe un preview y espera señal del agente
  principal antes de enviar. El agente principal solo registra el resultado final.
- README actualizado: tabla de requisitos con columna "Lo instala el skill",
  sección de búsqueda y postulación actualizada con mención a subagentes.

## 1.3.0
- **Paso 0 — Idioma de respuesta**: al iniciar el skill pregunta en qué idioma
  responder. Lo guarda en `perfil.md` y en memoria de Claude Code (`mem_save`);
  no lo vuelve a preguntar en sesiones siguientes.
- **Fase 1 — PDFs bilingües obligatorios**: siempre se generan dos versiones
  (idioma del usuario + inglés). Ambas requieren aprobación explícita e
  individual antes de continuar.
- **Fase 1 — Carpeta `cv/aprobados/`**: los PDFs aprobados se copian a esa
  carpeta exclusiva. Las Fases 2 y 3 solo usan archivos de `cv/aprobados/`;
  si falta cualquiera de las dos versiones, se muestra una advertencia y se
  bloquea el avance.
- **README reescrito**: estructura más clara con flujo paso a paso, diagrama,
  tabla de diseños, FAQ, y descripción del workspace.

## 1.2.0
- **Fase 1 — Gate de aprobación de PDF**: después de generar los PDFs del CV,
  el skill muestra la ruta completa de cada archivo y espera aprobación explícita
  del usuario antes de continuar. No avanza con un "no" o silencio.
- **Fase 1 — Limpieza anti-filtros IA**: el CV generado no puede contener advertencias
  de generación por IA, menciones a Claude/ChatGPT ni frases genéricas penalizadas
  por ATS. Regla forzada antes de escribir el markdown final.
- **Fase 2 — Salario en dos monedas**: al configurar la búsqueda se solicita el
  salario objetivo en la moneda del país del usuario Y en USD. Ambos campos se
  guardan en `perfil.md` y se usan según el país de la empresa.
- **Fase 2 — Selección de puesto (Paso 2.0)**: antes de buscar, el skill lee el CV,
  extrae aptitudes y muestra una lista de títulos de cargo sugeridos con checkboxes.
  El usuario elige uno o varios y/o escribe el suyo. La búsqueda usa solo los puestos
  confirmados en ese paso.
- **Fase 3 — Consentimiento de contacto**: si el formulario pregunta por WhatsApp o
  email, la respuesta es siempre **Yes** en ambos canales.
- `templates/perfil.md` actualizado: salario en dos monedas, consentimiento WhatsApp
  y email marcados como Yes por defecto con nota explicativa.

## 1.1.0
- `perfil.md` ahora guarda **respuestas fijas** para formularios (consentimiento de
  WhatsApp/SMS, fecha de inicio, autorización de trabajo) y las rutas de CV por idioma;
  nueva plantilla `templates/perfil.md`.
- Fase 3: el PDF del CV se elige **por idioma de la vacante**; verificación de campos antes
  de enviar y confirmación de la pantalla de éxito después; datos sin respaldo se reportan
  como supuestos.
- Fase 2: descarte por elegibilidad (nacionalidad, residencia, stack excluido) y búsqueda
  por APIs públicas de ATS con `scripts/escanear-ats.py`.
- Nuevo `references/ats-formularios.md` (técnicas por ATS, bloqueos conocidos: hCaptcha,
  Cloudflare, shadow DOM) y notas nuevas en `portales-soportados.md`.

## 1.0.0
- Versión inicial: diagnóstico de CV, 3 diseños, búsqueda con match honesto, cover letters
  y postulación asistida.
