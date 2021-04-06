from data.models import Shipment


class ShipmentDalModel:
    provider: str
    tracking_code: str

    def __init__(self, provider, tracking_code) -> None:
        self.provider = provider
        self.tracking_code = tracking_code

    @staticmethod
    def create_from_model(model: Shipment):
        return ShipmentDalModel(model.provider, model.tracking_code)
