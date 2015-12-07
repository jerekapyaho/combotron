import argparse
import logging
import sys
import os
from flask import Flask, Response, request
import json

app = Flask(__name__)

# Set up the gear data
lenses = [{'name': 'Helga Viking', 'tag': 'HelgaViking'},
          {'name': 'Lucifer VI', 'tag': 'LuciferVI'},
          {'name': 'Roboto Glitter', 'tag': 'RobotoGlitter'},
          {'name': 'Salvador 84', 'tag': 'Salvador84'},
          {'name': 'Melodie', 'tag': 'Melodie'},
          {'name': 'Chunky', 'tag': 'Chunky'},
          {'name': 'Tejas', 'tag': 'Tejas'},
          {'name': 'Watts', 'tag': 'Watts'},
          {'name': 'Libatique 73', 'tag': 'Libatique73'},
          {'name': 'Matty ALN', 'tag': 'MattyALN'},
          {'name': 'Lucas AB2', 'tag': 'LucasAB2'},
          {'name': 'Susie', 'tag': 'Susie'},
          {'name': 'James M', 'tag': 'JamesM'},
          {'name': 'Loftus', 'tag': 'Loftus'},
          {'name': 'Americana', 'tag': 'Americana'},
          {'name': 'Adler 9009', 'tag': 'Adler9009'},
          {'name': 'Hornbecker', 'tag': 'Hornbecker'},
          {'name': 'Kaimal Mark II', 'tag': 'KaimalMarkII'},
          {'name': 'Wonder', 'tag': 'Wonder'},
          {'name': 'Buckhorst H1', 'tag': 'BuckhorstH1'},
          {'name': 'Bettie XL', 'tag': 'BettieXL'},
          {'name': 'Ray Mark II', 'tag': 'RayMarkII'},
          {'name': 'Akira', 'tag': 'Akira'},          
          {'name': 'John S', 'tag': 'JohnS'},
          {'name': 'Foxy', 'tag': 'Foxy'},
          {'name': 'Burke', 'tag': 'Burke'},
          {'name': 'G2', 'tag': 'G2'},
          {'name': 'Jane', 'tag': 'Jane'},
          {'name': 'Chivas', 'tag': 'Chivas'},
          {'name': 'Florence', 'tag': 'Florence'},
          {'name': 'Muir', 'tag': 'Muir'},
          {'name': 'Tinto 1884', 'tag': 'Tinto1884'},
          {'name': 'Diego', 'tag': 'Diego'},
          {'name': 'Madalena', 'tag': 'Madalena'},
          {'name': 'Lowy', 'tag': 'Lowy'},
          {'name': 'YUЯI 61', 'tag': 'YUЯI61'},
          {'name': 'Lincoln', 'tag': 'Lincoln'},
          {'name': 'Vincent', 'tag': 'Vincent'},
          {'name': 'Yoona', 'tag': 'Yoona'},
          {'name': 'Mabel', 'tag': 'Mabel'},
          {'name': 'Doris', 'tag': 'Doris'},
          {'name': 'Sergio', 'tag': 'Sergio'},
          {'name': 'Benedict', 'tag': 'Benedict'},
          {'name': 'Jack London', 'tag': 'JackLondon'},
          {'name': 'Le Allan', 'tag': 'LeAllan'},
          {'name': 'Hannah', 'tag': 'Hannah'},
          {'name': 'Savannah', 'tag': 'Savannah'},
          {'name': 'Eric', 'tag': 'Eric'},
          {'name': 'Gregory', 'tag': 'Gregory'},
          {'name': 'Dee', 'tag': 'Dee'},
          {'name': 'Mark', 'tag': 'Mark'},
          {'name': 'Emma', 'tag': 'Emma'},
          {'name': 'Ruddy', 'tag': 'Ruddy'},
          {'name': 'Victoria', 'tag': 'Victoria'},
          {'name': 'Neville', 'tag': 'Neville'},
          {'name': 'Leonard', 'tag': 'Leonard'},
          {'name': 'Murray', 'tag': 'Murray'},
          {'name': 'Jing', 'tag': 'Jing'},
          {'name': 'Bruno', 'tag': 'Bruno'},
          {'name': 'Anne-Marie', 'tag': 'AnneMarie'},
          {'name': 'Jimmy',  'tag': 'Jimmy'},
          {'name': 'Aatto', 'tag': 'Aatto'}]
          
