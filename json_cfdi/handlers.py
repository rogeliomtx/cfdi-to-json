import os

import xmlschema

from json_cfdi.wrappers.cfdi.models import CFDI
from jsonpickle.pickler import Pickler


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


class CFDIJson:
    def __init__(self, use_decimal=True):
        self.use_decimal = use_decimal
        self.pickler = Pickler(use_decimal=self.use_decimal)

    def to_json(self, file):
        # todo: try except
        # - format is not valid
        data = schema.to_dict(file.file)
        cfdi = CFDI(data)
        return {"formated": self.to_dict(cfdi), "raw": data}

    def to_dict(self, cfdi):
        return self.pickler.flatten(cfdi)
