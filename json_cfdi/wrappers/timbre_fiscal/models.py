class TimbreFiscalDigital:
    def __init__(self, data):
        attrs = data.get("attributes")

        self.rfcProvCertif = attrs.get("RfcProvCertif")
        self.version = attrs.get("Version")
        self.uuid = attrs.get("UUID")
        self.fechaTimbrado = attrs.get("FechaTimbrado")
        self.selloCFD = attrs.get("SelloCFD")
        self.noCertificadoSAT = attrs.get("NoCertificadoSAT")
        self.selloSAT = attrs.get("SelloSAT")
        self.schemaLocation = attrs.get("xsi:schemaLocation")
