from netgazer.models import Device


def list_devices():
    devices = Device.objects.all()

    for device in devices:
        print(f"{device.name} ({device.ipv4})")
