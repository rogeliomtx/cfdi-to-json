# CFDI a JSON
Una forma consistente de procesar archivos xml y procesarlos en modelos 
manejable.

## Formatos soportados
- CFDI v3.3
- Nómina v1.2
- Timbre Fiscal Digital v1.1

## Uso
```python
from json_cfdi import CFDIJson

settings = {
    "use_decimal": True, # optional. default: True
}

def xml_to_json(file):
    handler = CFDIJson(**settings)
    return handler.to_json(file)

>> {"formated": {"formated_json"}, "raw": {"raw_json"}}
```

## Fast API
Opcionalmente puedes crear un servicio api rest para consumir en local.

```shell
uvicorn main.json_cfdi:app --reload
```

```python
import requests

requests.get("http://localhost:8000/cfdis/files/", file)
```
