from core.models import *

class Session:
    current_user = None

    doctors         : list[Doctor]         = []
    patients        : list[Patient]        = []
    solid_medicines : list[SolidMedicine]  = []
    liquid_medicines: list[LiquidMedicine] = []