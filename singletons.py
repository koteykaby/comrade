import json

# Configuration files
# Reliclink config is the in-game menus configuration. You can edit it and disable, for example, shop or news
servicesConfig = json.load(open("config/services.json"))
reliclinkConfig = json.load(open("config/reliclink.json"))

achievements = json.load(open("resources/achievements.json"))

# Load resources folder (responses that are static)
automatchMap = json.load(open("resources/automatchMap.json"))
itemDefinitionsJson = json.load(open("resources/itemDefinitionsJson.json"))
availableAchievements = json.load(open("resources/availableAchievements.json"))
availableLeaderboards = json.load(open("resources/availableLeaderboards.json"))
itemBundleItemsJson = json.load(open("resources/itemBundleItemsJson.json"))
itemLocations = json.load(open("resources/ItemLocations.json"))