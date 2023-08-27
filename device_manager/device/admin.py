from django.contrib import admin
from .models import (
    TestbedNport,
    CellularModuleBrand,
    CellularModuleModel,
    WifiModuleBrand,
    WifiModuleModel,
    DeviceSeries,
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
    TestbedWifiAP,
)


def get_field_names(model):
    return [field.name for field in model._meta.fields]


class TestbedNportInline(admin.TabularInline):
    model = TestbedNport
    extra = 0


class CellularModuleInline(admin.TabularInline):
    model = CellularModule
    extra = 0


class WifiModuleInline(admin.TabularInline):
    model = WifiModule
    extra = 0


class TestbedAIEInline(admin.StackedInline):
    model = TestbedAIE
    extra = 0


class TestbedSparkPlugInline(admin.StackedInline):
    model = TestbedSparkPlug
    extra = 0


class TestbedAWSInline(admin.StackedInline):
    model = TestbedAWS
    extra = 0


class TestbedAIDInline(admin.StackedInline):
    model = TestbedAID
    extra = 0


class SIMInline(admin.TabularInline):
    model = SIM
    extra = 0


class SDCardInline(admin.TabularInline):
    model = SDCard
    extra = 0


class NPortSerialInline(admin.TabularInline):
    model = NPortSerial
    extra = 0


class CellularModuleModelInline(admin.TabularInline):
    model = CellularModuleModel
    extra = 0


class WifiModuleModelInline(admin.TabularInline):
    model = WifiModuleModel
    extra = 0


class DeviceModelInline(admin.TabularInline):
    model = DeviceModel
    extra = 0


class DeviceInline(admin.TabularInline):
    model = Device
    extra = 0


class WifiModuleModelInline(admin.TabularInline):
    model = WifiModuleModel
    extra = 0


class CellularModuleBrandAdmin(admin.ModelAdmin):
    inlines = [CellularModuleModelInline]
    list_display = get_field_names(CellularModuleBrand)
    search_fields = get_field_names(CellularModuleBrand)


class CellularModuleModelAdmin(admin.ModelAdmin):
    list_display = get_field_names(CellularModuleModel)
    search_fields = get_field_names(CellularModuleModel)
    inlines = [CellularModuleInline]


class WifiModuleBrandAdmin(admin.ModelAdmin):
    list_display = get_field_names(WifiModuleBrand)
    search_fields = get_field_names(WifiModuleBrand)
    inlines = [WifiModuleModelInline]


class WifiModuleModelAdmin(admin.ModelAdmin):
    list_display = get_field_names(WifiModuleModel)
    search_fields = get_field_names(WifiModuleModel)
    inlines = [WifiModuleInline]


class DeviceSeriesAdmin(admin.ModelAdmin):
    list_display = get_field_names(DeviceSeries)
    search_fields = get_field_names(DeviceSeries)
    inlines = [DeviceModelInline]


class DeviceModelAdmin(admin.ModelAdmin):
    list_display = get_field_names(DeviceModel)
    search_fields = get_field_names(DeviceModel)
    inlines = [DeviceInline]


class DeviceAdmin(admin.ModelAdmin):
    list_display = get_field_names(Device)
    search_fields = get_field_names(Device)
    inlines = [
        CellularModuleInline,
        WifiModuleInline,
        TestbedAIEInline,
        TestbedSparkPlugInline,
        TestbedAWSInline,
        TestbedAIDInline,
        SIMInline,
        SDCardInline,
        NPortSerialInline,
    ]


class TestbedNportAdmin(admin.ModelAdmin):
    list_display = get_field_names(TestbedNport)
    search_fields = get_field_names(TestbedNport)
    inlines = [NPortSerialInline]


class CellularModuleAdmin(admin.ModelAdmin):
    list_display = get_field_names(CellularModule)
    search_fields = get_field_names(CellularModule)


class WifiModuleAdmin(admin.ModelAdmin):
    list_display = get_field_names(WifiModule)
    search_fields = get_field_names(WifiModule)


class TestbedAIEAdmin(admin.ModelAdmin):
    list_display = get_field_names(TestbedAIE)
    search_fields = get_field_names(TestbedAIE)


class TestbedSparkPlugAdmin(admin.ModelAdmin):
    list_display = get_field_names(TestbedSparkPlug)
    search_fields = get_field_names(TestbedSparkPlug)


class TestbedAWSAdmin(admin.ModelAdmin):
    list_display = get_field_names(TestbedAWS)
    search_fields = get_field_names(TestbedAWS)


class TestbedAIDAdmin(admin.ModelAdmin):
    list_display = get_field_names(TestbedAID)
    search_fields = get_field_names(TestbedAID)


class SIMAdmin(admin.ModelAdmin):
    list_display = get_field_names(SIM)
    search_fields = get_field_names(SIM)


class SDCardAdmin(admin.ModelAdmin):
    list_display = get_field_names(SDCard)
    search_fields = get_field_names(SDCard)


class NPortSerialAdmin(admin.ModelAdmin):
    list_display = get_field_names(NPortSerial)
    search_fields = get_field_names(NPortSerial)


class TestbedWifiAPAdmin(admin.ModelAdmin):
    list_display = get_field_names(TestbedWifiAP)
    search_fields = get_field_names(TestbedWifiAP)
    inlines = [DeviceInline]


# Register all models with their respective admin classes
admin.site.register(TestbedNport, TestbedNportAdmin)
admin.site.register(CellularModuleBrand, CellularModuleBrandAdmin)
admin.site.register(CellularModuleModel, CellularModuleModelAdmin)
admin.site.register(WifiModuleBrand, WifiModuleBrandAdmin)
admin.site.register(WifiModuleModel, WifiModuleModelAdmin)
admin.site.register(DeviceSeries, DeviceSeriesAdmin)
admin.site.register(DeviceModel, DeviceModelAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(CellularModule, CellularModuleAdmin)
admin.site.register(WifiModule, WifiModuleAdmin)
admin.site.register(TestbedAIE, TestbedAIEAdmin)
admin.site.register(TestbedSparkPlug, TestbedSparkPlugAdmin)
admin.site.register(TestbedAWS, TestbedAWSAdmin)
admin.site.register(TestbedAID, TestbedAIDAdmin)
admin.site.register(SIM, SIMAdmin)
admin.site.register(SDCard, SDCardAdmin)
admin.site.register(NPortSerial, NPortSerialAdmin)
admin.site.register(TestbedWifiAP, TestbedWifiAPAdmin)
