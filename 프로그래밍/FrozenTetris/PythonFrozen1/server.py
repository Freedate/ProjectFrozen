from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
from time import sleep

class ClientChannel(Channel):
    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        self.gameid = "0"

    def Network_gameStart(self, data):
        self._server.GameStart(data["stage"])

    def Network_userInfo(self, data):
        self.gameid = data["gameid"]

    def Close(self):
        self._server.DelPlayer(self, self.gameid)

    def Network_fezMove(self, data):
        self._server.FezMove(data["move"], data["turn"])

    def Network_fezPos(self, data):
        self._server.FezPos(data["x"], data["y"], data["jump"])
    
    def Network_gameOver(self, data):
        self._server.GameOver(data["score"])

    def Network_newTetris(self, data):
        self._server.NewTetris(data["shape"], data["color"])

    def Network_tetrisMove(self, data):
        self._server.TetrisMove(data["act"], data["what"], data["value"])
    
    def Network_blockOnMap(self, data):
        self._server.BlockOnMap(data["x"], data["y"])

    def Network_moveComponents(self, data):
        self._server.MoveComponents()

class FrozenServer(Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)  # create server
        print("server accept")
        
        self.queue = None
        self.currentIdx = 0

    def Connected(self, channel, addr):
        print('new connection:', str(channel.addr))
        if self.currentIdx >= 2:        # 현재 접속 인원이 2명이면
            channel.Send({"action":"overflow"})
            return

        if self.queue == None:         # 첫번째 유저
            print("First User")
            self.queue = Game(channel, self.currentIdx)
            self.currentIdx += 1
        else:      # 두번째 유저
            print("Second User")
            self.queue.player1 = channel
            self.queue.player0.Send({"action": "userConnected", "gameid":0})    # fez
            self.queue.player1.Send({"action": "userConnected", "gameid":1})    # block
            self.currentIdx += 1

    def DelPlayer(self, player, id):
        print("Deleting player" + str(id) + " " + str(player.addr))
        # 변수 리셋
        if self.currentIdx == 2:
            self.currentIdx = 1
            if int(id) == 0:
                self.queue.player0 = self.queue.player1
            self.queue.player0.Send({"action":"outUser"})
            self.queue.player1 = None
        else:
            self.queue = None
            self.currentIdx = 0

    def GameStart(self, stage):
        self.queue.player1.Send({"action": "gameStart","stage":stage})

    def PrintStr(self, str):
        print(str)

    def FezMove(self, move, turn):
        # player0의 움직임을 player1에게 전달
        self.queue.player1.Send({"action": "fezMove", "move":move, "turn":turn})
 
    def FezPos(self, x, y, jump):
        self.queue.player1.Send({"action": "fezPos", "x":x, "y":y, "jump":jump})

    def GameOver(self, score):
        self.queue.player0.Send({"action": "gameOver", "score":score})
        self.queue.player1.Send({"action": "gameOver", "score":score})

    def NewTetris(self, shape, color):
        self.queue.player0.Send({"action": "newTetris", "shape":shape, "color":color})

    def TetrisMove(self, act, what, value):
        self.queue.player0.Send({"action": "movementTetris", "act":act, "what":what, "value":value})
        #self.queue.player1.Send({"action": "movementTetris", "act":act, "what":what, "value":value})

    def BlockOnMap(self, x, y):
        self.queue.player0.Send({"action": "blockOnMap", "x":x, "y":y})
    
    def MoveComponents(self):
        self.queue.player1.Send({"action":"moveComponents"})

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



