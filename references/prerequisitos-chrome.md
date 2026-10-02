# Prerequisitos: Chrome MCP

Las Fases 2 (búsqueda) y 3 (postulación) dependen de que Claude Code tenga
acceso a un MCP de automatización de Chrome (por ejemplo `claude-in-chrome`
o `chrome-devtools`). Este skill no instala el MCP — solo verifica que
esté disponible y da instrucciones de troubleshooting.

## 1. Instalación de la extensión

1. Instala la extensión de Chrome correspondiente a tu MCP (sigue la guía
   oficial del MCP que vayas a usar).
2. Verifica que la extensión esté **habilitada** (no solo instalada) en
   `chrome://extensions`.
3. Abre Chrome y deja al menos una pestaña activa — algunos MCPs no
   responden si Chrome está completamente cerrado.

## 2. Verificación de conexión (test de ping)

Ejecuta:

```bash
bash scripts/verificar-chrome.sh
```

El script intenta una operación mínima (listar pestañas/contexto) contra
el MCP configurado. Una respuesta válida confirma la conexión.

**GATE:** no inicies Fase 2 o 3 sin que esta verificación pase.

## 3. Troubleshooting de errores comunes

| Síntoma | Causa probable | Solución |
|---|---|---|
| El MCP no responde / timeout | Extensión desactivada o Chrome cerrado | Habilita la extensión, abre Chrome, reintenta |
| "Tab not found" en cada llamada | IDs de pestaña de una sesión anterior | Vuelve a pedir el contexto de pestañas (no reutilices IDs viejos) |
| El MCP responde pero no ve la página | Página aún cargando o en un iframe no soportado | Espera a que cargue, reintenta una vez |
| Error de permisos / sitio bloqueado | El MCP requiere aprobación por sitio | Revisa la configuración de permisos de la extensión para ese dominio |
| Puerto o conexión rechazada | El servidor MCP no está corriendo | Reinicia el cliente MCP según su documentación |

## 4. Gate obligatorio

No continúes a Fase 2 o 3 si la verificación falla. Informa al usuario
exactamente qué paso de esta lista no se cumplió y espera a que lo
resuelva — no intentes "adivinar" selectores o rellenar formularios sin
confirmación de que el MCP está realmente conectado a la página correcta.
