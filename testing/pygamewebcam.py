import pygame
from pygame.locals import *
import pygame.camera
import sys

def main():
    pygame.init()
    pygame.camera.init()
    
    # Get list of available cameras
    camlist = pygame.camera.list_cameras()
    if not camlist:
        print("No cameras found.")
        sys.exit(1)
    
    # Use the first camera
    cam = pygame.camera.Camera(camlist[0], (640, 480), "RGB")
    cam.start()
    
    # Set up display
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Webcam Feed")
    
    running = True
    while running:
        # Capture frame
        image = cam.get_image()
        
        # Display frame
        screen.blit(image, (0, 0))
        pygame.display.flip()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False
    
    cam.stop()
    pygame.quit()

if __name__ == "__main__":
    main()
