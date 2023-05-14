import re
from services.ObjectsService import DocteurObj, AgentObj

class RegexUtils:
    def doctorToList(string, grade):
        docs = []
        regex = r"\d{2}/\d{2}/\d{4}\s-\s\d{3}-\d{4}\s(?P<first_name>[A-Z][a-z]*)\s(?P<last_name>(?:[A-Z][a-z]*\s*)+$)"
        matches = re.finditer(regex, string, re.MULTILINE)
        for _, match in enumerate(matches, start=1):
            doc = DocteurObj(0, match.group('last_name'), match.group('first_name'), grade, False, False, False, False)
            docs.append(doc)
        return docs
    
    def agentToList(string, grade):
        agents = []
        regex = r"\d{2}/\d{2}/\d{4}\s-\s\d{3}-\d{4}\s(?P<first_name>[A-Z][a-z]*)\s(?P<last_name>(?:[A-Z][a-z]*\s*)+$)"
        matches = re.finditer(regex, string, re.MULTILINE)
        for _, match in enumerate(matches, start=1):
            agent = AgentObj(0, match.group('last_name'), match.group('first_name'), grade, False, False, False, False)
            agents.append(agent)
        return agents
    
    def doctorToString(string, grade):
        regex = r"(?P<first_name>[A-Z][a-z]*)\s(?P<last_name>(?:[A-Z][a-z]*\s*)+$)"
        matches = re.finditer(regex, string, re.MULTILINE)
        for _, match in enumerate(matches, start=1):
            return DocteurObj(0, match.group('last_name'), match.group('first_name'), grade, False, False, False, False)
        
    def agentToString(string, grade):
        regex = r"(?P<first_name>[A-Z][a-z]*)\s(?P<last_name>(?:[A-Z][a-z]*\s*)+$)"
        matches = re.finditer(regex, string, re.MULTILINE)
        for _, match in enumerate(matches, start=1):
            return AgentObj(0, match.group('last_name'), match.group('first_name'), grade, False, False, False, False)

    