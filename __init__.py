from .nodes import SubtitleExtractorWrapper
print("ComfyUI-video-subtitle-extractor loaded")
NODE_CLASS_MAPPINGS = {
     "VideoSubtitleExtractor": SubtitleExtractorWrapper,
}
NODE_DISPLAY_NAME_MAPPINGS = {
     "VideoSubtitleExtractor": "Video Subtitle Extractor",
}
__all__ = ['NODE_CLASS_MAPPINGS','NODE_DISPLAY_NAME_MAPPINGS']