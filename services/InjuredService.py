import json
import os

class InjuredService:
    def __init__(self, filename):
        self.filename = "data/" + filename
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                f.write(json.dumps({
                    "UR": 0,
                    "UA": 0,
                    "Delta": 0
                    }))
                f.close()

    def getInjured(self):
        with open(self.filename, "r") as f:
            return json.load(f)
        
    def setUR(self, value):
        with open(self.filename, "r") as f:
            data = json.load(f)
            data["UR"] = value
            f.close()
        with open(self.filename, "w") as f:
            json.dump(data, f)
            f.close()

    def addUR(self):
        with open(self.filename, "r") as f:
            data = json.load(f)
            data["UR"] += 1
            f.close()
        with open(self.filename, "w") as f:
            json.dump(data, f)
            f.close()

    def removeUR(self):
        with open(self.filename, "r") as f:
            data = json.load(f)
            if data["UR"] > 0:
                data["UR"] -= 1
            else:
                return False
            f.close()
        with open(self.filename, "w") as f:
            json.dump(data, f)
            f.close()
        return True

    def setUA(self, value):
        with open(self.filename, "r") as f:
            data = json.load(f)
            data["UA"] = value
            f.close()
        with open(self.filename, "w") as f:
            json.dump(data, f)
            f.close()

    def addUA(self):
        with open(self.filename, "r") as f:
            data = json.load(f)
            data["UA"] += 1
            f.close()
        with open(self.filename, "w") as f:
            json.dump(data, f)
            f.close()

    def removeUA(self):
        with open(self.filename, "r") as f:
            data = json.load(f)
            if data["UA"] > 0:
                data["UA"] -= 1
            else:
                return False
            f.close()
        with open(self.filename, "w") as f:
            json.dump(data, f)
            f.close()
        return True

    def setDelta(self, value):
        with open(self.filename, "r") as f:
            data = json.load(f)
            data["Delta"] = value
            f.close()
        with open(self.filename, "w") as f:
            json.dump(data, f)
            f.close()

    def addDelta(self):
        with open(self.filename, "r") as f:
            data = json.load(f)
            data["Delta"] += 1
            f.close()
        with open(self.filename, "w") as f:
            json.dump(data, f)
            f.close()

    def removeDelta(self):
        with open(self.filename, "r") as f:
            data = json.load(f)
            if data["Delta"] > 0:
                data["Delta"] -= 1
            else:
                return False
            f.close()
        with open(self.filename, "w") as f:
            json.dump(data, f)
            f.close()
        return True

    def reset(self):
        with open(self.filename, "w") as f:
            f.write(json.dumps({
                "UR": 0,
                "UA": 0,
                "Delta": 0
                }))
            f.close()

    def getUR(self):
        with open(self.filename, "r") as f:
            data = json.load(f)
            return data["UR"]
            f.close()

    def getUA(self):
        with open(self.filename, "r") as f:
            data = json.load(f)
            return data["UA"]
            f.close()

    def getDelta(self):
        with open(self.filename, "r") as f:
            data = json.load(f)
            return data["Delta"]
            f.close()