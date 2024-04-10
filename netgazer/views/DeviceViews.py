from django.shortcuts import render

from netgazer.models import Device, Neighbor


def device_map(request):

    devices = Device.objects.all()
    neighbors = Neighbor.objects.all()

    mapped_devices = [{
        'id': device.name,
        'label': device.name,
        'url': device.get_absolute_url(),
    } for device in devices]

    mapped_neighbors = [{
        'source': neighbor.device.name,
        'target': neighbor.neighbor_device.name,
    } for neighbor in neighbors if neighbor.device and neighbor.device.name and neighbor.neighbor_device and neighbor.neighbor_device.name]

    for unknown_neighbor in neighbors:
        if unknown_neighbor.neighbor_device == None:
            mapped_devices.append({
                'id': unknown_neighbor.name,
                'label': unknown_neighbor.name,
                'url': '#',
            })
            mapped_neighbors.append({
                'source': unknown_neighbor.device.name,
                'target': unknown_neighbor.name,
            })

    return render(request, 'netgazer/map_view.html', {
        'devices': mapped_devices,
        'edges': mapped_neighbors,
    })
