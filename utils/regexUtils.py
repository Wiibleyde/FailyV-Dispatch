import re
from services.ObjectsService import DocteurObj

class RegexUtils:
    def doctorToList(string, grade):
        docs = []
        regex = r"\d{2}/\d{2}/\d{4}\s-\s\d{3}-\d{4}\s(?P<first_name>[A-Z][a-z]*)\s(?P<last_name>(?:[A-Z][a-z]*\s*)+$)"
        matches = re.finditer(regex, string, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            doc = DocteurObj(0, match.group('last_name'), match.group('first_name'), grade, False, False, False, False)
            docs.append(doc)
        return docs
    
    def doctorToString(string, grade):
        regex = r"(?P<first_name>[A-Z][a-z]*)\s(?P<last_name>(?:[A-Z][a-z]*\s*)+$)"
        matches = re.finditer(regex, string, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            return DocteurObj(0, match.group('last_name'), match.group('first_name'), grade, False, False, False, False)
    