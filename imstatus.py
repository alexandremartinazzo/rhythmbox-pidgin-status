#!/usr/bin/env python
# -*- coding: utf-8 -*-

#~ imstatus.py
#~ 
#~ Copyright 2008 (C) Alexandre Antonino Gonçalves Martinazzo <alexandremartinazzo@gmail.com>
#~ 
#~ This program is free software; you can redistribute it and/or modify
#~ it under the terms of the GNU General Public License as published by
#~ the Free Software Foundation; either version 2 of the License, or
#~ (at your option) any later version.
#~ 
#~ This program is distributed in the hope that it will be useful,
#~ but WITHOUT ANY WARRANTY; without even the implied warranty of
#~ MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#~ GNU General Public License for more details.
#~ 
#~ You should have received a copy of the GNU General Public License
#~ along with this program; if not, write to the Free Software
#~ Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#~ MA 02110-1301, USA.
 

import dbus
import rb

class IMStatus (rb.Plugin):
    def __init__ (self):
        rb.Plugin.__init__ (self)
        
    def activate(self, shell):
        obj = dbus.SessionBus ().get_object ('im.pidgin.purple.PurpleService', '/im/pidgin/purple/PurpleObject')
        self.im_instance = Pidgin (interface)
        im_accounts = im_instance.listAccounts ()
        #olhar esses eventos
        player = shell.get_player ()
        self.psc_id = player.connect ('playing-song-changed', self.playing_song_changed)
        self.pc_id = player.connect ('playing-changed', self.playing_changed)
    #obtido do plugin de artcover
    def playing_changed (self, player, playing):
        pass

    def playing_song_changed (self, player, entry):
        pass
        
 ## informações obtidas a partir da função help()
 #~ |      Signals from RBShellPlayer:
 #~ |    window-title-changed (gchararray)
 #~ |    elapsed-changed (guint)
 #~ |    playing-source-changed (RBSource)
 #~ |    playing-changed (gboolean)
 #~ |    playing-song-changed (RhythmDBEntry)
 #~ |    playing-uri-changed (gchararray)
 #~ |    playing-song-property-changed (gchararray, gchararray, GValue, GValue)
 #~ 
 #~ |  Properties from RBShellPlayer:
 #~ |    source -> RBSource: RBSource
 #~ |      RBSource object
 #~ |    db -> RhythmDB: RhythmDB
 #~ |      RhythmDB object
 #~ |    ui-manager -> GtkUIManager: GtkUIManager
 #~ |      GtkUIManager object
 #~ |    action-group -> GtkActionGroup: GtkActionGroup
 #~ |      GtkActionGroup object
 #~ |    play-order -> gchararray: play-order
 #~ |      What play order to use
 #~ |    playing -> gboolean: playing
 #~ |      Whether Rhythmbox is currently playing
 #~ |    volume -> gfloat: volume
 #~ |      Current playback volume
 #~ |    statusbar -> RBStatusbar: RBStatusbar
 #~ |      RBStatusbar object
 #~ |    queue-source -> RBPlaylistSource: RBPlaylistSource
 #~ |      RBPlaylistSource object
 #~ |    queue-only -> gboolean: Queue only
 #~ |      Activation only adds to queue
 #~ |    playing-from-queue -> gboolean: Playing from queue
 #~ |      Whether playing from the play queue or not
 #~ |    player -> GObject: RBPlayer
 #~ |      RBPlayer object
 
    def deactivate(self, shell):
        player = shell.get_player()
        player.disconnect(self.psc_id)
        player.disconnect(self.pc_id)
    


class Pidgin :

    def __init__(self, dbusInterface) :
        """
            Constructor
        """
        self.dbusInterface = dbusInterface

    def listAccounts(self) :
        """
            Purple merges all accounts, so we return a default one
            Each account is associated with:
                * A boolean -> True if the status of this account was changed on the previous track change
        """
        return {'GenericAccount' : False}

    def setAccountStatusMsg(self, account, msg) :
        """
            Change the status message of the given account
            Why is it so complex with Purple??
            Return true if the message is successfully updated
        """
        try :
            current    = self.dbusInterface.PurpleSavedstatusGetCurrent()
            statusType = self.dbusInterface.PurpleSavedstatusGetType(current)
            statusId   = self.dbusInterface.PurplePrimitiveGetIdFromType(statusType)
            if statusId in ['available'] :
                saved = self.dbusInterface.PurpleSavedstatusNew('', statusType)
                self.dbusInterface.PurpleSavedstatusSetMessage(saved, msg)
                self.dbusInterface.PurpleSavedstatusActivate(saved)
                return True
        except :
            pass
        return False

