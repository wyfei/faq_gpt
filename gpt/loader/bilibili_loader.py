from __future__ import annotations
from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader
import re
from typing import List, Tuple
from bilibili_api import video, Credential
from .bilibili_parser import parse_get_info, VideoInfo
from .sync import sync

class Bilibili_loader:
    """Loader that loads bilibili transcripts."""
    
    def __init__(
        self,
        url: str,
        sessdata: str,
        bili_jct: str,
        buvid3: str
    ):
        """Initialize with bilibili url."""
        self.url = url
        self.sessdata = sessdata
        self.bili_jct = bili_jct
        self.buvid3 = buvid3
    
    def load(self) -> VideoInfo:
        """Load from bilibili url."""
        video_info = self._get_bilibili_subs_and_info(self.url)
        # doc = Document(page_content=transcript, metadata=video_info)

        return video_info
    
    def _get_bilibili_subs_and_info(self, url: str) -> VideoInfo:
        try:
            from bilibili_api import video
        except ImportError:
            raise ValueError(
                "requests package not found, please install it with "
                "`pip install bilibili-api-python`"
            )

        SESSDATA = self.sessdata
        BILI_JCT = self.bili_jct
        BUVID3 = self.buvid3
        credential = Credential(sessdata=SESSDATA, bili_jct=BILI_JCT, buvid3=BUVID3)
        
        bvid = re.search(r"BV\w+", url)
        if bvid is not None:
            v = video.Video(bvid=bvid.group(), credential=credential)
        else:
            aid = re.search(r"av[0-9]+", url)
            if aid is not None:
                try:
                    v = video.Video(aid=int(aid.group()[2:]), credential=credential)
                except AttributeError:
                    raise ValueError(f"{url} is not bilibili url.")
            else:
                raise ValueError(f"{url} is not bilibili url.")
        
        video_info = sync(v.get_info()) 
        return parse_get_info(video_info=video_info)
