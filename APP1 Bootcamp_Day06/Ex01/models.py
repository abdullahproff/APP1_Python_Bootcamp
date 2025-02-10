from pydantic import BaseModel, field_validator, ValidationError
from typing import List, Optional

# Модель для офицера
class Officer(BaseModel):
    first_name: str
    last_name: str
    rank: str

# Модель для корабля
class Spaceship(BaseModel):
    alignment: str
    name: str
    ship_class: str
    length: float
    crew_size: int
    armed: bool
    officers: List[Officer]

    # Валидация имени (Unknown только для врагов)
    @field_validator('name')
    def validate_name(cls, value, info):
        alignment = info.data.get('alignment')
        if value == 'Unknown' and alignment != 'Enemy':
            raise ValueError("Name can be 'Unknown' only for enemy ships.")
        return value

    # Валидация параметров корабля в зависимости от класса
    @field_validator('length', 'crew_size', 'armed')
    def validate_ship_params(cls, value, info):
        field_name = info.field_name
        ship_class = info.data.get('ship_class')
        if not ship_class:
            return value

        # Правила для каждого класса кораблей
        rules = {
            'Corvette': {'length': (80, 250), 'crew_size': (4, 10), 'armed': True},
            'Frigate': {'length': (300, 600), 'crew_size': (10, 15), 'armed': True},
            'Cruiser': {'length': (500, 1000), 'crew_size': (15, 30), 'armed': True},
            'Destroyer': {'length': (800, 2000), 'crew_size': (50, 80), 'armed': True},
            'Carrier': {'length': (1000, 4000), 'crew_size': (120, 250), 'armed': False},
            'Dreadnought': {'length': (5000, 20000), 'crew_size': (300, 500), 'armed': True},
        }

        if ship_class not in rules:
            raise ValueError(f"Unknown ship class: {ship_class}")

        rule = rules[ship_class]

        if field_name == 'length' and not (rule['length'][0] <= value <= rule['length'][1]):
            raise ValueError(f"Invalid length for {ship_class}: {value}")

        if field_name == 'crew_size' and not (rule['crew_size'][0] <= value <= rule['crew_size'][1]):
            raise ValueError(f"Invalid crew size for {ship_class}: {value}")

        if field_name == 'armed' and value != rule['armed']:
            raise ValueError(f"Invalid armed status for {ship_class}: {value}")

        return value