films = [{'name': 'Ina''s 1982', 'tag': 'Inas1982'},
         {'name': 'BlacKeys B+W', 'tag': 'BlacKeysBW'},
         {'name': 'BlacKeys SuperGrain', 'tag': 'BlacKeysSuperGrain'},
         {'name': 'Claunch 72 Monochrome', 'tag': 'Claunch'},
         {'name': 'Ina''s 1935', 'tag': 'Inas1935'},
         {'name': 'Alfred Infrared', 'tag': 'AlfredInfrared'},
         {'name': 'Float', 'tag': 'Float'},
         {'name': 'AO DLX', 'tag': 'AODLX'},
         {'name': 'Ina''s 1969', 'tag': 'Inas1969'},
         {'name': 'AO BW', 'tag': 'AOBW'},
         {'name': 'DC', 'tag': 'DC'},
         {'name': 'Blanko Freedom 13', 'tag': 'BlankoFreedom13'},
         {'name': 'Shilshole', 'tag': 'Shilshole'},
         {'name': 'US1776', 'tag': 'US1776'},
         {'name': 'Dylan', 'tag': 'Dylan'},
         {'name': 'Rock BW-11', 'tag': 'RockBW11'},
         {'name': 'RTV', 'tag': 'RTV'},
         {'name': 'RTV Shout!', 'tag': 'RTVShout'},
         {'name': 'Big Up', 'tag': 'BigUp'},
         {'name': 'Irom 2000', 'tag': 'Irom2000'},
         {'name': 'Kodama', 'tag': 'Kodama'},
         {'name': 'OG', 'tag': 'OG'},
         {'name': 'Sugar', 'tag': 'Sugar'},         
         {'name': 'Blanko', 'tag': 'Blanko'},
         {'name': 'BlacKeys Extra Fine', 'tag': 'BlacKeysExtraFine'},
         {'name': 'Estrada 83', 'tag': 'Estrada83'},
         {'name': 'Sequoia', 'tag': 'Sequoia'},
         {'name': 'Robusta', 'tag': 'Robusta'},
         {'name': 'Gotland', 'tag': 'Gotland'},
         {'name': 'Uchitel 20', 'tag': 'Uchitel20'},
         {'name': 'Blanko C16', 'tag': 'BlankoC16'},
         {'name': 'D-Type Plate', 'tag': 'DTypePlate'},
         {'name': 'C-Type Plate', 'tag': 'CTypePlate'},
         {'name': 'DreamCanvas', 'tag': 'DreamCanvas'},
         {'name': 'Cano Cafenol', 'tag': 'CanoCafenol'},
         {'name': 'Blanko Noir', 'tag': 'BlankoNoir'},
         {'name': 'W40', 'tag': 'W40'},
         {'name': 'Pistil', 'tag': 'Pistil'},
         {'name': 'Blanko BL4', 'tag': 'BlankoBL4'},
         {'name': 'Rasputin', 'tag': 'Rasputin'},
         {'name': 'T. Roosevelt 26', 'tag': 'Roosevelt'},
         {'name': 'Rijks', 'tag': 'Rijks'},
         {'name': 'Sussex', 'tag': 'Sussex'},
         {'name': 'Blanko 일', 'tag': 'Blanko1'},
         {'name': 'Maximus LXIX', 'tag': 'MaximusLXIX'},
         {'name': 'Dixie', 'tag': 'Dixie'},
         {'name': 'Telegraph', 'tag': 'Telegraph'},
         {'name': 'Hackney', 'tag': 'Hackney'},
         {'name': 'Queen West', 'tag': 'QueenWest'},
         {'name': 'Otto', 'tag': 'Otto'},
         {'name': 'Louis XIV Infrared', 'tag': 'LouisXIV'},
         {'name': 'Love 81', 'tag': 'Love81'},
         {'name': 'Manneken', 'tag': 'Manneken'},
         {'name': 'Big Easy', 'tag': 'BigEasy'},
         {'name': 'BlacKeys 44', 'tag': 'BlacKeys44'},
         {'name': 'Lite', 'tag': 'Lite'},
         {'name': 'Stand Up', 'tag': 'StandUp'},
         {'name': 'Daydream', 'tag': 'Daydream'},
         {'name': 'Indio', 'tag': 'Indio'},
         {'name': 'Tilda', 'tag': 'Tilda'},
         {'name': 'Gongbi', 'tag': 'Gongbi'},
         {'name': 'Mount Royal', 'tag': 'Mount Royal'},
         {'name': 'Kodot XGrizzled', 'tag': 'KodotXGrizzled'},
         {'name': 'Reeta', 'tag': 'Reeta'}]

