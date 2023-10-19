class Formatter:
    MESSAGES = {
        'pt_BR': {'all_fields': 'PREENCHA TODOS OS CAMPOS'},
        'en_US': {'all_fields': 'FILL IN ALL FIELDS'}
    }
    def formmatt_text_label_language(self, language: str, field: str) -> str:
        return self.MESSAGES[language][field]