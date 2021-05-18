import numpy as np

from matplotlib import pyplot as plt
from PIL import Image, ImageDraw
from src.map import Map
import cv2
import random


def draw(grid_map: Map, solutions, agents):
    k = 20
    h_im = grid_map.height * k
    w_im = grid_map.width * k

    max_t = max(map(len, solutions))

    color = lambda: (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    agent_color_map = {}
    for i in range(len(agents)):
        agent_color_map[i] = color()

    sequence = []
    for t in range(max_t):
        im = Image.new('RGB', (w_im, h_im), color='white')
        draw = ImageDraw.Draw(im)
        for i in range(grid_map.height):
            for j in range(grid_map.width):
                if grid_map.cells[i][j] == 1:
                    draw.rectangle((j * k, i * k, (j + 1) * k - 1, (i + 1) * k - 1), fill=(70, 80, 80))
        for i, agent in enumerate(agents):
            (s_i, s_j), (f_i, f_j) = agent
            draw.rectangle((s_j * k, s_i * k, (s_j + 1) * k - 1, (s_i + 1) * k - 1), fill=(255, 255, 255),
                           width=1, outline=agent_color_map[i])
            draw.rectangle((f_j * k, f_i * k, (f_j + 1) * k - 1, (f_i + 1) * k - 1), fill=(255, 255, 255),
                           width=1, outline=agent_color_map[i])
        for i, solution in enumerate(solutions):
            if len(solution) > t:
                step_i, step_j = solution[t]
            else:
                step_i, step_j = solution[-1]
            draw.rectangle(((step_j + 0.25) * k, (step_i + 0.25) * k, (step_j + 0.75) * k - 1, (step_i + 0.75) * k - 1),
                           fill=agent_color_map[i], width=0)

        sequence.append(np.array(im)[:, :, ::-1])

    cur_i = 0
    while True:
        cv2.imshow('Video', cv2.resize(sequence[cur_i], (360, round(360 / w_im * h_im))))
        key = cv2.waitKey(0) & 0xFF
        if key == ord('a'):
            cur_i = max(cur_i - 1, 0)
        if key == ord('d'):
            cur_i = min(len(sequence) - 1, cur_i + 1)
        if key == ord('q'):
            break