flashes = [{'name': 'Standard', 'tag': 'Standard'},
           {'name': 'Cherry Shine', 'tag': 'CherryShine'},
           {'name': 'Cadet Blue Gel', 'tag': 'CadetBlueGel'},
           {'name': 'RedEye Gel', 'tag': 'RedEyeGel'},
           {'name': 'Berry Pop', 'tag': 'BerryPop'},
           {'name': 'Jolly Rainbo 2X', 'tag': 'JollyRainbo2X'},
           {'name': 'Tasty Pop', 'tag': 'TastyPop'},
           {'name': 'Pop Rox', 'tag': 'PopRox'},
           {'name': 'Laser Lemon Gel', 'tag': 'LaserLemonGel'},
           {'name': 'Triple Crown', 'tag': 'TripleCrown'},
           {'name': 'Juicy Orange Gel', 'tag': 'JuicyOrangeGel'},
           {'name': 'Purple Raindrops Gel', 'tag': 'PurpleRaindropsGel'},
           {'name': 'Leprechaun Tears Gel', 'tag': 'LeprechaunTearsGel'},
           {'name': 'Cubic Gel', 'tag': 'CubicGel'},
           {'name': 'Triad Gel', 'tag': 'TriadGel'},
           {'name': 'Spiro Gel', 'tag': 'SpiroGel'},
           {'name': 'Dreampop', 'tag': 'Dreampop'}]

localized_no_flash_strings = {'en': 'No Flash',
                              'zh-Hans': '没开闪光灯',
                              'zh-Hant': '無閃光燈',
                              'nl': 'geen flits',
                              'fr': 'sans flash',
                              'de': 'Kein Blitz',
                              'id': 'Tanpa Blitz',
                              'it': 'Nessun Flash',
                              'ja': 'フラッシなし',
                              'ko': '플래시 없음',
                              'ms': 'Tiada Lampu Kilat',
                              'pt-BR': 'Sem flash',
                              'pt-PT': 'sem flash',
                              'ru': 'без вспышки',
                              'es': 'sin flash',
                              'sv': 'No Blixt'}

def lens_part(parts):
    return parts[0]
    
def film_part(parts):
    return parts[1]
    
def flash_part(parts):
    return parts[2]

def metadata_language(md):
    lang = None
    if ' Lens, ' in md:
        lang = 'en'
    elif '-lens, ' in md:
        lang = 'nl'
    elif 'Objectif' in md:
        lang = 'fr'
    elif ' Lins, ' in md:
        lang = 'sv'
    elif ' Lentes, ' in md:
        lang = 'pt-BR'
    elif ' レンズ, ' in md:
        lang = 'ja'
    elif ' объектив, ' in md:
        lang = 'ru'
    elif ' Lensa, ' in md:
        lang = 'ms'
    elif ' 렌즈, ' in md:
        lang = 'ko'
    elif ' 镜头，' in md:
        lang = 'zh-Hans'
    elif ' 鏡頭, ' in md:
        lang = 'zh-Hant'
    else:
        if md.startswith('Lente '):
            if ', Pellicola ' in md:
                lang = 'it'
            elif ', rolo ' in md:
                lang = 'pt-PT'
            else:
                lang = 'es'
                
    return lang


