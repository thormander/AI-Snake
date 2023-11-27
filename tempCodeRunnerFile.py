def gameOverText(self):
    endText = font.render("Game Over! Your final score is: " + str(self.score), True, WHITE)
    endPosition = endText.get_rect(center=(self.w/2, self.h/2))
    self.display.blit(endText, endPosition)
    
    pygame.display.flip()
    pygame.time.wait(5000)