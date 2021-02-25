from fastapi.exceptions import HTTPException

from cfdi.generics import Complex


class Nomina12SubContratacion:
    def __init__(self, data):
        attrs = data.get("attributes")

        self.rfcLabora = attrs.get("RfcLabora")
        self.porcentajeTiempo = attrs.get("PorcentajeTiempo")


class Nomina12Receptor:
    def __init__(self, data):
        attrs = data.get("attributes")

        self.curp = attrs.get("Curp")
        self.numSeguridadSocial = attrs.get("NumSeguridadSocial")
        self.fechaInicioRelLaboral = attrs.get("FechaInicioRelLaboral")
        self.antiguedad = attrs.get("Antigüedad")
        self.tipoContrato = attrs.get("TipoContrato")
        self.sindicalizado = attrs.get("Sindicalizado")
        self.tipoJornada = attrs.get("TipoJornada")
        self.tipoRegimen = attrs.get("TipoRegimen")
        self.numEmpleado = attrs.get("NumEmpleado")
        self.departamento = attrs.get("Departamento")
        self.puesto = attrs.get("Puesto")
        self.riesgoPuesto = attrs.get("RiesgoPuesto")
        self.periodicidadPago = attrs.get("PeriodicidadPago")
        self.banco = attrs.get("Banco")
        self.cuentaBancaria = attrs.get("CuentaBancaria")
        self.salarioBaseCotApor = attrs.get("SalarioBaseCotApor")
        self.salarioDiarioIntegrado = attrs.get("SalarioDiarioIntegrado")
        self.claveEntFed = attrs.get("ClaveEntFed")

        # todo: SubContratacion


class Nomina12Emisor:
    def __init__(self, data):
        attrs = data.get("attributes")

        self.registroPatronal = attrs.get("RegistroPatronal")
        self.curp = attrs.get("Curp")
        self.rfcPatronOrigen = attrs.get("RfcPatronOrigen")

        # todo: EntidadSNCF


class Nomina12Percepcion:
    def __init__(self, data):
        attrs = data.get("attributes")

        self.clave = attrs.get("Clave")
        self.concepto = attrs.get("Concepto")
        self.importeExento = attrs.get("ImporteExento")
        self.importeGravado = attrs.get("ImporteGravado")
        self.tipoPercepcion = attrs.get("TipoPercepcion")


class Nomina12JubilacionPensionRetiro:
    def __init__(self, data):
        attrs = data.get("attributes")

        self.totalUnaExhibicion = attrs.get("TotalUnaExhibicion")
        self.ingresoAcumulable = attrs.get("IngresoAcumulable")
        self.ingresoNoAcumulable = attrs.get("IngresoNoAcumulable")


class Nomina12Deduccion:
    def __init__(self, data):
        attrs = data.get("attributes")

        self.clave = attrs.get("Clave")
        self.concepto = attrs.get("Concepto")
        self.importe = attrs.get("Importe")
        self.tipoDeduccion = attrs.get("TipoDeduccion")


class Nomina12Deducciones(Complex):
    def __init__(self, data):
        attrs = data.get("attributes")

        self.totalImpuestosRetenidos = attrs.get("TotalImpuestosRetenidos")

        # getting nomina12:Deduccion
        self.deducciones = self.get_complex(
            data, item="nomina12:Deduccion", klass=Nomina12Deduccion
        )


class Nomina12Percepciones(Complex):
    def __init__(self, data):
        attrs = data.get("attributes")

        self.totalExento = attrs.get("TotalExento")
        self.totalGravado = attrs.get("TotalGravado")
        self.totalJubilacionPensionRetiro = attrs.get(
            "TotalJubilacionPensionRetiro"
        )
        self.totalSueldos = attrs.get("TotalSueldos")

        # getting percepciones
        self.percepciones = self.get_complex(
            data, item="nomina12:Percepcion", klass=Nomina12Percepcion
        )

        # getting JubilacionPensionRetiro
        children = data.get("children")[0]

        self.jubilacionPensionRetiro = self.get_optional(
            children,
            item="nomina12:JubilacionPensionRetiro",
            klass=Nomina12JubilacionPensionRetiro,
        )


class Nomina12SubsidioCausado:
    def __init__(self, data):
        attrs = data.get("SubsidioCausado")

        self.subsidioCausado = attrs.get("SubsidioCausado")


class Nomina12CompensacionSaldosAFavor:
    def __init__(self, data):
        attrs = data.get("attributes")

        self.saldoAFavor = attrs.get("SaldoAFavor")
        self.anio = attrs.get("Año")
        self.remanenteSalFav = attrs.get("RemanenteSalFav")


class Nomina12OtroPago:
    def __init__(self, data):
        attrs = data.get("attributes")

        self.tipoOtroPago = attrs.get("TipoOtroPago")
        self.clave = attrs.get("Clave")
        self.concepto = attrs.get("Concepto")
        self.importe = attrs.get("Importe")

        # todo: SubsidioAlEmpleo
        # todo: CompensacionSaldosAFavor


class Nomina12Incapacidad:
    def __init__(self, data):
        attrs = data.get("attributes")

        self.diasIncapacidad = attrs.get("DiasIncapacidad")
        self.tipoIncapacidad = attrs.get("TipoIncapacidad")
        self.importeMonetario = attrs.get("ImporteMonetario")


class Nomina(Complex):
    supported_versions = ["1.2"]

    def __init__(self, data):
        attrs = data.get("attributes")

        self.version = attrs.get("Version")

        self.check_version()

        self.tipoNomina = attrs.get("TipoNomina")

        self.fechaPago = attrs.get("FechaPago")
        self.fechaFinalPago = attrs.get("FechaFinalPago")
        self.fechaInicialPago = attrs.get("FechaInicialPago")

        self.numDiasPagados = attrs.get("NumDiasPagados")
        self.totalPercepciones = attrs.get("TotalPercepciones")
        self.totalDeducciones = attrs.get("TotalDeducciones")
        self.totalOtrosPagos = attrs.get("TotalOtrosPagos")

        # getting children
        children = data.get("children")[0]

        self.receptor = Nomina12Receptor(children.get("nomina12:Receptor"))
        self.emisor = self.get_optional(
            children, item="nomina12:Emisor", klass=Nomina12Emisor
        )

        self.percepciones = self.get_optional(
            children, item="nomina12:Percepciones", klass=Nomina12Percepciones
        )
        self.deducciones = self.get_optional(
            children, item="nomina12:Deducciones", klass=Nomina12Deducciones
        )

        # todo: raw
        self.otrosPagos = children.get("nomina12:OtrosPagos")
        self.incapacidades = children.get("nomina12:Incapacidades")

    def check_version(self):
        if self.version not in self.supported_versions:
            raise HTTPException(
                status_code=422, detail=f"Version {self.version} not supported"
            )