part_info = {'en': [' Lens', ' Film', ' Flash'],
             'nl': ['-lens', '-filmrol', '-flitser'],
             'fr': ['Objectif ', 'Film ', 'Flash '],
             'de': [' Linse', ' Film', ' Blitz'],
             'it': ['Lente ', 'Pellicola ', 'Flash '],
             'es': ['Lente ', 'Película ', 'Flash '],
             'pt-PT': ['Lente ', 'rolo ', 'flash '],
             'sv': [' Lins', ' Film', ' Blixt'],
             'pt-BR': [' Lentes', ' Filme', ' Flash'],
             'ja': [' レンズ', ' フィルム', ' フラッシュ'],
             'ru': [' объектив', ' пленка', ' вспышка'],
             'id': ['Lensa ', 'Film ', 'Blitz '],      
             'ms': [' Lensa', ' Filem', ' Lampu Kilat'],
             'ko': [' 렌즈', ' 필름', ' 플래시'],  
             'zh-Hans': [' 镜头', ' 胶卷', ' 闪光灯'],
             'zh-Hant': [' 鏡頭', ' 膠片', ' 閃光燈']}

# If a language is in this set, it has the gear name after the noun.
# Otherwise the gear name comes before the noun (the majority).
languages_with_position_after = set(['fr', 'it', 'es', 'pt-PT', 'id'])

def name_from_part(part, localized_part, name_pos):
    result = ''
    part_pos = part.find(localized_part)
    if part_pos != -1:
        if name_pos == 'before':
            result = part[:part_pos]
        elif name_pos == 'after':
            result = part[part_pos:len(localized_part)]
    return result

def extracted_names(parts, lang, name_pos):
    lang_info = part_info[lang]
    
    result = {'lens': name_from_part(lens_part(parts), lens_part(lang_info), name_pos),
              'film': name_from_part(film_part(parts), film_part(lang_info), name_pos),
              'flash': 'No'}
    
    if flash_part(parts) != localized_no_flash_strings[lang]: 
        result['flash'] = name_from_part(flash_part(parts), flash_part(lang_info), name_pos)
        
    return result
    

def gear_names(md, lang):
    # Some Chinese metadata strings have the FULLWIDTH COMMA character.
    # Replace it with a regular comma and space, then split into parts.
    fixed_comma = md.replace('\N{FULLWIDTH COMMA}', ', ')
    parts = fixed_comma.split(', ')
    
    name_pos = 'before'
    if lang in languages_with_position_after:
        name_pos = 'after'

    result = None
    if lang in part_info:
        result = extracted_names(parts, lang, name_pos)
        
    return result


def gear_tags(names):

    pass  


@app.route('/')
def index():
    return 'Nothing to see here. Move along.'
    
@app.route('/lens')
def lens():
    result = {'status': 'success',
              'data': lenses}
    js = json.dumps(result)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@app.route('/film')
def film():
    result = {'status': 'success',
              'data': films}
    js = json.dumps(result)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@app.route('/flash')
def flash():
    result = {'status': 'success',
              'data': flashes}
    js = json.dumps(result)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@app.route('/analyze', methods=['POST'])
def analyze():
    if request.headers['Content-Type'] == 'application/json':
        payload = request.get_json()

        model = payload['Model']
        if model >= 300:
            result = {'status': 'fail',
                      'data': {'title': 'Cannot parse Software metadata for Hipstamatic 300 and later. Maybe later.'}}
        else:
            software = payload['Software']
            lang = metadata_language(software)
            if lang != None:
                tags = gear_names(software, lang)
                result = {'status': 'success',
                          'data': {'tags': tags, 'lang': lang}}
            else:
                result = {'status': 'fail',
                          'data': {'title': 'No language determined, maybe bad metadata?'}}
    else:
        message = 'No JSON payload found in request.'
        app.logger.error(message)
        result = {'status': 'fail',
                  'data': {'title': message}}
    
    js = json.dumps(result)
    
    resp = Response(js, status=200, mimetype='application/json')
    return resp
    
if __name__ == '__main__':
    app.run()
