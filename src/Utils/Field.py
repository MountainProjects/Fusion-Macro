from pysondb import db

class Field():
    def __init__(self, macro):
        self.macro = macro
        self.database = db.getDb("src/Field_Data.json")
    
    def start(self):
        Fields = self.database.getAll()
        for field in Fields:
            self.macro.fields[field["name"]] = field

    def get(self, name):
        """
        Получает данные поля по имени.
        :param name: Имя поля
        :return: Данные поля или None, если поле не найдено
        """
        if not name:
            return None
        
        field = self.database.getBy({"name": name})
        return field[0] if field else None
    
    def get_paths(self, name):
        """
        Получает пути для указанного поля.
        :param name: Имя поля
        :return: Список путей или None, если поле не найдено
        """
        field = self.get(name)
        if not field:
            return None
        
        paths = field.get("paths", [])
        path_ids = [path.get("id") for path in paths if "id" in path]
        return path_ids
    
    def get_patterns(self, name):
        """
        Получает паттерны для указанного поля.
        :param name: Имя поля
        :return: Список паттернов или None, если поле не найдено
        """
        field = self.get(name)
        if not field:
            return None
        
        patterns = field.get("patterns", [])
        pattern_ids = [pattern.get("id") for pattern in patterns if "id" in pattern]
        return pattern_ids