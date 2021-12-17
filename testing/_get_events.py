import evdev

devices = [evdev.InputDevice(p) for p in evdev.list_devices()]
for device in devices:
    print(device.path, device.name, device.phys)