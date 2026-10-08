# Changelog

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
