import cv2
import numpy as np
def acquisition_manuelle(chemin):
    image = cv2.imread('chemin')
    return(image)


## pour sauver au format PNG

def ecrire_PNG(nom_du_fichier):
    cv2.imwrite('nom_du_fichier.png', image, [cv2.IMWRITE_PNG_COMPRESSION, 0])


## pour format jpg
def ecrire_jpeg(nom_du_fichier,nouvelleimage):
    cv2.imwrite('nouvelleimage.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 0])


##verification
def  verif(IMG):
    saved_img = cv2.imread('IMG.jpg')
    cv2.imshow('nouvelle_image',saved_img)


##sauvegarde de video

capture = cv2.VideoCapture('video_2.mp4')

def ecrire_video(adresse_video,video):
    frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    has_frame, frame = capture.read()
    video=cv2.VideoWriter(adresse_video,cv2.VideoWriter_fourcc(*'MJPG'),25,(frame_width,frame_height))

    while True:
        has_frame, frame = capture.read()
        if not has_frame:
            print('cant get frame')
            break
        video.write(frame)
        cv2.imshow('frame',frame)
        key = cv2.waitKey(3)
        if key == 27:
            print('Pressed Esc')
            break
    capture.release()
    ##writer.release()
    cv2.destroyAllWindows()
    
