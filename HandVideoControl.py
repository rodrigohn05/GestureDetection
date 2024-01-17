import cv2
import mediapipe as mp
import time
import vlc
import argparse

class handDetector():
    def __init__(self, mode=False, maxHands=1, detectionCon=0.7, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]


    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):

        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                self.lmList.append([id, cx, cy])
              #  if draw:
             #       cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return self.lmList

    def fingersUp(self):
        fingers = []
        # Thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return fingers

    
def main():
    playvar = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    #var= player.video_get_adjust_float(vlc.VideoAdjustOption.Brightness)
    cap = cv2.VideoCapture(1)
    detector = handDetector()
    draw = 0
    if draw == 0:
        player.play()
    tempo = 5000
    stopvar = 0
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        value = player.get_time()
        for x in playvar:
            #print("aqui")
            if value >= tempo and x == 0 and FLAGS.tutorial == 1:
                player.set_time(tempo - 5000)
             #   print("dentro")
                break
        
        if len(lmList) != 0:
            #print(lmList[9])
            fingers = detector.fingersUp()

            #PULGAR BAIXO DIREITA (PLAY)
            if fingers[0] == 0 and lmList[9][1]<250 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                player.play()
                if stopvar != 0:
                    player.set_time(reopen)
                
                if tempo == 70000 and FLAGS.tutorial == 1:
                    tempo += 5000       
            #INDICADOR BAIXO DIREITA (PAUSE)
            elif fingers[1] == 0 and lmList[9][1]<250 and fingers[0] == 1 and fingers[4] == 1 and fingers[2] == 1 and fingers[3] == 1:
                player.pause()
                time.sleep(0.5)
                playvar[0] = 1
                if tempo == 5000 and FLAGS.tutorial==1:
                    tempo+=5000
            #MEIO BAIXO DIREITA (STOP)
            elif fingers[2] == 0 and lmList[9][1]<250 and fingers[1] == 1 and fingers[0] == 1 and fingers[3] == 1 and fingers[4] == 1:
                reopen = value
                stopvar = 1
                player.stop()
                
                if tempo == 75000 and FLAGS.tutorial==1:
                    tempo += 5000
            #ANELAR BAIXO DIREITA (+5segs)    
            elif fingers[3] == 0 and lmList[9][1]<250 and fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 1 and fingers[4] == 1:
                player.set_time(player.get_time() + 500)
                playvar[1] = 1
                if tempo == 10000 and FLAGS.tutorial==1:
                    tempo += 5000
            #MINDINHO BAIXO DIREITA (Bright +1)
            elif fingers[4] == 0 and lmList[9][1]<250 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[0] == 1:
                player.video_set_adjust_float(vlc.VideoAdjustOption.Brightness, player.video_get_adjust_float(vlc.VideoAdjustOption.Brightness)+0.2)
                #time.sleep(0.25)
                if tempo == 20000 and FLAGS.tutorial==1:
                    tempo += 5000

            #PULGAR BAIXO ESQUERDA (+ Contraste)
            if fingers[0] == 0 and lmList[9][1]>400 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                player.video_set_adjust_float(vlc.VideoAdjustOption.Contrast, player.video_get_adjust_float(vlc.VideoAdjustOption.Contrast)+0.2)
                #time.sleep(0.25)
                if tempo == 30000 and FLAGS.tutorial==1:
                    tempo += 5000
            #INDICADOR BAIXO Esquerda (+SAT)
            elif fingers[1] == 0 and lmList[9][1]>400 and fingers[0] == 1 and fingers[4] == 1 and fingers[2] == 1 and fingers[3] == 1:
                player.video_set_adjust_float(vlc.VideoAdjustOption.Saturation, player.video_get_adjust_float(vlc.VideoAdjustOption.Saturation)+0.2)
                #time.sleep(0.25)
                if tempo == 40000 and FLAGS.tutorial==1:
                    tempo += 5000
            #MEIO BAIXO Esquerda (-SAT)
            elif fingers[2] == 0 and lmList[9][1]>400 and fingers[1] == 1 and fingers[0] == 1 and fingers[3] == 1 and fingers[4] == 1:
                player.video_set_adjust_float(vlc.VideoAdjustOption.Saturation, player.video_get_adjust_float(vlc.VideoAdjustOption.Saturation)-0.2)
                #time.sleep(0.25)
                if tempo == 45000 and FLAGS.tutorial==1:
                    tempo += 5000
            #ANELAR BAIXO Esquerda (-5segs)    
            elif fingers[3] == 0 and lmList[9][1]>400 and fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 1 and fingers[4] == 1:
                player.set_time(player.get_time() - 500)
                playvar[2]=1
                if tempo == 15000 and FLAGS.tutorial==1:
                    tempo += 5000
            #MINDINHO BAIXO Esquerda (-Brightness)
            elif fingers[4] == 0 and lmList[9][1]>400 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[0] == 1:
                player.video_set_adjust_float(vlc.VideoAdjustOption.Brightness, player.video_get_adjust_float(vlc.VideoAdjustOption.Brightness)-0.2)
                if tempo == 25000 and FLAGS.tutorial==1:
                    tempo += 5000
                #time.sleep(0.25)
            #MAO FITXADA ESQUERDA (-Contraste)
            elif fingers[4] == 0 and lmList[9][1]>400 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[0] == 0:
                player.video_set_adjust_float(vlc.VideoAdjustOption.Contrast, player.video_get_adjust_float(vlc.VideoAdjustOption.Contrast)-0.2)
                #time.sleep(0.25)
                if tempo == 35000 and FLAGS.tutorial==1:
                    tempo += 5000
            #CORNOS (RESET VÍDEO)
            elif fingers[4] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[0] == 1:
                player.video_set_adjust_float(vlc.VideoAdjustOption.Contrast, 1)
                player.video_set_adjust_float(vlc.VideoAdjustOption.Saturation, 1)
                player.video_set_adjust_float(vlc.VideoAdjustOption.Brightness, 1)
                if tempo == 50000 and FLAGS.tutorial==1:
                    tempo += 5000
            #LEGAU (RESET SOM)
            elif fingers[4] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[0] == 1:
                player.audio_set_volume(100)
                if tempo == 65000 and FLAGS.tutorial==1:
                    tempo += 5000
            #PALAVRA DE ESCUTEIRO (SOM+)
            elif fingers[4] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[0] == 0:
                player.audio_set_volume(player.audio_get_volume()+10)
                if tempo == 55000 and FLAGS.tutorial==1:
                    tempo += 5000
            #INDICADOR + MEIO (SOM-)
            elif fingers[4] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[0] == 0:
                player.audio_set_volume(player.audio_get_volume()-10)
                if tempo == 60000 and FLAGS.tutorial==1:
                    tempo += 5000
            #Pulgar (SS)    
            elif fingers[4] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[0] == 1:
                player.video_set_adjust_int(vlc.VideoAdjustOption.Enable, 0)
                time.sleep(0.5)
                player.video_take_snapshot(0, ".\gt.png", 640, 480)
                player.video_set_adjust_int(vlc.VideoAdjustOption.Enable, 1)
                draw = 1
                player.stop()
                exec(open('virtualpainter.py').read())
                #print ("tou aqui por alguma razao")
                #vp.main()
        
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tutorial',
        type=int,
        default=1,
        help='Wether or not the user wishes to play the tutorial version (1-Yes; 0-No)')
    
    
    parser.add_argument('-v', '--video',
        type=str,
        default='spirit.mp4',
        help='Name of the video that the user wants to watch (Must include the file extension, eg: myvideo.mp4')

    
    FLAGS, unparsed = parser.parse_known_args()

    i = vlc.Instance()
    player = i.media_player_new()
    if FLAGS.tutorial == 1:
        media = i.media_new("./Tutorial.mp4")
    else:
        media = i.media_new("./{}".format(FLAGS.video))
    player.set_media(media)
    player.video_set_adjust_int(vlc.VideoAdjustOption.Enable, 1)

    main()
    
    