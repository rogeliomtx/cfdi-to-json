import os

import xmlschema

from cfdi.cfdi.models import CFDI


base_dir = os.path.dirname(__file__)
cfdi_path = os.path.join(base_dir, "assets/cfdv33.xsd.xml")
stamp_path = os.path.join(base_dir, "tfdv11.xsd.xml")
payroll_path = os.path.join(base_dir, "nomina12.xsd.xml")


schema = xmlschema.XMLSchema(
    cfdi_path,
    locations=[
        (
            "http://www.sat.gob.mx/TimbreFiscalDigital",
            stamp_path,
        ),
        ("http://www.sat.gob.mx/nomina12", payroll_path),
    ],
    converter=xmlschema.AbderaConverter,
    validation="skip",
    allow="local",
)


class CFDIHandler:
    @classmethod
    def to_json(cls, file):
        data = schema.to_dict(file.file)

        cfdi = CFDI(data)

        return {"formated": cfdi.to_dict(), "raw": data}
