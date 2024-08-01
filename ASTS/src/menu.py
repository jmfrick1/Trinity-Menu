import pygame
import sys

# Constants for UI elements
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
BLUE = (0, 153, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BOLD_FONT_SIZE = 48
TOGGLE_FONT_SIZE = 36
SLIDER_FONT_SIZE = 36

# Define dimensions and positions
MENU_WIDTH = 300
MENU_HEIGHT = 600
TOGGLE_HEIGHT = 70
SLIDER_HEIGHT = 70
MARGIN = 15

# State variables
esp_enabled = False
aimbot_enabled = False
fov_value = 90

def draw_menu(screen, fov_value, security_level):
    # Draw menu background with rounded corners
    menu_rect = pygame.Rect(0, 0, MENU_WIDTH, MENU_HEIGHT)
    pygame.draw.rect(screen, GRAY, menu_rect, border_radius=20)
    pygame.draw.rect(screen, BLUE, menu_rect, 4, border_radius=20)
    
    # Draw header
    draw_header(screen, "Trajectory Oracle", (MARGIN, MARGIN))

    # Draw ESP toggle
    draw_toggle(screen, "ESP", esp_enabled, (MARGIN, 2 * MARGIN + BOLD_FONT_SIZE))

    # Draw Aimbot toggle
    draw_toggle(screen, "Aimbot", aimbot_enabled, (MARGIN, 3 * MARGIN + BOLD_FONT_SIZE + TOGGLE_HEIGHT))

    # Draw FOV slider
    draw_slider(screen, "FOV", fov_value, (MARGIN, 4 * MARGIN + BOLD_FONT_SIZE + 2 * TOGGLE_HEIGHT))

def draw_header(screen, text, position):
    font = pygame.font.Font(None, BOLD_FONT_SIZE)
    header = font.render(text, True, WHITE)
    screen.blit(header, position)

def draw_toggle(screen, label, state, position):
    x, y = position
    toggle_rect = pygame.Rect(x, y, MENU_WIDTH - 2 * MARGIN, TOGGLE_HEIGHT)
    pygame.draw.rect(screen, BLUE if state else RED, toggle_rect, border_radius=10)
    pygame.draw.rect(screen, WHITE, toggle_rect, 3, border_radius=10)
    font = pygame.font.Font(None, TOGGLE_FONT_SIZE)
    text = font.render(f"{label}: {'On' if state else 'Off'}", True, WHITE)
    screen.blit(text, (x + MARGIN, y + MARGIN))

def draw_slider(screen, label, value, position):
    x, y = position
    slider_rect = pygame.Rect(x, y, MENU_WIDTH - 2 * MARGIN, SLIDER_HEIGHT)
    pygame.draw.rect(screen, WHITE, slider_rect, 3, border_radius=10)
    font = pygame.font.Font(None, SLIDER_FONT_SIZE)
    text = font.render(f"{label}: {value}", True, WHITE)
    screen.blit(text, (x + MARGIN, y + MARGIN))
    # Draw slider handle with dynamic color
    handle_x = x + int((value / 120) * (MENU_WIDTH - 4 * MARGIN))
    handle_rect = pygame.Rect(handle_x, y, 10, SLIDER_HEIGHT)
    pygame.draw.rect(screen, BLUE, handle_rect, border_radius=5)

def handle_ui_events():
    global esp_enabled, aimbot_enabled, fov_value

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                esp_enabled = not esp_enabled
            elif event.key == pygame.K_a:
                aimbot_enabled = not aimbot_enabled
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = event.pos
                if MARGIN < mouse_x < MENU_WIDTH - MARGIN:
                    if 2 * MARGIN + BOLD_FONT_SIZE < mouse_y < 2 * MARGIN + BOLD_FONT_SIZE + TOGGLE_HEIGHT:
                        esp_enabled = not esp_enabled
                    elif 3 * MARGIN + BOLD_FONT_SIZE + TOGGLE_HEIGHT < mouse_y < 3 * MARGIN + BOLD_FONT_SIZE + 2 * TOGGLE_HEIGHT:
                        aimbot_enabled = not aimbot_enabled
                    elif 4 * MARGIN + BOLD_FONT_SIZE + 2 * TOGGLE_HEIGHT < mouse_y < 4 * MARGIN + BOLD_FONT_SIZE + 2 * TOGGLE_HEIGHT + SLIDER_HEIGHT:
                        fov_value = int((mouse_x - MARGIN) / (MENU_WIDTH - 2 * MARGIN) * 120)

    return True

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
    pygame.display.set_caption('Trajectory Oracle Menu')

    running = True
    while running:
        screen.fill(BLACK)  # Clear screen with black color for a sleek look
        draw_menu(screen, fov_value, 1)  # Default security level set to 1
        pygame.display.flip()

        running = handle_ui_events()
        pygame.time.delay(100)

    pygame.quit()
 # Trajectory Oracle