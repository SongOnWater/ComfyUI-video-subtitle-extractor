from .backend.main import SubtitleExtractor
import os 
import pysrt

class SubtitleExtractorWrapper:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { 
                "video_path": ("STRING", {"default":"",}),
                "subtitle_area": ("BBOX",{}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("srt_path", "srt")
    FUNCTION = "wrapper_run"
    OUTPUT_NODE = True
    def wrapper_run(self,video_path,subtitle_area):
            if subtitle_area is not None:
                x, y, width, height = subtitle_area
                subtitle_area = (  y, y+height,x, x+width)
            se = SubtitleExtractor(video_path, subtitle_area)
            # 开始提取字幕z
            se.run() 
            srt_file=os.path.join(os.path.splitext(video_path)[0] + '.srt')
            subs = pysrt.open(srt_file, encoding='utf-8')
            return (srt_file,subs.text)
    