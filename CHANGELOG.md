# Changelog

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
