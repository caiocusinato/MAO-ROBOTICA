import cv2
import mediapipe as mp
import serial 
import time


ser = serial.Serial('COM16',9600,timeout=.1)
print(ser.name)
video = cv2.VideoCapture(0)
hand = mp.solutions.hands
Hand = hand.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils
video.set(cv2.CAP_PROP_FPS,10)
video.set(cv2.CAP_PROP_BUFFERSIZE, 10)
delay = 0.1
def limpaBuffer(video_capture):
    video_capture.release()
    cv2.waitKey(500) 
    video_capture.open(0)

ultimoLimpo=time.time()

while True:
    tempoAgr = time.time() 
    if tempoAgr-ultimoLimpo>=60:
         limpaBuffer(video)
         ultimoLimpo = tempoAgr

    check,img = video.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = Hand.process(imgRGB)
    handPoints = results.multi_hand_landmarks
    h,w,_ = img.shape
    pontos = []
    if handPoints: 
            for points in handPoints: 
                #print(points)
                mpDraw.draw_landmarks(img,points,hand.HAND_CONNECTIONS)
                for id,cord in enumerate(points.landmark):
                    cx,cy = int(cord.x*w) , int(cord.y*h)
                    #cv2.putText(img,str(id),(cx,cy),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2)
                    pontos.append((cx,cy))
    final = ['0','0','0','0','0']
    if pontos: 
        dedos = [8,12,16,20] 
        contador=0 
        if points: 
                if pontos[4][0]> pontos[2][0]: 
                    final[contador]='1'
                    contador+=1
                else: 
                     final[contador]='0'
                     contador+=1

                for x in dedos: 
                    if pontos[x][1] < pontos[x-2][1]:
                        final[contador]='1'
                        contador+=1
                    else: 
                         final[contador]='0'
                         contador+=1  
        
    resul = ''.join(final)
    resulFinal = "$" + resul
    ser.write(resulFinal.encode())
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    img = img[:, ::-1]
    cv2.imshow("maozinha.com",img)
    cv2.waitKey(1)
    time.sleep(delay)
