# -*- coding: utf-8 -*-
import sys
import time
import telnetlib
from vlc import VideoMarqueeOption, Position, EventType, Instance
from vlc import State
from vlc import MediaParsedStatus
VLC_Player_Stoped = False

class RTSP_Client():
    pass

class VLC_Player():

    def __init__(self, url):
        self.url = url
        self.start_status = False
        self.vlc_player_stoped = VLC_Player_Stoped
        self.echo_position = False
        self.logger_pipe = None
        self.log_data_file = None

    def bytes_to_str(self, b):
        """Translate bytes to unicode string.
        """
        if isinstance(b, str):
            return unicode(b, DEFAULT_ENCODING)
        else:
            return b

    def start(self, timeout=60):
        """这种是最简方案，用来测试播放足够了
    　　"""
        instance = Instance()
        player = instance.media_player_new()
        Media = instance.media_new(self.url)
        mrl = Media.get_mrl()
        player.set_media(Media)
        event_manager = player.event_manager()
        event_manager.event_attach(EventType.MediaPlayerOpening, self.open_callback)
        event_manager.event_attach(EventType.MediaPlayerPaused, self.paused_callback)
        event_manager.event_attach(EventType.MediaListPlayerStopped, self.media_list_stoped_callback)
        event_manager.event_attach(EventType.MediaParsedChanged, self.media_buffering_callback)
        event_manager.event_attach(EventType.MediaPlayerStopped, self.stoped_callback)
        event_manager.event_attach(EventType.MediaPlayerEndReached, self.end_callback)
        event_manager.event_attach(EventType.VlmMediaInstanceStatusPause, self.vlm_media_instance_status_pause_callback)
        event_manager.event_attach(EventType.VlmMediaInstanceStatusError, self.vlm_media_instance_error_callback)
        event_manager.event_attach(EventType.MediaPlayerPausableChanged, self.media_player_pausable_callback)
        event_manager.event_attach(EventType.MediaPlayerPositionChanged, self.pos_callback, player, Media)
        while self.start_status:
            player.play()# 如果是看直播这里直接写while True 即可
            if player.get_state() == State.Stopped:
                for i in range(5):
                    player.play()
                    self.write_log(u"VLC播放停止了，第%d次尝试重连，总共尝试5次" % i)
                    if player.get_state() == State.Opening or player.get_state() == State.Playing:
                        break
                break
            if player.get_state() == State.Ended:
                for i in range(5):
                    player.stop()
                    self.start()
                    self.write_log(u"VLC播放终止了，第%d次尝试重连，总共尝试5次" % i)
                    if player.get_state() == State.Opening or player.get_state() == State.Playing:
                        break
                break
            if player.get_state() == State.Error:
                for i in range(5):
                    player.stop()
                    self.start()
                    self.write_log(u"VLC播放出错了，第%d次尝试重连，总共尝试5次" % i)
                    if player.get_state() == State.Opening or player.get_state() == State.Playing:
                        break
                break
        player.stop()

    def open_callback(self, event):
        self.write_log('player is starting...')

    def pos_callback(self, event, player, media):
        if player.get_fps():
            current_rate = int(1000 // (player.get_fps()))
        else:
            current_rate = 0
        ret = media.get_parsed_status()
        if ret == MediaParsedStatus(1):
            self.write_log(u"解析状态发生跳跃")
        elif ret == MediaParsedStatus(2):
            self.write_log(u"解析失败")
        elif ret == MediaParsedStatus(3):
            self.write_log(u"解析超时")
        self.write_log(u'当前VLC速率%d fps' % current_rate)
        player_state = media.get_state()
        if player_state == State.Buffering:
            log_str = u"当前VLC正在缓冲"
            self.write_log(log_str)
        if player_state == State.Error:
            log_str = u"当前VLC播放出错"
            self.write_log(log_str)
        if self.echo_position:
            self.write_log('\r%s %s to %.2f%% (%.2f%%)' % (
            time.ctime(), event.type, event.u.new_position * 100, player.get_position() * 100))

    def write_log(self, str):
        if self.logger_pipe is not None:
            if self.start_status:
                self.logger_pipe.send(str)
        else:
            return
        with open('log.txt', 'a+') as f:
            str = str.encode("utf-8")+'\n'
            f.write(str)

    def str_to_bytes(self, s):
        """Translate string or bytes to bytes.
        """
        if isinstance(s, str):
            return bytes(s, encoding="UTF-8")
        else:
            return s

    def media_list_stoped_callback(self, event):
        self.write_log(' media player was stoped' )

    def media_buffering_callback(self, event):
        self.write_log(" player is need buffering....." )

    def stoped_callback(self, event):
        self.write_log('player was stoped..')

    def paused_callback(self, event):
        self.write_log("player was paused.... " )

    def end_callback(self, event):
        self.write_log('End of media stream (event %s)' %  event.type)
        self.echo_position = False

    def parsed_callback(self, event):
        self.write_log('parse chanaged !!')

    def vlm_media_instance_status_pause_callback(self, event):
        self.write_log('status pause callback')

    def vlm_media_instance_error_callback(self, event):
        self.write_log('error callback')

    def media_player_pausable_callback(self, event):
        self.write_log('pausable callback')






if __name__ == "__main__":
    # 测试url为浙江卫视直播流
    url = "http://58.221.254.33:1935/live/zhongwen.sdp/playlist.m3u"
    url = "http://202.102.79.114:554/live/tvb8.stream/playlist.m3u8"
    url = "http://vshare.ys7.com:80/hcnp/472637161_1_1_1_0_www.ys7.com_6500.m3u8"
    url = "rtmp://live.hkstv.hk.lxdns.com/live/hks2"
    p = VLC_Player(url)
    p.start_status = True
    p.start()

