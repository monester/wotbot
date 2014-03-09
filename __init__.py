""" fix 0.8.11 waiting bug (c) sirmax 2014 """

#####################################################################
# MOD INFO (mandatory)

XPM_MOD_VERSION    = "0.0.1"
XPM_MOD_URL        = "http://www.koreanrandom.com/forum/topic/11630-/#entry151768"
XPM_MOD_UPDATE_URL = ""
XPM_GAME_VERSIONS  = ["0.8.11"]

#####################################################################

from gui.mods.xpm import *
import Keys
#from gui.BattleContext import g_battleContext
from gui.InputHandler import g_instance
#from gui.WindowsManager import g_windowsManager
from gui import g_keyEventHandlers
from PlayerEvents import g_playerEvents
import math
import Math
from walker import walker
## For debugging import sys lib
import sys
#log(dir(BigWorld.player()))
#log(dir(g_playerEvents))


class WotBotter:
    enabled = False
    i=0
    #poi = [[-400,-400],[-400,-200],[-300,-200],[-300,200],[0,200],[0,450],[-450,450]]
    poi = [[0,0],[-280, 380]]
    subpos = list()
    
    def __init__(self):
        pass

    def seti(self):
        self.i = self.i+1 if self.i<len(self.poi)-1 else 0

    def rrad(self, x1, y1, x2,y2):
        x2 -= x1
        y2 -= y1
        return math.atan2(x2,y2)

#    def next_point(self):
#        i = self.i
#        (x,y) = (self.poi[i][0], self.poi[i][1])
#        if(x,y
#        (sub_x, sub_y) = (self.subpos[j][0], self.subpos[j][1])
        

    def move(self):
        try:
            i = self.i
            (dst_x, dst_y) = (self.subpos[self.j][0], self.subpos[self.j][1])
            player = BigWorld.player()
            (speed,rspeed) = player.getOwnVehicleSpeeds()
            (x,z,y) = player.getOwnVehiclePosition()
            yaw = player.vehicle.yaw
            log('x: %f y: %f z: %f' % (x, y, z))
            rad = poi_angle = self.rrad(x,y,dst_x,dst_y)
            log ("real: %f ?? needed: %f" % (yaw, poi_angle))
            flags = 1
            left=0
            right=0
            """ Add dx,dy depending on vehicle max speed """
            if not ( (rad+0.2 > yaw > rad - 0.2) or (rad+0.2 > yaw - 2*math.pi > rad - 0.2)):
                while walk.check_nowalls((x,y), (self.subpos[self.j+1][0], self.subpos[self.j+1][1])):
                    log("SKIPPING SUB POS")
                    self.j += 1
                    if self.j >= len(self.subpos)-1:
                        return True
                (left, right) = (0,0)
                if (yaw > rad > yaw - math.pi) or (yaw > rad - 2*math.pi > yaw - math.pi):
                    flags |= 4
                else:
                    flags |= 8
            if(dst_x - 3 < x < dst_x + 3 and dst_y - 3 < y < dst_y + 3):
                log("j++")
                self.j += 1
            if(self.poi[i][0] - 5 < x < self.poi[i][0] + 5 and self.poi[i][1] - 5 < y < self.poi[i][1] + 5):
                #self.seti()
                return True
            BigWorld.player().base.vehicle_moveWith(flags)
        except Exception, ex:
            log('[WOTBOT Move] throwed exception: %s' % (ex.message))
            print sys.exc_traceback.tb_lineno 

    def handleKeyEvent(self, event):
        #log ("%s %s %s %s" % (event.isKeyDown, event.isKeyUp ,event.key, event.isCtrlDown))
        pass

    def running(self):
        """
        Check if bot can move ingame.
        player.isOnArena == True only when player is alive
        player.isOnArena exists only when battle is loaded
        """
        player = BigWorld.player()
        if self.enabled and 'player' in locals() and hasattr(player, 'isOnArena') and player.isOnArena:
            return True

