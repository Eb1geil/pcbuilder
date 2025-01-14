from django.contrib import admin
from pc_builder_core.models import Motherboard, CPU, GPU, RAM, Storage

@admin.register(Motherboard)
class MotherboardAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'socket', 'chipset', 'memoryfr', 'price', 'ref')
    search_fields = ['brand', 'model', 'socket']

@admin.register(CPU)
class CPUAdmin(admin.ModelAdmin):
    list_display = ('brand', 'line', 'model', 'price', 'socket', 'cores', 'threads', 'max_frequency', 'benchmark')
    search_fields = ['brand', 'line', 'model', 'socket']

@admin.register(GPU)
class GPUAdmin(admin.ModelAdmin):
    list_display = ('brand', 'manufacturer', 'model', 'price', 'benchmark', 'memory', 'memorytype', 'interface', 'ref')
    search_fields = ['brand', 'model', 'manufacturer']

@admin.register(RAM)
class RAMAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'memory', 'frequency', 'voltage', 'price', 'ref')
    search_fields = ['brand', 'model', 'memory', 'frequency']

@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'memory', 'price', 'benchmark','ref')
    search_fields = ['brand', 'model', 'memory']
