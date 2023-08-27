from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Status(models.TextChoices):
    IDLE = "Idle", "Idle"
    TESTING = "Testing", "Testing"
    DEBUG = "Debug", "Debug"


class CPUArchType(models.TextChoices):
    ARMHF = "armhf", "armhf"
    AMD64 = "amd64", "amd64"


class EncryptionType(models.TextChoices):
    SYMMETRIC = "Symmetric", "Symmetric"
    X509 = "X509", "X509"


class SerialModel(models.TextChoices):
    RS232 = "RS232", "RS232"
    RS422 = "RS422", "RS422"
    RS485 = "RS485", "RS485"


class BaudRate(models.IntegerChoices):
    RATE_1200 = 1200, "1200"
    RATE_2400 = 2400, "2400"
    RATE_4800 = 4800, "4800"
    RATE_9600 = 9600, "9600"
    RATE_19200 = 19200, "19200"
    RATE_115200 = 115200, "115200"


class SIMOperator(models.TextChoices):
    CHUNGHWA = "Chunghwa", "Chunghwa"
    TMOBILE = "TMobile", "TMobile"


class NportMode(models.TextChoices):
    REALCOM = "Realcom", "Realcom"
    RFC2217 = "RFC2217", "RFC2217"
    TELNET = "Telnet", "TELNET"


class TestbedWifiAP(models.Model):
    name = models.CharField(max_length=20)
    ssid = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name


class DeviceSeries(models.Model):
    device_series_name = models.CharField(unique=True, max_length=30, null=True)
    num_lan = models.IntegerField(default=0, null=True)
    num_sim_slot = models.IntegerField(default=0, null=True)
    num_sd_card = models.IntegerField(default=0, null=True)
    cpu_arch = models.CharField(max_length=10, choices=CPUArchType.choices, null=True)

    def __str__(self) -> str:
        return self.device_series_name


class DeviceModel(models.Model):
    device_model_name = models.CharField(unique=True, max_length=30, null=True)
    device_series = models.ForeignKey(DeviceSeries, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.device_model_name


class Device(models.Model):
    serial_no = models.CharField(unique=True, max_length=20, primary_key=True)
    device_model = models.ForeignKey(DeviceModel, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10, choices=Status.choices, default="IDLE")
    mac_address = models.CharField(unique=True, max_length=17, null=True)
    ip = models.GenericIPAddressField(unique=True, null=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="devices_owned"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="devices_used"
    )
    testbed_wifi_ap = models.ForeignKey(
        TestbedWifiAP, null=True, blank=True, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.serial_no


class CellularModuleBrand(models.Model):
    brand = models.CharField(unique=True, max_length=20, null=True)

    def __str__(self) -> str:
        return self.brand


class CellularModuleModel(models.Model):
    model_name = models.CharField(unique=True, max_length=20, null=True)
    brand = models.ForeignKey(CellularModuleBrand, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.model_name


class CellularModule(models.Model):
    model = models.ForeignKey(CellularModuleModel, on_delete=models.CASCADE, null=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True, blank=True)
    imei = models.CharField(unique=True, max_length=20, null=True)
    module_id = models.IntegerField(null=True)

    def __str__(self) -> str:
        return f"IMEI:{self.imei}, Moudle: {self.model.model_name}"


class WifiModuleBrand(models.Model):
    brand = models.CharField(unique=True, max_length=20, null=True)

    def __str__(self) -> str:
        return self.brand


class WifiModuleModel(models.Model):
    model_name = models.CharField(unique=True, max_length=20, null=True)
    brand = models.ForeignKey(WifiModuleBrand, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.model_name


class WifiModule(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True, blank=True)
    serial_no = models.CharField(unique=True, max_length=30, null=True)
    model = models.ForeignKey(WifiModuleModel, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f"IMEI:{self.serial_no}, Moudle: {self.model.model_name}"


class SIM(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True, blank=True)
    serial_no = models.CharField(max_length=20, null=True, blank=True)
    sim_slot = models.IntegerField(null=True)
    pin_code = models.CharField(max_length=4, null=True)
    apn = models.CharField(max_length=20, null=True)
    operator = models.CharField(max_length=20, choices=SIMOperator.choices, null=True)
    iccid = models.CharField(unique=True, max_length=20, null=True)

    def __str__(self) -> str:
        return self.serial_no


class SDCard(models.Model):
    serial_no = models.CharField(max_length=20, null=True, blank=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True, blank=True)
    sd_card_slot = models.IntegerField(null=True)
    capability = models.IntegerField(null=True)

    def __str__(self) -> str:
        return f"SD card (serial NO: {self.serial_no})"


class TestbedNport(models.Model):
    ip = models.GenericIPAddressField(unique=True, null=True)
    name = models.CharField(max_length=20, null=True)

    def __str__(self) -> str:
        return f"Testbed Nport (ip: {self.ip})"


class NPortSerial(models.Model):
    com_port = models.IntegerField(null=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True, blank=True)
    nport = models.ForeignKey(
        TestbedNport, on_delete=models.CASCADE, null=True, blank=True
    )
    nport_port = models.IntegerField(null=True)
    cabel_model = models.CharField(
        max_length=10, choices=SerialModel.choices, null=True
    )
    baud_rate = models.IntegerField(choices=BaudRate.choices, null=True)
    mode = models.CharField(max_length=20, choices=NportMode.choices, null=True)

    def __str__(self) -> str:
        return f"Nport ip: {self.nport.ip}"


class TestbedAIE(models.Model):
    device = models.OneToOneField(
        Device, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=20, null=True, blank=True)
    encryption = models.CharField(
        max_length=10, choices=EncryptionType.choices, null=True, blank=True
    )
    identity_cert = models.CharField(max_length=100, null=True)
    identity_pk = models.CharField(max_length=100, null=True)
    identity_cer_content = models.CharField(max_length=100, null=True)
    identity_pk_content = models.CharField(max_length=100, null=True)
    downstream_certs_ca_cert_file = models.CharField(
        max_length=100, null=True, blank=True
    )
    downstream_certs_ca_pk_file = models.CharField(
        max_length=100, null=True, blank=True
    )
    downstream_certs_trusted_ca_file = models.CharField(
        max_length=100, null=True, blank=True
    )

    def __str__(self) -> str:
        return self.name


class TestbedSparkPlug(models.Model):
    device = models.OneToOneField(
        Device, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=20, null=True, blank=True)
    client_id = models.CharField(max_length=10, null=True)

    def __str__(self) -> str:
        return self.name


class TestbedAWS(models.Model):
    device = models.OneToOneField(
        Device, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=20, null=True, blank=True)
    host = models.CharField(max_length=50, null=True)

    def __str__(self) -> str:
        return self.name


class TestbedAID(models.Model):
    device = models.OneToOneField(
        Device, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=20, null=True, blank=True)
    encryption = models.CharField(
        max_length=10, choices=EncryptionType.choices, null=True
    )
    connection_string = models.CharField(max_length=100, null=True)
    root_ca_cert_file = models.CharField(max_length=100, null=True)
    ca_cert_file = models.CharField(max_length=100, null=True)
    ca_pk_file = models.CharField(max_length=100, null=True)

    def __str__(self) -> str:
        return self.name