# event handlers (entry points)
    def onEnterWorld(self, *args):
        """ Executet when map is loaded """
        log(">onEnterWorld")
        self.boundingBox = BigWorld.player().arena.arenaType.boundingBox
        walk.set_map(-self.boundingBox[0][0], self.boundingBox[1][1])
        print BigWorld.player().arena.arenaType.boundingBox
        log(BigWorld.player().arena.arenaType)
#    log(dir(BigWorld.player().arena.arenaType.boundingBox))


    def onLeaveWorld(self, *args):
        """ Executed before map is unloaded """
        log(">onLeaveWorld")
#   try:
#            #isDown, key, mods, isRepeat = game.convertKeyEvent(event)
#            if not isRepeat and isDown:
#                log("%s %s %s %s" % isDown, key, mods, isRepeat)
#        except Exception as e:
#            LOG_CURRENT_EXCEPTION()
#        finally:
#            #return game.oldHandleKeyEvent(event)

wb = WotBotter()
walk = walker('')
walk.load_maze('')

#wb.subpos = walk.get_path(20,20,

def _wotbot_callback():
    try:
    	if wb.running():
            (x,z,y) = BigWorld.player().getOwnVehiclePosition()
            #(dx,dy) = (-wb.boundingBox[0][0], wb.boundingBox[1][1])
            #walk.get_path(x,y,0,0,dx,dy)
            if wb.move():
                wb.seti()
                (x,z,y) = BigWorld.player().getOwnVehiclePosition()
                wb.j=0
                wb.subpos = walk.get_path((x,y),wb.poi[wb.i])
        if BigWorld.isKeyDown(Keys.KEY_F11):
            log('[WOTBOT] F_11 pressed')
            msg = ""
            if wb.enabled:
            	wb.enabled = False
            	msg = "WOTBOT is off"
                log(msg)
            else:
                msg = "WOTBOT is on, building path"
                log(msg)
                wb.j=0
                (x,z,y) = BigWorld.player().getOwnVehiclePosition()
                wb.subpos = walk.get_path((x,y),wb.poi[wb.i])
                wb.enabled = True
            log("Sending message to window")
            from gui.WindowsManager import g_windowsManager
            if g_windowsManager.battleWindow is not None:
                 g_windowsManager.battleWindow.call('battle.PlayerMessagesPanel.ShowMessage', ['0', msg, 'gold'])
        if BigWorld.isKeyDown(Keys.KEY_F2):
            (dst_x, dst_y) = (wb.subpos[wb.j][0], wb.subpos[wb.j][1])
            player = BigWorld.player()
            (speed,rspeed) = player.getOwnVehicleSpeeds()
            (x,z,y) = player.getOwnVehiclePosition()
            yaw = player.vehicle.yaw
            log('x: %f y: %f z: %f => (%i, %i)' % (x, y, z, dst_x, dst_y))
            rad = poi_angle = wb.rrad(x,y,dst_x,dst_y)
            log ("real: %f ?? needed: %f" % (yaw, poi_angle))
            print (player.userSeesWorld)
  
    except Exception, ex:
        log('[WOTBOT] throwed exception: %s' % (ex.message))
    finally:
        BigWorld.callback(0.1, _wotbot_callback)




# Register events
def _RegisterEvents():
    try:
        from Avatar import PlayerAvatar
        RegisterEvent(PlayerAvatar, 'onEnterWorld', wb.onEnterWorld)
        RegisterEvent(PlayerAvatar, 'onLeaveWorld', wb.onLeaveWorld)

        #from gui import g_keyEventHandlers, g_mouseEventHandlers
        #g_keyEventHandlers.add(wb.handleKeyEvent)

        #game.oldHandleKeyEvent = game.handleKeyEvent
        #game.handleKeyEvent = wb.handleKeyEvent
        pass
    except Exception, ex:
        log('[WOTBOT] throwed exception: %s' % (ex.message))

g_keyEventHandlers.add(wb.handleKeyEvent)
BigWorld.callback(1, _RegisterEvents)
BigWorld.callback(1, _wotbot_callback)

