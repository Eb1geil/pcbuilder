from django.shortcuts import render
from django.http import JsonResponse
from pc_builder_core.models import Motherboard, CPU, GPU, RAM, Storage

def motherboard_list_view(request):
    motherboards = Motherboard.objects.all()
    return render(request, "pc_builder_core/motherboard_view.html", {"motherboards": motherboards})

def select_motherboard(request):
    motherboards = Motherboard.objects.all()  # Получаем все материнские платы
    return render(request, 'pc_builder_core/select_motherboard.html', {'motherboards': motherboards})

def motherboard_detail_view(request, motherboard_id):
    try:
        motherboard = Motherboard.objects.get(id=motherboard_id)
    except Motherboard.DoesNotExist:
        return render(request, "pc_builder_core/404.html")  # Страница ошибки, если плата не найдена

    # Подготовим только нужные поля для сериализации
    motherboard_data = {
        'id': motherboard.id,
        'model': motherboard.model,
        'price': motherboard.price,
        'socket': motherboard.socket,
        # Добавьте другие поля, если необходимо
    }

    # Передаем данные как JSON
    return render(
        request,
        'pc_builder_core/motherboard_detail.html',
        {'motherboard': motherboard, 'motherboard_data': motherboard_data}
    )


def motherboard_detail_view(request, motherboard_id):
    try:
        motherboard = Motherboard.objects.get(id=motherboard_id)
    except Motherboard.DoesNotExist:
        return render(request, "pc_builder_core/404.html")  # Страница ошибки, если плата не найдена

    return render(request, 'pc_builder_core/motherboard_detail.html', {'motherboard': motherboard})

def filter_components_by_motherboard(request, motherboard_id, component_type):
    try:
        motherboard = Motherboard.objects.get(id=motherboard_id)
    except Motherboard.DoesNotExist:
        return JsonResponse({"error": "Материнская плата не найдена"}, status=404)

    if component_type == "cpu":
        # Фильтруем процессоры по сокету
        components = CPU.objects.filter(socket=motherboard.socket)
        response_data = [
            {
                "id": cpu.id,
                "brand": cpu.brand,
                "line": cpu.line,
                "model": cpu.model,
                "socket": cpu.socket,
                "cores": cpu.cores,
                "threads": cpu.threads,
                "max_frequency": str(cpu.max_frequency) if cpu.max_frequency else None,
                "base_frequency": str(cpu.base_frequency) if cpu.base_frequency else None,
                "benchmark": cpu.benchmark,
                "price": str(cpu.price) if cpu.price else "Цена не указана",
                "ref": cpu.ref,
            }
            for cpu in components
        ]
    elif component_type == "ram":
        # Фильтруем оперативную память по частоте
        components = RAM.objects.all()
        response_data = [
            {
                "id": ram.id,
                "brand": ram.brand,
                "model": ram.model,
                "frequency": ram.frequency,
                "memory": ram.memory,
                "voltage": ram.voltage,
                "price": str(ram.price) if ram.price else "Цена не указана",
                "ref": ram.ref,
            }
            for ram in components
        ]
    elif component_type == "gpu":
        # GPU без фильтрации
        components = GPU.objects.all()
        response_data = [
            {
                "id": gpu.id,
                "brand": gpu.brand,
                "model": gpu.model,
                "manufacturer": gpu.manufacturer,
                "rank": gpu.rank,
                "benchmark": gpu.benchmark,
                "memory": gpu.memory,
                "memorytype": gpu.memorytype,
                "interface": gpu.interface,
                "energy": gpu.energy,
                "price": str(gpu.price) if gpu.price else "Цена не указана",
                "ref": gpu.ref,
            }
            for gpu in components
        ]
    elif component_type == "storage":
        # Storage без фильтрации
        components = Storage.objects.all()
        response_data = [
            {
                "id": storage.id,
                "brand": storage.brand,
                "model": storage.model,
                "memory": storage.memory,
                "benchmark": storage.benchmark,
                "price": str(storage.price) if storage.price else "Цена не указана",
                "ref": storage.ref,
            }
            for storage in components
        ]
    else:
        return JsonResponse({"error": "Неподдерживаемый тип компонента"}, status=400)

    return JsonResponse({"components": response_data})

def get_preset(request, motherboard_id, preset_type):
    try:
        motherboard = Motherboard.objects.get(id=motherboard_id)
        components = []

        if preset_type == 'budget':
            # Get the cheapest CPU compatible with the motherboard socket
            components.append(CPU.objects.filter(socket=motherboard.socket).order_by('price').first())
            # Get the cheapest GPU compatible with the motherboard socket
            components.append(GPU.objects.filter(price__isnull=False).order_by('price').first())
            # Get the cheapest RAM compatible with the motherboard (no direct link in models)
            components.append(RAM.objects.all().order_by('price').first())
            # Get the cheapest storage
            components.append(Storage.objects.filter(price__isnull=False).order_by('price').first())

        elif preset_type == 'maximum':
            # Get the most expensive CPU compatible with the motherboard socket
            components.append(CPU.objects.filter(socket=motherboard.socket).order_by('-price').first())
            # Get the most expensive GPU
            components.append(GPU.objects.filter(price__isnull=False).order_by('-price').first())
            # Get the most expensive RAM
            components.append(RAM.objects.all().order_by('-price').first())
            # Get the most expensive storage
            components.append(Storage.objects.filter(price__isnull=False).order_by('-price').first())

        elif preset_type == 'work':
            # Get a mid-range CPU (second cheapest)
            components.append(CPU.objects.filter(socket=motherboard.socket).order_by('price')[1])
            # Get a mid-range GPU (second cheapest)
            components.append(GPU.objects.filter(price__isnull=False).order_by('price')[1])
            # Get a mid-range RAM (second cheapest)
            components.append(RAM.objects.all().order_by('price')[1])
            # Get a mid-range storage (second cheapest)
            components.append(Storage.objects.filter(price__isnull=False).order_by('price')[1])

        elif preset_type == 'render':
            # Get a high-end Intel CPU (best for rendering)
            components.append(CPU.objects.filter(socket=motherboard.socket, brand__icontains='Intel').order_by('-price').first())
            # Get the most expensive GPU
            components.append(GPU.objects.filter(price__isnull=False).order_by('-price').first())
            # Get the most expensive RAM
            components.append(RAM.objects.all().order_by('-price').first())
            # Get the most expensive storage
            components.append(Storage.objects.filter(price__isnull=False).order_by('-price').first())

        # Prepare component data for response
        components_data = [{
            'type': type(c).__name__.lower(),  # Get the type of the component (CPU, GPU, etc.)
            'model': c.model,
            'price': str(c.price) if c.price else "Цена не указана",
            'ref': c.ref,
            'memory': getattr(c, 'memory', None),  # Only include 'memory' if it exists
            'cores': getattr(c, 'cores', None),   # Only include 'cores' if it exists
            'base_frequency': getattr(c, 'base_frequency', None),  # Only include 'base_frequency' if it exists
        } for c in components if c]

        return JsonResponse({'components': components_data})

    except Motherboard.DoesNotExist:
        return JsonResponse({"error": "Материнская плата не найдена"}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
