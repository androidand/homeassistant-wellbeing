from .api_models import Appliance, Mode

class CustomComponent:
    def get_translation(self, key):
        return translations.get(key, key)

    def get_entity(self, entity_type, entity_attr):
        return next(
            entity
            for entity in self.entities
            if entity.attr == entity_attr and entity.entity_type == entity_type
        )

    def clear_mode(self):
        self.mode = Mode.UNDEFINED

    def setup(self, data):
        self.firmware = data.get('FrmVer_NIU')
        self.mode = Mode(data.get('Workmode'))
        self.entities = [
            entity.setup(data)
            for entity in Appliance._create_entities(data) if entity.attr in data
        ]

    @property
    def speed_range(self) -> tuple:
        ## Electrolux Air Purifier Devices:
        if self.model == "WELLA5":
            return 1, 5
        if self.model == "WELLA7":
            return 1, 5
        if self.model == "PUREA9":
            return 1, 9


        ## AEG Air Purifier Devices:
        if self.model == "AX5":
            return 1, 5
        if self.model == "AX7":
            return 1, 5
        if self.model == "AX9":
            return 1, 9

        return 0, 0