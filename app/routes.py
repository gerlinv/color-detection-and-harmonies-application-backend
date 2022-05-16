import ast

from flask import request

from app import app
from app.color.color_service import ColorService
from app.color_harmonies.color_harmonies_service import ColorHarmoniesService

color_service = ColorService()
color_harmonies_service = ColorHarmoniesService()


@app.route('/colors/name', methods=['POST'])
def find_color():
    img = request.json['img']
    precise_color_detection = request.json['precise']
    x = request.json['x']
    y = request.json['y']

    return color_service.find_color(img, precise_color_detection, x, y)


@app.route('/colors', methods=['GET'])
def get_colors():
    return color_service.get_colors()


@app.route('/colors', methods=['POST'])
def add_color():
    name = request.json['name']
    rgb = ast.literal_eval(request.json['rgb'])
    hue = request.json['hue']
    comment = request.json['comment']

    return color_service.add_color(name, rgb, hue, comment, True)


@app.route('/colors', methods=['PUT'])
def update_color():
    color_id = request.json['id']
    new_comment = request.json['comment']

    return color_service.update_color(color_id, new_comment)


@app.route('/colors', methods=['DELETE'])
def delete_color():
    color_id = request.json['id']

    return color_service.delete_color(color_id)


@app.route('/harmonies/info', methods=['POST'])
def calculate_harmonies():
    val1 = ast.literal_eval(request.json['val1'])
    val2 = ast.literal_eval(request.json['val2'])

    return color_harmonies_service.calculate_harmonies(val1, val2)


@app.route('/harmonies/colors', methods=['POST'])
def get_harmonies():
    harmonies_id = request.json['id']

    return color_harmonies_service.get_harmonies(harmonies_id)


@app.route('/harmonies', methods=['GET'])
def get_all_harmonies():
    return color_harmonies_service.get_all_harmonies()


@app.route('/harmonies', methods=['POST'])
def add_harmonies():
    rgb1 = ast.literal_eval(request.json['rgb1'])
    rgb2 = ast.literal_eval(request.json['rgb2'])
    name1 = request.json['name1']
    name2 = request.json['name2']
    hue1 = request.json['hue1']
    hue2 = request.json['hue2']
    ana = request.json['ana']
    comp = request.json['comp']
    mono = request.json['mono']
    neutral = request.json['neutral']
    comment = request.json['comment']

    return color_harmonies_service.add_harmonies(rgb1, rgb2, name1, name2, hue1, hue2,
                                                 ana, comp, mono, neutral, comment)


@app.route('/harmonies', methods=['PUT'])
def update_harmonies():
    harmonies_id = request.json['id']
    new_comment = request.json['comment']

    return color_harmonies_service.update_harmonies(harmonies_id, new_comment)


@app.route('/harmonies', methods=['DELETE'])
def delete_color_harmonies():
    color_harmonies_id = request.json['id']

    return color_harmonies_service.delete_harmonies(color_harmonies_id)
