import os, sys, win32com.client
from pathlib import Path
docx = Path(os.environ['TEMP']) / 'tfi_tesis_build' / 'tesis_v6.docx'
pdf = Path(r'C:\Users\sever\OneDrive\Desktop\tfi-osint-n8n\V4\devoluciones\tesis_v6.pdf')
word = win32com.client.Dispatch('Word.Application')
word.Visible = False
word.DisplayAlerts = 0
try:
    doc = word.Documents.Open(str(docx))
    doc.ExportAsFixedFormat(str(pdf), ExportFormat=17)
    doc.Close(False)
    print('DONE')
except Exception as e:
    print('ERR')
    print(e)
    sys.exit(1)
finally:
    try:
        word.Quit()
    except:
        pass
