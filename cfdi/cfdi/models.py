from fastapi.exceptions import HTTPException
from jsonpickle.pickler import Pickler

from cfdi.generics import Complex
from cfdi.nomina.models import Nomina
from cfdi.timbre_fiscal.models import TimbreFiscalDigital


class Emisor:
    def __init__(self, data):
        attrs = data.get("attributes")

        self.rfc = attrs.get("Rfc")
        self.nombre = attrs.get("Nombre")
        self.regimenFiscal = attrs.get("RegimenFiscal")


class Receptor:
    def __init__(self, data):
        attrs = data.get("attributes")

        self.rfc = attrs.get("Rfc")
        self.nombre = attrs.get("Nombre")
        self.usoCFDI = attrs.get("UsoCFDI")
        self.residenciaFiscal = attrs.get("ResidenciaFiscal")
        self.numRegIdTrib = attrs.get("NumRegIdTrib")


class Complemento(Complex):
    def __init__(self, data):

        self.timbreFiscalDigital = self.get_optional(
            data, item="tfd:TimbreFiscalDigital", klass=TimbreFiscalDigital
        )

        self.nomina = self.get_optional(
            data, item="nomina12:Nomina", klass=Nomina
        )


class Trasladado:
    def __init__(self, data):
        attrs = data.get("attributes")

        self.base = attrs.get("Base")
        self.impuesto = attrs.get("Impuesto")
        self.tipoFactor = attrs.get("TipoFactor")
        self.tasaOCuota = attrs.get("TasaOCuota")
        self.importe = attrs.get("Importe")


class Retencion:
    def __init__(self, data):
        attrs = data.get("attributes")

        self.impuesto = attrs.get("Impuesto")
        self.importe = attrs.get("Importe")


class ConceptoImpuestos:
    """
    {
        cfdi:Impuestos: {
            cfdi:Traslados: {
                cfdi:Traslado: {}
            }
        }
    }
    """

    def __init__(self, data):
        self.trasladados = []

        traslados = data.get("cfdi:Traslados")
        self.trasladados.append(Trasladado(traslados.get("cfdi:Traslado")))


class Concepto(Complex):
    def __init__(self, data):
        attrs = data.get("attributes")

        self.claveProdServ = attrs.get("ClaveProdServ")
        self.cantidad = attrs.get("Cantidad")
        self.claveUnidad = attrs.get("ClaveUnidad")
        self.descripcion = attrs.get("Descripcion")
        self.valorUnitario = attrs.get("ValorUnitario")
        self.importe = attrs.get("Importe")
        self.noIdentificacion = attrs.get("NoIdentificacion")
        self.unidad = attrs.get("Unidad")
        self.descuento = attrs.get("Descuento")

        # getting children
        if not self.has_children(data.get("children")):
            return  # nothing to do

        children = data.get("children")[0]
        self.impuestos = ConceptoImpuestos(children.get("cfdi:Impuestos"))

        # todo: raw
        self.InformacionAduanera = children.get("cfdi:InformacionAduanera")
        self.CuentaPredial = children.get("cfdi:CuentaPredial")
        self.ComplementoConcepto = children.get("cfdi:ComplementoConcepto")
        self.Parte = children.get("cfdi:Parte")


class Conceptos(Complex):
    def __init__(self, data):
        self.concepto = Concepto(data.get("cfdi:Concepto"))


class Impuestos:
    def __init__(self, data):
        attrs = data.get("attributes")

        self.totalImpuestosTrasladados = attrs.get("TotalImpuestosTrasladados")
        self.totalImpuestosRetenidos = attrs.get("TotalImpuestosRetenidos")

        # getting children
        children = data.get("children")[0]

        # todo make it better
        self.retenciones = []
        if children.get("cfdi:Retenciones"):
            retenciones = children.get("cfdi:Retenciones")
            self.retenciones.append(
                Retencion(retenciones.get("cfdi:Retencion"))
            )

        # todo make it better
        self.traslados = []
        if children.get("cfdi:Traslados"):
            traslados = children.get("cfdi:Traslados")
            self.traslados.append(Trasladado(traslados.get("cfdi:Traslado")))


class CFDI(Complex):
    supported_versions = ["3.3"]

    def __init__(self, data):
        attrs = data.get("attributes")

        self.schemaLocation = attrs.get("xsi:schemaLocation")
        self.version = attrs.get("Version")

        self.check_version()

        self.serie = attrs.get("Serie")
        self.folio = attrs.get("Folio")
        self.fecha = attrs.get("Fecha")
        self.sello = attrs.get("Sello")
        self.formaPago = attrs.get("FormaPago")
        self.noCertificado = attrs.get("NoCertificado")
        self.certificado = attrs.get("Certificado")
        self.subTotal = attrs.get("SubTotal")
        self.moneda = attrs.get("Moneda")
        self.total = attrs.get("Total")
        self.tipoDeComprobante = attrs.get("TipoDeComprobante")
        self.metodoPago = attrs.get("MetodoPago")
        self.lugarExpedicion = attrs.get("LugarExpedicion")
        self.condicionesDePago = attrs.get("CondicionesDePago")
        self.descuento = attrs.get("Descuento")
        self.tipoCambio = attrs.get("TipoCambio")
        self.confirmacion = attrs.get("Confirmacion")

        # getting children
        children = data.get("children")[0]

        self.emisor = Emisor(children.get("cfdi:Emisor"))
        self.receptor = Receptor(children.get("cfdi:Receptor"))
        self.complemento = Complemento(children.get("cfdi:Complemento"))

        self.conceptos = Conceptos(children.get("cfdi:Conceptos"))
        self.impuestos = self.get_optional(
            children, item="cfdi:Impuestos", klass=Impuestos
        )

        # todo: raw
        self.addenda = children.get("cfdi:Addenda")
        self.cfdiRelacionados = children.get("cfdi:CfdiRelacionados")

    def to_dict(self):
        p = Pickler(use_decimal=True)
        return p.flatten(self)

    def check_version(self):
        if self.version not in self.supported_versions:
            raise HTTPException(
                status_code=422, detail=f"Version {self.version} not supported"
            )
