from typing import List


class Peer:
    def __init__(self, ip, port) -> None:
        self.__ip = ip
        self.__port = int(port)

    @property
    def ip(self):
        return self.__ip

    @property
    def port(self):
        return self.__port

    def __eq__(self, value: object) -> bool:
        return isinstance(value, Peer) and self.ip == value.ip and self.port == value.port

    def __hash__(self) -> int:
        return hash((self.ip, self.port))


class PeerStore:
    PEER_CONF_PATH = "/tmp/hffs_peers.conf"

    def __init__(self):
        self.__peers = set()
        with open(self.PEER_CONF_PATH, "r+", encoding="utf-8") as f:
            for line in f:
                ip, port = line.strip().split(":")
                peer = Peer(ip, port)
                self.__peers.add(peer)

    def close(self):
        with open(self.PEER_CONF_PATH, "w", encoding="utf-8") as f:
            for peer in self.__peers:
                f.write(f"{peer.ip}:{peer.port}\n")

    def add_peer(self, peer):
        self.__peers.add(peer)

    def remove_peer(self, peer):
        self.__peers.discard(peer)

    def get_peers(self):
        return self.__peers


class PeerManager:
    DEFAULT_PORT = 8080

    def __init__(self, peer_store):
        self.__peer_store = peer_store

    def add_peer(self, ip, port=None):
        peer = Peer(ip, port if port else self.DEFAULT_PORT)
        self.__peer_store.add_peer(peer)

    def remove_peer(self, ip, port=None):
        peer = Peer(ip, port if port else self.DEFAULT_PORT)
        self.__peer_store.remove_peer(peer)
        
    def get_peers(self) -> List[Peer]:
        return self.__peer_store.get_peers()

    def list_peers(self):
        print("List of peers:")
        for peer in self.__peer_store.get_peers():
            print(f"{peer.ip}:{peer.port}")
