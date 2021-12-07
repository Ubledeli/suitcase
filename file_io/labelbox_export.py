from PIL import Image
import numpy as np
from labelbox.data.annotation_types import Geometry
from labelbox import Client, OntologyBuilder
from tqdm import tqdm
import os


LB_API_KEY = "LONGEST_KEY_EVER"
PROJECT_ID = 'this long project id'
FOLDER_NAME = 'folder'

os.makedirs(f'{FOLDER_NAME}', exist_ok=True)
lb = Client(api_key=LB_API_KEY)
project = lb.get_project(PROJECT_ID)
labels = project.label_generator().as_list()
hex_to_rgb = lambda hex_color: tuple(int(hex_color[i+1:i+3], 16) for i in (0, 2, 4))
colors = {tool.name: hex_to_rgb(tool.color) for tool in OntologyBuilder.from_project(project).tools}
colors['ignore'] = 255, 0, 255
for label in tqdm(labels):
    image_np = label.data.value

    # Draw the annotations onto the source image
    for annotation in label.annotations:
        if isinstance(annotation.value, Geometry):
            image_np = annotation.value.draw(canvas=image_np, color=colors[annotation.name], thickness=5)
    img = Image.fromarray(image_np.astype(np.uint8))
    img.save(f'{FOLDER_NAME}/{label.data.external_id}')
print('done')
