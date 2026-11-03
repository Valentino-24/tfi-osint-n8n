# TFI OSINT/n8n — Sistema automatizado de monitoreo de foros y redes sociales

Sistema de monitoreo OSINT sobre comunidades técnicas de Reddit, construido con n8n y PostgreSQL, con clasificación heurística bilingüe (español/inglés) y motor de detección de anomalías.

**Autores:** Valentino Lorca, Jerónimo Zúñiga, Enzo Severino
**Directores:** Prof. Alberto Cortez, Prof. Ariel Enferrel
**Institución:** Universidad (Tecnicatura Universitaria en Programación)

---

## Estructura del repositorio

```
├── README.md                    # Este archivo
├── AGENTS.md                    # Instrucciones para agentes de IA
├── CHANGES.md                   # Roadmap de changes (OpenSpec)
├── knowledge-base/              # Base de conocimiento del dominio (fuente de verdad)
├── openspec/                    # Changes y specs (OpenSpec)
├── docs/                        # Documentación del informe
│   ├── informe/                 # Informe vigente (tesis_v6.md + tesis_v6.pdf)
│   │   └── tribunal/            # Devoluciones del tribunal (V4, V5)
│   ├── anexos/                  # DDL (A) y workflow (B)
│   ├── evidencias/              # Evidencia reproducible por fecha
│   ├── figuras/                 # Figuras del informe (4)
│   ├── scripts/                 # Scripts de generación y verificación
│   │   └── legacy/              # Scripts de un solo uso (histórico)
│   ├── guias/                   # Guías de instalación, ejecución y conceptos
│   ├── historico/               # Versiones anteriores del informe (v2, v3, v4, v5)
│   └── build/                   # Artefactos temporales de build
├── prototipo-landing-page/      # Prototipo de landing page
├── .opencode/                   # Configuración de OpenCode (skills)
├── .claude/                     # Skills de Claude
└── .gitignore                   # Archivos excluidos del repositorio
```

## Documentación principal

- **Informe vigente:** `docs/informe/tesis_v6.pdf`
- **Informe en Markdown:** `docs/informe/tesis_v6.md`
- **Base de conocimiento:** `knowledge-base/README.md`
- **Roadmap:** `CHANGES.md`

## Generación del PDF

```powershell
python docs/scripts/convertir_pdf.py --md docs/informe/tesis_v6.md --out docs/informe/tesis_v6.pdf
```

## Verificación del PDF

```powershell
python docs/scripts/verificar_pdf.py --pdf docs/informe/tesis_v6.pdf --md docs/informe/tesis_v6.md --docx "%TEMP%\tfi_tesis_build\tesis_v6.docx"
```

## Stack tecnológico

| Capa | Tecnología |
|------|------------|
| Orquestación | n8n 2.40.6 (Docker) |
| Persistencia | PostgreSQL 18 |
| Base de datos | `tesi_osint` |
| Fuente de datos | Reddit RSS/Atom público |
| Seudonimización | HMAC-SHA-256 |

Ver `knowledge-base/02_descripcion_general.md` para el detalle completo.
