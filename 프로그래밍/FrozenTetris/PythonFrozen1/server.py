from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
from time import sleep

class ClientChannel(Channel):
    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)

    def Close(self):
        self._server.DelPlayer(self)

    def Network_fezMove(self, data):
        self._server.FezMove(data["move"], data["turn"])

    def Network_fezPos(self, data):
        self._server.FezPos(data["x"], data["y"], data["jump"])

class FrozenServer(Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)  # create server
        print("server accept")
        
        self.queue = None
        self.currentIdx = 0

    def Connected(self, channel, addr):
        print('new connection:', str(channel.addr))

        if self.queue == None:         # 첫번째 유저
            print("First User")
            self.queue = Game(channel, self.currentIdx)
            self.currentIdx += 1
        else:      # 두번째 유저
            print("Second User")
            self.queue.player1 = channel
            self.queue.player0.Send({"action": "gameStart", "gameid":0})    # fez
            self.queue.player1.Send({"action": "gameStart", "gameid":1})    # block

    def DelPlayer(self, player):
        print("Deleting Player" + str(player.addr))
        # 변수 리셋
        self.queue = None
        self.currentIdx = 0
        exit()

    def PrintStr(self, str):
        print(str)

    def FezMove(self, move, turn):
        # player0의 움직임을 player1에게 전달
        self.queue.player1.Send({"action": "fezMove", "move":move, "turn":turn})
 
    def FezPos(self, x, y, jump):
        self.queue.player1.Send({"action": "fezPos", "x":x, "y":y, "jump":jump})

    def tick(self):
        while True:
            self.Pump()
            sleep(0.01)

class Game:
    def __init__(self, player0, currentIndex):
        self.turn = 0
        self.player0 = player0
        self.player1 = None
        self.gameid = currentIndex


print("STARTING SERVER ON LOCALHOST")
# try:
#address = input("Host:Port (localhost:8000): ")
#if not address:
#    host, port = "localhost", 8000
#else:
#    host,port = address.split(":")
host, port = "203.252.182.154", 8000
frozenServe = FrozenServer(localaddr=(host, int(port)))
frozenServe.tick()



