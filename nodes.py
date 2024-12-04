import configparser
from .backend.main import SubtitleExtractor
import os 
import pysrt
from .backend import config


class SubtitleExtractorWrapper:
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.ini')
    INTERFACE_KEY_NAME_MAP = {
        '简体中文': 'ch',
        '繁體中文': 'chinese_cht',
        'English': 'en',
        '한국어': 'ko',
        '日本語': 'japan',
        'Tiếng Việt': 'vi',
        'Español': 'es'
    }
    
    interface_config = configparser.ConfigParser()
        # 设置语言
    LANGUAGE_DEF = 'ch'
    LANGUAGE_NAME_KEY_MAP = None
    LANGUAGE_KEY_NAME_MAP = None
    MODE_DEF = 'fast'
    MODE_NAME_KEY_MAP = None
    MODE_KEY_NAME_MAP = None


    def __init__(self):
        pass
 

       
    def parse_config(self, config_file):
        if not os.path.exists(config_file):
            self.interface_config.read(self.interface_file, encoding='utf-8')
            interface_def = self.interface_config['LanguageModeGUI']['InterfaceDefault']
            language_def = self.interface_config['LanguageModeGUI']['InterfaceDefault']
            mode_def = self.interface_config['LanguageModeGUI']['ModeFast']
            return interface_def, language_def, mode_def
        config = configparser.ConfigParser()
        config.read(config_file, encoding='utf-8')
        interface = config['DEFAULT']['Interface']
        language = config['DEFAULT']['Language']
        mode = config['DEFAULT']['Mode']
        self.interface_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend', 'interface',
                                           f"{self.INTERFACE_KEY_NAME_MAP[interface]}.ini")
        self._load_interface_text(self)
        interface_def = interface if interface in self.INTERFACE_KEY_NAME_MAP else \
            self.INTERFACE_DEF
        language_def = self.LANGUAGE_KEY_NAME_MAP[language] if language in self.LANGUAGE_KEY_NAME_MAP else \
            self.LANGUAGE_DEF
        mode_def = self.MODE_KEY_NAME_MAP[mode] if mode in self.MODE_KEY_NAME_MAP else self.MODE_DEF
        return interface_def, language_def, mode_def    
    

    @staticmethod
    def set_config(config_file, interface, language_code, mode):
        # 写入配置文件
        with open(config_file, mode='w', encoding='utf-8') as f:
            f.write('[DEFAULT]\n')
            f.write(f'Interface = {interface}\n')
            f.write(f'Language = {language_code}\n')
            f.write(f'Mode = {mode}\n')
    

    def _load_interface_text(self):
        self.interface_config.read(self.interface_file, encoding='utf-8')
        config_language_mode_gui = self.interface_config["LanguageModeGUI"]
        # 设置界面
        self.INTERFACE_DEF = config_language_mode_gui["InterfaceDefault"]

        self.LANGUAGE_DEF = config_language_mode_gui["LanguageCH"]
        self.LANGUAGE_NAME_KEY_MAP = {}
        for lang in config.MULTI_LANG:
            self.LANGUAGE_NAME_KEY_MAP[config_language_mode_gui[f"Language{lang.upper()}"]] = lang
        self.LANGUAGE_NAME_KEY_MAP = dict(sorted(self.LANGUAGE_NAME_KEY_MAP.items(), key=lambda item: item[1]))
        self.LANGUAGE_KEY_NAME_MAP = {v: k for k, v in self.LANGUAGE_NAME_KEY_MAP.items()}
        self.MODE_DEF = config_language_mode_gui['ModeFast']
        self.MODE_NAME_KEY_MAP = {
            config_language_mode_gui['ModeAuto']: 'auto',
            config_language_mode_gui['ModeFast']: 'fast',
            config_language_mode_gui['ModeAccurate']: 'accurate',
        }
        self.MODE_KEY_NAME_MAP = {v: k for k, v in self.MODE_NAME_KEY_MAP.items()}

    @classmethod
    def INPUT_TYPES(cls):
        interface_def, language_def, mode_def=cls.parse_config(cls,cls.config_file)
        return {
            "required": { 
                "video_path": ("STRING", {"default":"",}),
                "subtitle_area": ("BBOX",{}),
            },
            "optional": {
                "inter_lang":(list(config.INTERFACE_KEY_NAME_MAP.keys()),{"default":interface_def}),
                "sub_lang":(list(cls.LANGUAGE_NAME_KEY_MAP.keys()),{"default":language_def}),
                "mode":(list(cls.MODE_NAME_KEY_MAP.keys()),{"default":mode_def}),
                "use_gpu":("BOOLEAN", {"default":False})
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("srt_path", "srt")
    FUNCTION = "wrapper_run"
    OUTPUT_NODE = True
    def wrapper_run(self,video_path,subtitle_area,inter_lang,sub_lang,mode,use_gpu):
            sub_lang_code=self.LANGUAGE_NAME_KEY_MAP[sub_lang]
            self.set_config(self.config_file,inter_lang,sub_lang_code,mode)
            config.REC_CHAR_TYPE=sub_lang_code
            config.USE_GPU=use_gpu
            config.MODE_TYPE=mode

            if subtitle_area is not None:
                x, y, width, height = subtitle_area
                subtitle_area = (  y, y+height,x, x+width)
            se = SubtitleExtractor(video_path, subtitle_area)
            # 开始提取字幕z
            se.run() 
            srt_file=os.path.join(os.path.splitext(video_path)[0] + '.srt')
            with open(srt_file, 'r') as f:
                srt_content = f.read()
            return (srt_file,srt_content)
    