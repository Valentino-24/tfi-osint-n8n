# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, 'docs/scripts')
import convertir_pdf as cp

# Override paths for v6
cp.DOCX_BUILD = Path(r'C:\temp\tfi_tesis_build\tesis_v6.docx')
cp.PDF_SALIDA = Path(r'C:\Users\sever\OneDrive\Desktop\tfi-osint-n8n\V4\devoluciones\tesis_v6.pdf')
cp.MD_ORIGEN  = Path(r'C:\Users\sever\OneDrive\Desktop\tfi-osint-n8n\V4\devoluciones\tesis_v6.md')

# Run just the word processing
cp.procesar_con_word(numerar=True)
