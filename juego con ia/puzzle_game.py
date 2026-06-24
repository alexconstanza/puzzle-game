import os
import sys
import random
import urllib.request
import pygame
from PIL import Image

# --- CONFIGURACIÓN ---
pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750
PLAY_AREA_X = 50
PLAY_AREA_Y = 50
PLAY_AREA_SIZE = 600 

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rompecabezas Pro: Level Selection & Physics")
clock = pygame.time.Clock()

# Fuentes
FONT_BIG = pygame.font.SysFont("Arial", 48, bold=True)
FONT_MED = pygame.font.SysFont("Arial", 28, bold=True)
FONT_TEXT = pygame.font.SysFont("Arial", 20)

# Colores
BG_COLOR = (25, 25, 35)
PANEL_COLOR = (40, 40, 55)
TEXT_COLOR = (240, 240, 255)
HIGHLIGHT_COLOR = (0, 255, 150)
WARNING_COLOR = (255, 50, 50) # Rojo para la señal de advertencia
FRAME_COLOR = (100, 100, 130)

# --- BANCO DE IMÁGENES ---
IMAGE_URLS = {
    1: ["https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=600&h=600&fit=crop"] * 5,
    2: ["https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=600&h=600&fit=crop"] * 5,
    3: ["https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600&h=600&fit=crop"] * 5,
    4: ["https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=600&h=600&fit=crop"] * 5,
    5: ["https://images.unsplash.com/photo-1541701494587-cb58502866ab?w=600&h=600&fit=crop"] * 5
}

CACHE_DIR = "puzzle_images_cache"
if not os.path.exists(CACHE_DIR): os.makedirs(CACHE_DIR)

def get_image_path(level, sub_idx):
    filename = os.path.join(CACHE_DIR, f"lvl_{level}_img_{sub_idx}.jpg")
    if not os.path.exists(filename):
        try: urllib.request.urlretrieve(IMAGE_URLS[level][sub_idx], filename)
        except: 
            img = Image.new("RGB", (600, 600), (80, 80, 80))
            img.save(filename)
    return filename

# --- CLASES ---

class Piece:
    def __init__(self, id_num, surface, grid_x, grid_y, width, height):
        self.id = id_num
        self.image = surface
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.w = width
        self.h = height
        
        # Posición inicial aleatoria dentro del recuadro
        self.pos = pygame.Vector2(
            random.randint(PLAY_AREA_X, PLAY_AREA_X + PLAY_AREA_SIZE - self.w),
            random.randint(PLAY_AREA_Y, PLAY_AREA_Y + PLAY_AREA_SIZE - self.h)
        )
        self.rect = self.image.get_rect(topleft=self.pos)
        self.group = {self}

    def update_rect(self):
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

