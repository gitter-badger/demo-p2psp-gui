import os
import sys
import threading
import time
try:
    import pygame
    import vlc
    from gi.repository import GObject
    from gi.repository import Gtk
    from gi.repository import GdkX11
    import peer
    from peer_ims import Peer_IMS
    from peer_dbs import Peer_DBS
    from lossy_peer import Lossy_Peer
except Exception as msg:
    print(msg)


class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print "Starting " + self.name
        self.x=peer.Peer()
        print "Exiting " + self.name



def callback(self, player):
 
	'''print
	print 'FPS =',  player.get_fps()
	print 'time =', player.get_time(), '(ms)'
	print 'FRAME =', .001 * player.get_time() * player.get_fps()'''
	

    
class GameWindow(Gtk.Window):

    
    
    def __init__(self):
        Peer_IMS.USE_LOCALHOST = True
        self.player_paused=False
        self.peer_active=False
        self.builder = self.load_interface('ice.glade', 'ice.glade')
        self.get_objects()
        self.builder.connect_signals(self.setup_signals())
        self.window.connect("destroy",Gtk.main_quit)
        self.create_list_view()
        self.draw_area.set_size_request(600,500)
        #self.window.set_size_request(600,600)
        self.draw_area.show()
        self.draw_area.connect("realize",self._realized)
        
    def AddPeerListColumn(self, title, columnId):
		"""This function adds a column to the list view.
		First it create the gtk.TreeViewColumn and then set
		some needed properties"""
						
		column = Gtk.TreeViewColumn(title, Gtk.CellRendererText()
			, text=columnId)
		column.set_resizable(True)		
		column.set_sort_column_id(columnId)
		self.peer_view.append_column(column)
		
    def setup_peer_list(self):
        localhost_list = ['Monitor Peer', str(Lossy_Peer.CHUNK_LOSS_PERIOD), str(Peer_DBS.MAX_CHUNK_LOSS), str(Peer_IMS.PLAYER_PORT),str(Peer_IMS.SPLITTER_ADDR),str(Peer_IMS.SPLITTER_PORT),str(Peer_IMS.PORT),str(Peer_IMS.USE_LOCALHOST),'Pending','Pending','GUI DEMO']
        self.peer_ListStore.append(localhost_list)
        #self.peer_ListStore.append(localhost_list)
        #self.peer_ListStore.append(localhost_list)
    
    def create_list_view(self):
        
        self.column_number = [0,1,2,3,4,5,6,7,8,9,10]
        self.columnm_string = ["ID->Peer Name","Chunk Loss period","Max Chunk Loss","Player Port","Splitter Host","Splitter Port","Port","Using Localhost","Buffer Status","Peers in Team","Category"]
        i=0
        while i < len(self.column_number):
            self.AddPeerListColumn(self.columnm_string[i], self.column_number[i])
            i = i + 1
        self.peer_ListStore = Gtk.ListStore(str, str, str, str,str,str,str,str,str,str,str)
        self.peer_view.set_model(self.peer_ListStore)
        
        self.setup_peer_list()
           
    def load_interface(self,dire, fName):
        fName = self.find_file(dire, fName)
        builder = Gtk.Builder()
        builder.add_from_file(fName)
        return builder
    
    def setup_signals(self):
        """
        Sets up the signals
        """
        sig = { 'on_stop_clicked'            : self.stop_player
                ,'on_pause_clicked'          : self.pause_player
                ,'on_play_clicked'           : self.play_player}

        return sig
        
    def show(self):
        self.window.show_all() # display widgets
        
    def get_objects(self):
        self.window = self.builder.get_object('MainWindow')
        self.menubar = self.builder.get_object('menubar')
        self.add_btn = self.builder.get_object('add')
        self.draw_area = self.builder.get_object('surface')
        self.channel_label = self.builder.get_object('team')
        self.peer_view = self.builder.get_object('PeerView')

        
    def find_file(self,dire, fName):
        """
        Generates the complete path of a file
        returns the complete path
        """
        path = os.path.join(os.path.dirname(dire), fName)
        return path
        
    	
    def stop_player(self, widget, data=None):
        self.player.stop()
        #time.sleep(1)
        self.peer_active=False
        print 'player stopped'
        
    def pause_player(self,widget, data=None):
        if (self.player_paused== False):
            self.player.pause()
            self.player_paused=True
            print 'player paused'
       
       
    def start_peer(self):
        thread1 = myThread(1, "Peer Thread")
        thread1.start()
        
    def play_player(self,widget, data=None):
        if (self.peer_active == False):
            self.start_peer()
            self.peer_active=True
        self.player.play()
        self.player_paused = False
        print 'player started'
        
    
        
    def _realized(self, widget, data=None):
        os.putenv('SDL_WINDOWID', str(widget.get_window().get_xid()))        
        pygame.init()
        pygame.display.set_mode()
        self.screen = pygame.display.get_surface()
        print "Using %s renderer" % pygame.display.get_driver()
        # Create instane of VLC and create reference to movie.
        self.vlcInstance = vlc.Instance()
        self.player = self.vlcInstance.media_player_new()
        self.em = self.player.event_manager()
        self.em.event_attach(vlc.EventType.MediaPlayerTimeChanged,callback, self.player)
        win_id = pygame.display.get_wm_info()['window']
        self.player.set_xwindow(win_id)
        self.player.set_mrl('http://localhost:9999')
        pygame.mixer.quit()
        #self.player.play()   

exitFlag = 0
        

if __name__ == "__main__":
    window=GameWindow()
    window.show()

    Gtk.main()
    window.player.stop()
    print "Exiting Main Thread"
        
        
