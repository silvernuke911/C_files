 for y in range(start_y, end_y, grid_spacing):
        sy = (vec2(0, y) - camera_center) * zoom + screen_center
        # ex = (vec2(screen_width, y) - camera_center) * zoom + screen_center
        pygame.draw.line(screen, grid_color, (0, sy.y), (screen_width, sy.y), 1)
    