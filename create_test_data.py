#!/usr/bin/env python
"""
Script to create test data for CleanTrack
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cleantrack.settings')
django.setup()

from apps.facilities.models import Facility
from apps.equipment.models import Equipment

# Create a test facility
facility, created = Facility.objects.get_or_create(
    name="Hospital Central",
    defaults={
        "address": "Rua Principal, 123",
        "is_active": True
    }
)

if created:
    print(f"✓ Facility created: {facility.name} (ID: {facility.id})")
else:
    print(f"✓ Facility already exists: {facility.name} (ID: {facility.id})")

# Create test equipment
equipment_data = [
    {
        "name": "Ventilador Mecânico VM-01",
        "serial_number": "VM-001-2024",
        "category": "life_support",
        "location": "UTI - Leito 1",
        "cleaning_frequency_hours": 8,
        "description": "Ventilador mecânico de última geração"
    },
    {
        "name": "Monitor Cardíaco MC-02",
        "serial_number": "MC-002-2024",
        "category": "monitoring",
        "location": "UTI - Leito 2",
        "cleaning_frequency_hours": 4,
        "description": "Monitor multiparamétrico"
    },
    {
        "name": "Bomba de Infusão BI-03",
        "serial_number": "BI-003-2024",
        "category": "life_support",
        "location": "Enfermaria - Sala 101",
        "cleaning_frequency_hours": 24,
        "description": "Bomba de infusão programável"
    },
    {
        "name": "Ultrassom US-04",
        "serial_number": "US-004-2024",
        "category": "diagnostic",
        "location": "Centro de Diagnóstico",
        "cleaning_frequency_hours": 24,
        "description": "Ultrassom de alta resolução"
    },
    {
        "name": "Mesa Cirúrgica MS-05",
        "serial_number": "MS-005-2024",
        "category": "surgical",
        "location": "Centro Cirúrgico - Sala 1",
        "cleaning_frequency_hours": 4,
        "description": "Mesa cirúrgica elétrica"
    }
]

print("\nCreating equipment...")
for data in equipment_data:
    equipment, created = Equipment.objects.get_or_create(
        serial_number=data["serial_number"],
        defaults={
            "facility": facility,
            "name": data["name"],
            "category": data["category"],
            "location": data["location"],
            "cleaning_frequency_hours": data["cleaning_frequency_hours"],
            "description": data["description"],
            "is_active": True
        }
    )

    if created:
        print(f"  ✓ {equipment.name} - {equipment.serial_number}")
    else:
        print(f"  → {equipment.name} - {equipment.serial_number} (already exists)")

print(f"\n{'='*60}")
print(f"✓ Test data created successfully!")
print(f"{'='*60}")
print(f"\nFacility ID: {facility.id}")
print(f"Total Equipment: {Equipment.objects.filter(facility=facility).count()}")
print(f"\n🔗 Test the PDF endpoint at:")
print(f"   http://localhost:8000/equipment/labels/pdf/{facility.id}/")
print(f"{'='*60}\n")
