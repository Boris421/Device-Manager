from rest_framework import serializers
from .models import (
    DeviceModel,
    Device,
    CellularModule,
    WifiModule,
    TestbedAIE,
    TestbedSparkPlug,
    TestbedAWS,
    TestbedAID,
    SIM,
    SDCard,
    NPortSerial,
)

from django.contrib.auth.models import User


class DeviceCapabilitySerializer(serializers.ModelSerializer):
    num_lan = serializers.CharField(source="device_series.num_lan")
    num_sim_slot = serializers.CharField(source="device_series.num_sim_slot")
    num_sd_card = serializers.CharField(source="device_series.num_sd_card")

    class Meta:
        model = DeviceModel
        fields = ["num_lan", "num_sim_slot", "num_sd_card"]


class DeviceSerializer(serializers.ModelSerializer):
    device_series = serializers.CharField(
        source="device_model.device_series.device_series_name"
    )
    model_name = serializers.CharField(source="device_model.device_model_name")
    user = serializers.CharField(source="user.username")
    owner = serializers.CharField(source="owner.username")
    cpu_arch = serializers.CharField(source="device_model.device_series.cpu_arch")
    capability = serializers.SerializerMethodField()
    testbed = serializers.SerializerMethodField()

    class Meta:
        model = Device
        fields = [
            "serial_no",
            "device_series",
            "model_name",
            "status",
            "ip",
            "mac_address",
            "user",
            "owner",
            "cpu_arch",
            "capability",
            "testbed",
        ]

    def get_capability(self, obj):
        return DeviceCapabilitySerializer(obj.device_model).data

    def get_testbed(self, obj):
        testbed = {
            "device": self.get_testbed_device(obj),
            "cloud": self.get_testbed_could(obj),
        }
        return testbed

    def get_testbed_device(self, obj):
        testbed_device = {
            "cellular": self.get_cellular_module(obj),
            "wifi_module": self.get_wifi_module(obj),
            "sim": self.get_sim(obj),
            "wifi_client": self.get_wifi_client(obj),
            "serial": self.get_serial(obj),
            "sd_card": self.get_sd_card(obj),
        }
        return testbed_device

    def get_testbed_could(self, obj):
        testbed_cloud = {
            "aws": self.get_testbed_aws(obj),
            "aie": self.get_testbed_aie(obj),
            "aid": self.get_testbed_aid(obj),
            "sparkplug": self.get_testbed_sparkplug(obj),
        }
        return testbed_cloud

    def get_sd_card(self, obj):
        sd_cards = SDCard.objects.filter(device=obj)
        sd_card_data = []
        for sd_card in sd_cards:
            sd_card_data.append(
                {
                    "sd_card_slot": sd_card.sd_card_slot,
                    "capability": sd_card.capability,
                }
            )
        return sd_card_data

    def get_cellular_module(self, obj):
        cellular_modules = CellularModule.objects.filter(device=obj)
        cellular_module_data = []
        for cellular_module in cellular_modules:
            cellular_module_data.append(
                {
                    "module_id": cellular_module.module_id,
                    "imei": cellular_module.imei,
                    "brand": cellular_module.model.brand.brand,
                    "model_name": cellular_module.model.model_name,
                }
            )
        return cellular_module_data

    def get_sim(self, obj):
        sims = SIM.objects.filter(device=obj)
        sim_data = []
        for sim in sims:
            sim_data.append(
                {
                    "slot": sim.sim_slot,
                    "pin_coded": sim.pin_code,
                    "apn": sim.apn,
                    "operator": sim.operator,
                    "iccid": sim.iccid,
                }
            )
        return sim_data

    def get_wifi_module(self, obj):
        wifi_modules = WifiModule.objects.filter(device=obj)
        wifi_module_data = []
        for wifi_module in wifi_modules:
            wifi_module_data.append(
                {
                    "brand": wifi_module.model.brand.brand,
                    "model_name": wifi_module.model.model_name,
                }
            )
        return wifi_module_data

    def get_wifi_client(self, obj):
        testbed_wifi_ap = obj.testbed_wifi_ap
        testbed_wifi_ap_data = []
        if testbed_wifi_ap:
            testbed_wifi_ap_data.append(
                {
                    "ssid": testbed_wifi_ap.ssid,
                    "password": testbed_wifi_ap.password,
                }
            )
        return testbed_wifi_ap_data

    def get_serial(self, obj):
        nport_serials = NPortSerial.objects.filter(device=obj)
        nport_serial_data = []
        for nport_serial in nport_serials:
            nport_serial_data.append(
                {
                    "com_port": nport_serial.com_port,
                    "nport_ip": nport_serial.nport.ip,
                    "nport_port": nport_serial.nport_port,
                    "cable_model": nport_serial.cabel_model,
                    "baudrate": nport_serial.baud_rate,
                }
            )
        return nport_serial_data

    def get_testbed_aws(self, obj):
        testbed_aws = TestbedAWS.objects.filter(device=obj).first()
        if testbed_aws:
            testbed_aws_data = {"host": testbed_aws.host}
        else:
            testbed_aws_data = {}
        return testbed_aws_data

    def get_testbed_aid(self, obj):
        testbed_aids = TestbedAID.objects.filter(device=obj)
        testbed_aid_data = {}
        for testbed_aid in testbed_aids:
            testbed_aid_data[testbed_aid.encryption] = {
                "connectionString": testbed_aid.connection_string,
                "certificate_files": {
                    "rootCaCertFile": testbed_aid.root_ca_cert_file,
                    "caCertFile": testbed_aid.ca_cert_file,
                    "caPkFile": testbed_aid.ca_pk_file,
                },
            }

        return testbed_aid_data

    def get_testbed_aie(self, obj):
        testbed_aie = TestbedAIE.objects.filter(device=obj).first()
        if testbed_aie:
            testbed_aie_data = {
                "identityCert": testbed_aie.identity_cert,
                "identityPk": testbed_aie.identity_pk,
                "identityCertContent": testbed_aie.identity_cer_content,
                "identityPkContent": testbed_aie.identity_pk_content,
                "downstreamCerts": {
                    "caCertFile": testbed_aie.downstream_certs_ca_cert_file,
                    "caPkFile": testbed_aie.downstream_certs_ca_pk_file,
                    "trustedCaFile": testbed_aie.downstream_certs_trusted_ca_file,
                },
            }
        else:
            testbed_aie_data = {}
        return testbed_aie_data

    def get_testbed_sparkplug(self, obj):
        testbed_sparkplug = TestbedSparkPlug.objects.filter(device=obj).first()
        if testbed_sparkplug:
            testbed_sparkplug_data = {"clientID": testbed_sparkplug.client_id}
        else:
            testbed_sparkplug_data = {}
        return testbed_sparkplug_data

    def update(self, instance, validated_data):
        # user is foreign key, handle to update user object.
        user_data = validated_data.pop("user", None)
        instance = super().update(instance, validated_data)

        if user_data:
            user_name = user_data.get("username", None)
            user = User.objects.get(username=user_name)
            instance.user = user
            instance.save()

        return instance