class PuzzleGame:
    def __init__(self):
        self.state = "MENU" # Estados: MENU, PLAYING
        self.level = 1
        self.image_index = 0
        self.score = 0
        self.pieces = []
        self.selected_piece = None
        self.level_completed = False
        self.hitting_border = False # Para la señal visual
        
        self.difficulty_settings = {
            1: {"grid": 2, "name": "Fácil (2x2)"},
            2: {"grid": 3, "name": "Normal (3x3)"},
            3: {"grid": 4, "name": "Medio (4x4)"},
            4: {"grid": 5, "name": "Avanzado (5x5)"},
            5: {"grid": 6, "name": "Experto (6x6)"}
        }
        
        # Botones del menú
        self.menu_buttons = []
        for i in range(1, 6):
            rect = pygame.Rect(SCREEN_WIDTH//2 - 150, 200 + (i*80), 300, 60)
            self.menu_buttons.append((i, rect))

    def load_challenge(self):
        self.pieces = []
        self.selected_piece = None
        self.level_completed = False
        self.start_time = pygame.time.get_ticks()
        
        grid_size = self.difficulty_settings[self.level]["grid"]
        img_path = get_image_path(self.level, self.image_index)
        
        full_img = pygame.image.load(img_path).convert()
        full_img = pygame.transform.scale(full_img, (PLAY_AREA_SIZE, PLAY_AREA_SIZE))
        
        p_w = PLAY_AREA_SIZE // grid_size
        p_h = PLAY_AREA_SIZE // grid_size
        
        for y in range(grid_size):
            for x in range(grid_size):
                rect_sub = pygame.Rect(x * p_w, y * p_h, p_w, p_h)
                sub_surface = full_img.subsurface(rect_sub).copy()
                self.pieces.append(Piece(len(self.pieces), sub_surface, x, y, p_w, p_h))

    def move_group_with_clamping(self, piece, dx, dy):
        """Mueve el grupo de piezas y evita que se salgan del recuadro."""
        self.hitting_border = False
        
        # 1. Calcular los límites actuales del grupo completo
        min_x = min(p.pos.x for p in piece.group)
        max_x = max(p.pos.x + p.w for p in piece.group)
        min_y = min(p.pos.y for p in piece.group)
        max_y = max(p.pos.y + p.h for p in piece.group)
        
        # 2. Predecir nueva posición y bloquear si excede los bordes
        can_move_x = True
        can_move_y = True
        
        if min_x + dx < PLAY_AREA_X or max_x + dx > PLAY_AREA_X + PLAY_AREA_SIZE:
            can_move_x = False
            self.hitting_border = True
            
        if min_y + dy < PLAY_AREA_Y or max_y + dy > PLAY_AREA_Y + PLAY_AREA_SIZE:
            can_move_y = False
            self.hitting_border = True

        # 3. Aplicar movimiento solo en ejes permitidos
        final_dx = dx if can_move_x else 0
        final_dy = dy if can_move_y else 0
        
        for p in piece.group:
            p.pos.x += final_dx
            p.pos.y += final_dy
            p.update_rect()

    def check_connections(self, moved_piece):
        grid_size = self.difficulty_settings[self.level]["grid"]
        SNAP_DIST = 25
        p_w = PLAY_AREA_SIZE // grid_size
        p_h = PLAY_AREA_SIZE // grid_size
        
        for p_moved in list(moved_piece.group):
            for p_other in self.pieces:
                if p_other in moved_piece.group: continue
                
                dx_grid = p_moved.grid_x - p_other.grid_x
                dy_grid = p_moved.grid_y - p_other.grid_y
                
                if abs(dx_grid) + abs(dy_grid) == 1:
                    target_x = p_other.pos.x + (dx_grid * p_w)
                    target_y = p_other.pos.y + (dy_grid * p_h)
                    
                    dist = pygame.Vector2(p_moved.pos.x, p_moved.pos.y).distance_to((target_x, target_y))
                    
                    if dist < SNAP_DIST:
                        # Acoplamiento perfecto
                        corr_dx = target_x - p_moved.pos.x
                        corr_dy = target_y - p_moved.pos.y
                        for p in moved_piece.group:
                            p.pos.x += corr_dx
                            p.pos.y += corr_dy
                            p.update_rect()
                        
                        new_grp = p_moved.group.union(p_other.group)
                        for p_update in new_grp: p_update.group = new_grp

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if self.state == "MENU":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for lvl_num, rect in self.menu_buttons:
                        if rect.collidepoint(event.pos):
                            self.level = lvl_num
                            self.load_challenge()
                            self.state = "PLAYING"

            elif self.state == "PLAYING":
                if event.type == pygame.MOUSEBUTTONDOWN and not self.level_completed:
                    for p in reversed(self.pieces):
                        if p.rect.collidepoint(event.pos):
                            self.selected_piece = p
                            self.pieces.remove(p); self.pieces.append(p)
                            break
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.selected_piece:
                        self.check_connections(self.selected_piece)
                        self.selected_piece = None
                        if len(self.pieces[0].group) == len(self.pieces):
                            self.level_completed = True
                            self.score += self.level * 100
                elif event.type == pygame.MOUSEMOTION and self.selected_piece:
                    self.move_group_with_clamping(self.selected_piece, event.rel[0], event.rel[1])
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = "MENU"
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.level_completed:
                    self.image_index = (self.image_index + 1) % 5
                    self.load_challenge()

    def draw(self):
        screen.fill(BG_COLOR)
        
        if self.state == "MENU":
            title = FONT_BIG.render("Puzzle Jigsaw Master", True, HIGHLIGHT_COLOR)
            screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
            
            for lvl_num, rect in self.menu_buttons:
                color = PANEL_COLOR if not rect.collidepoint(pygame.mouse.get_pos()) else HIGHLIGHT_COLOR
                pygame.draw.rect(screen, color, rect, border_radius=12)
                txt = FONT_MED.render(f"Nivel {lvl_num}: {self.difficulty_settings[lvl_num]['name']}", True, (255,255,255) if color == PANEL_COLOR else (0,0,0))
                screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))

        elif self.state == "PLAYING":
            # Recuadro de juego con señal visual
            border_color = WARNING_COLOR if self.hitting_border else FRAME_COLOR
            pygame.draw.rect(screen, (15, 15, 20), (PLAY_AREA_X, PLAY_AREA_Y, PLAY_AREA_SIZE, PLAY_AREA_SIZE))
            pygame.draw.rect(screen, border_color, (PLAY_AREA_X - 4, PLAY_AREA_Y - 4, PLAY_AREA_SIZE + 8, PLAY_AREA_SIZE + 8), 4)

            for p in self.pieces:
                screen.blit(p.image, p.rect)
                pygame.draw.rect(screen, (50, 50, 70), p.rect, 1)

            # UI Lateral
            pygame.draw.rect(screen, PANEL_COLOR, (700, 0, 300, SCREEN_HEIGHT))
            screen.blit(FONT_MED.render(f"PUNTOS: {self.score}", True, HIGHLIGHT_COLOR), (720, 50))
            screen.blit(FONT_TEXT.render(f"Esc para Menú", True, TEXT_COLOR), (720, 650))
            
            if self.level_completed:
                win_txt = FONT_MED.render("¡LOGRADO!", True, HIGHLIGHT_COLOR)
                screen.blit(win_txt, (720, 300))
                screen.blit(FONT_TEXT.render("Espacio: Siguiente", True, TEXT_COLOR), (720, 340))

        pygame.display.flip()

if __name__ == "__main__":
    game = PuzzleGame()
    while True:
        game.handle_events()
        game.draw()
        clock.tick(60)