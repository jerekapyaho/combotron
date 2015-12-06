import argparse
import logging
import sys


# Set up logging
logger = logging.getLogger('combotron')
logger.setLevel(logging.DEBUG)

# Create console handler and set level to debug
log_console_handler = logging.StreamHandler()
log_console_handler.setLevel(logging.DEBUG)

# Prepare formatter for log messages
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_console_handler.setFormatter(log_formatter)
logger.addHandler(log_console_handler)

# Set up the gear data
lenses = [{'name': 'John S', 'tag': 'John S'},
          {'name': 'Jane',   'tag': 'Jimmy'},
          {'name': 'Jimmy',  'tag': 'Jimmy'},
          {'name': 'KaimalMarkII', 'tag': 'Kaimal Mark II'}]

films = [{'name': 'Blanko', 'tag': 'Blanko'},
         {'name': 'Ina''s 1969', 'tag': 'Inas1969'},
         {'name': 'Kodot XGrizzled', 'tag': 'KodotXGrizzled'},
         {'name': 'Ina''s 1982', 'tag': 'Inas1982'}]

flashes = [{'name': 'Standard', 'tag': 'Standard'},
           {'name': 'Dreampop', 'tag': 'Dreampop'},
           {'name': 'Cherry Shine', 'tag': 'CherryShine'},
           {'name': 'Cadet Blue Gel', 'tag': 'CadetBlueGel'}]

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
             'nl': ['-lens', '-filmrol', '-flitser']}

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
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyze the metadata of a Hipstamatic photo by parsing the Software key in the {TIFF} metadata.')
    parser.add_argument('-m', '--model', help='The Hipstamatic model number from the {TIFF} metadata Model key')
    parser.add_argument('-s', '--software', help='The software string from the {TIFF} metadata Software key')
    args = parser.parse_args()
    logger.info('Software string = "%s"' % args.software)

    model = int(args.model)
    logger.info('Hipstamatic model = %d' % model)
    if model >= 300:
        logger.error('Cannot parse Software metadata for Hipstamatic 300 and later. Maybe later.')
        sys.exit(-1)
            
    lang = metadata_language(args.software)
    if lang != None:
        logger.info('Metadata language = ' + lang)
        result = gear_names(args.software, lang)
        result['lang'] = lang
        print(result)
    else:
        print('No language determined, maybe bad metadata?')
