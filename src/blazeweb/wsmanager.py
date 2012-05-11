import uuid
import simplejson
import logging
log = logging.getLogger(__name__)

class MultiDictionary(object):
    def __init__(self):
        self.dict = {}

    def add(self, k, v):
        self.dict.setdefault(k, set()).add(v)
        
    def remove_val(self, k, v):
        self.dict.setdefault(k, set()).remove(v)
        if len(self.dict[k]) == 0:
            self.remove(k)
            
    def remove(self, k):
        del self.dict[k]

    def get(self, k):
        return self.dict[k]
        
class WebSocketManager(object):
    def __init__(self):
        self.sockets = {}
        self.topic_clientid_map = MultiDictionary()
        self.clientid_topic_map = MultiDictionary()
    
    def remove_clientid(self, clientid):
        topics = self.clientid_topic_map.get(clientid)
        for topic in topics:
            self.topic_clientid_map.remove_val(topic, clientid)
            
    def remove_topic(self, topic):
        clientids = self.topic_clientid_map.get(topic)
        for clientid in clientids:
            self.clientid_topic_map.remove_val(clientid, topic)
            
    def subscribe_socket(self, socket, topic, clientid=None):
        if clientid is None :
            clientid = str(uuid.uuid4())
        self.subscribe(clientid, topic)
        self.add_socket(socket, clientid)

    def can_subscribe(self, clientid, topic):
        #auth goes here
        return True
    
    def subscribe(self, clientid, topic):
        if self.can_subscribe(clientid, topic):
            self.topic_clientid_map.add(topic, clientid)
            self.clientid_topic_map.add(clientid, topic)
        
    def add_socket(self, socket, clientid):
        self.sockets[clientid] = socket
    
    def remove_socket(self, clientid):
        del self.sockets[clientid]
        
    def send(self, topic, msg):
        for clientid in self.topic_clientid_map.get(topic):
            socket = self.sockets[clientid]
            try:
                socket.send(msg)
            except Exception as e: #what exception is this?if a client disconnects
                log.exception(e)
                self.remove_socket(clientid)
                self.remove_clientid(clientid)

def run_socket(socket, manager, auth_function, protocol_helper):
    ph = protocol_helper
    clientid = str(uuid.uuid4())
    while True:
        msg = socket.receive()
        if msg is None:
            self.close()
            break
        msgobj = ph.deserialize_msg(msg)
        if msgobj['msgtype'] == 'subscribe':
            if auth_function(msgobj.get('auth'), msgobj['topic']):
                manager.add_socket(socket, clientid)
                manager.subscribe(clientid, msgobj['topic'])
                socket.send(ph.serialize_msg(
                    ph.status_obj(
                        ['subscribesuccess', msgobj['topic']])))
            else:
                socket.send(ph.serialize_msg(ph.error_obj('unauthorized')))
                
        
