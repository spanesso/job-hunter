#!/usr/bin/env bash
# Verifica (de forma manual/guiada) que el Chrome MCP esté listo antes de
# iniciar las Fases 2 o 3 del skill job-hunter.
#
# Este script NO puede invocar herramientas MCP directamente (eso solo lo
# puede hacer el agente de Claude Code dentro de la conversación). Lo que
# hace es una lista de chequeo reproducible que el agente debe correr y
# reportar, más una verificación básica de que Chrome está corriendo.

set -euo pipefail

echo "== Verificación de prerequisitos Chrome MCP =="

if pgrep -x "Google Chrome" >/dev/null 2>&1; then
  echo "[OK] Google Chrome está en ejecución."
else
  echo "[FALTA] Google Chrome no parece estar corriendo. Ábrelo antes de continuar."
  exit 1
fi

cat <<'EOF'

Checklist que el agente debe completar manualmente dentro de la sesión
(ver references/prerequisitos-chrome.md):

  1. Confirmar que la extensión del Chrome MCP está HABILITADA en
     chrome://extensions (no solo instalada).
  2. Llamar a la herramienta de contexto/listado de pestañas del MCP
     (p.ej. tabs_context) y confirmar que devuelve al menos una pestaña.
  3. Si falla, consultar la tabla de troubleshooting en
     references/prerequisitos-chrome.md antes de reintentar.

GATE: no iniciar Fase 2 o 3 hasta que el paso 2 devuelva una respuesta
válida del MCP.
EOF
