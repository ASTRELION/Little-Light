from little_light import LittleLightClient

# Start bot & login
client = LittleLightClient()
client.run(client.config["token"], bot = True, reconnect = True)