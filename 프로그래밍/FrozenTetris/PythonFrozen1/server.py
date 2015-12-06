from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
from time import sleep

class ClientChannel(Channel):
    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)

    def Close(self):
        self._server.DelPlayer(self)

    def Network_fezPos(self, data):
        self._server.PrintStr("fezPos : "+str(data['x'])+","+str(data['y']))

class FrozenServer(Server):
    channelClass = ClientChannel
    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)  # create server
        print("server accept")
        
        #self.games = []
        #self.queue = None
        #self.currentIndex = 0

    def Connected(self, channel, addr):
        print('new connection:', str(channel.addr))

        #if self.queue == None:         # 첫번째 유저
        #    self.currentIndex += 1
        #    channel.gameid = self.currentIndex
        #    self.queue = Game(channel, self.currentIndex)
        #else:      # 두번째 유저
        #    channel.gameid=self.currentIndex
        #    self.queue.player1=channel
        #    self.queue.player0.Send({"action": "startgame","player":0, "gameid": self.queue.gameid})
        #    self.queue.player1.Send({"action": "startgame","player":1, "gameid": self.queue.gameid})
        #    self.games.append(self.queue)
        #    self.queue=None

    def DelPlayer(self, player):
        print("Deleting Player" + str(player.addr))

    def PrintStr(self, str):
        print(str)

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
address = input("Host:Port (localhost:8000): ")
if not address:
    host, port = "localhost", 8000
else:
    host,port = address.split(":")
frozenServe = FrozenServer(localaddr=(host, int(port)))
#frozenServe = FrozenServer(localaddr=("192.168.11.103", int("5000")))
frozenServe.tick()



