import pygame

# Constants for colors and dimensions
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
BLUE = (0, 255, 255)
RED = (255, 0, 0)
MENU_WIDTH = 300
MENU_HEIGHT = 600
TOGGLE_HEIGHT = 50
SLIDER_HEIGHT = 50
MARGIN = 10

# State variables
esp_enabled = False
aimbot_enabled = False
fov_value = 90

def draw_menu(screen, fov_value):
    # Draw menu background
    menu_rect = pygame.Rect(0, 0, MENU_WIDTH, MENU_HEIGHT)
    pygame.draw.rect(screen, GRAY, menu_rect)
    pygame.draw.rect(screen, BLUE, menu_rect, 2)

    # Draw ESP toggle
    draw_toggle(screen, "ESP", esp_enabled, (MARGIN, MARGIN))

    # Draw Aimbot toggle
    draw_toggle(screen, "Aimbot", aimbot_enabled, (MARGIN, MARGIN + TOGGLE_HEIGHT + MARGIN))

    # Draw FOV slider
    draw_slider(screen, "FOV", fov_value, (MARGIN, MARGIN + 2 * (TOGGLE_HEIGHT + MARGIN)))

def draw_toggle(screen, label, state, position):
    x, y = position
    toggle_rect = pygame.Rect(x, y, MENU_WIDTH - 2 * MARGIN, TOGGLE_HEIGHT)
    pygame.draw.rect(screen, BLUE if state else RED, toggle_rect)
    pygame.draw.rect(screen, WHITE, toggle_rect, 2)
    font = pygame.font.Font(None, 36)
    text = font.render(f"{label}: {'On' if state else 'Off'}", True, WHITE)
    screen.blit(text, (x + MARGIN, y + MARGIN))

def draw_slider(screen, label, value, position):
    x, y = position
    slider_rect = pygame.Rect(x, y, MENU_WIDTH - 2 * MARGIN, SLIDER_HEIGHT)
    pygame.draw.rect(screen, WHITE, slider_rect, 2)
    font = pygame.font.Font(None, 36)
    text = font.render(f"{label}: {value}", True, WHITE)
    screen.blit(text, (x + MARGIN, y + MARGIN))
    # Draw slider handle
    handle_x = x + int((value / 120) * (MENU_WIDTH - 4 * MARGIN))
    handle_rect = pygame.Rect(handle_x, y, 10, SLIDER_HEIGHT)
    pygame.draw.rect(screen, BLUE, handle_rect)

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
                    if MARGIN < mouse_y < MARGIN + TOGGLE_HEIGHT:
                        esp_enabled = not esp_enabled
                    elif MARGIN + TOGGLE_HEIGHT + MARGIN < mouse_y < 2 * (MARGIN + TOGGLE_HEIGHT):
                        aimbot_enabled = not aimbot_enabled
                    elif 2 * (MARGIN + TOGGLE_HEIGHT) < mouse_y < 3 * (MARGIN + TOGGLE_HEIGHT):
                        fov_value = int((mouse_x - MARGIN) / (MENU_WIDTH - 2 * MARGIN) * 120)

    return True

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
    pygame.display.set_caption('Trajectory Oracle Menu')

    running = True
    while running:
        screen.fill((0, 0, 0))  # Clear screen
        draw_menu(screen, fov_value)
        pygame.display.flip()

        running = handle_ui_events()
        pygame.time.delay(100)

    pygame.quit()
