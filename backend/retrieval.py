import json
import math
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse
from backend.schemas import Citation

STOP = set("a an the is are to of in for and i my do does can what how with on visa student".split())


def tokens(text: str) -> list[str]:
    return [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP]


class KnowledgeBase:
    def __init__(self, directory: Path):
        self.chunks: list[Citation] = []
        ids = set()
        for path in sorted(directory.glob("*.json")):
            source = json.loads(path.read_text(encoding="utf-8"))
            for key in ("id", "title", "url", "reviewed", "text"):
                if not isinstance(source.get(key), str) or not source[key].strip():
                    raise ValueError(f"Invalid {key} in {path.name}")
            if source["id"] in ids or not re.fullmatch(r"[A-Za-z0-9_-]+", source["id"]):
                raise ValueError(f"Invalid or duplicate source id in {path.name}")
            if urlparse(source["url"]).scheme not in {"https", "http"}:
                raise ValueError(f"Source URL must use HTTP(S): {path.name}")
            ids.add(source["id"])
            for n, start in enumerate(range(0, len(source["text"]), 1400), 1):
                self.chunks.append(Citation(id=f"{source['id']}-{n}", title=source["title"],
                    url=source["url"], reviewed=source["reviewed"], excerpt=source["text"][start:start+1600]))

    def search(self, query: str, limit: int = 4) -> list[Citation]:
        words = set(tokens(query))
        docs = [Counter(tokens(c.title + " " + c.excerpt)) for c in self.chunks]
        scores = []
        for c, doc in zip(self.chunks, docs):
            score = sum((1 + math.log(doc[w])) * math.log(1 + len(docs) / sum(w in d for d in docs))
                        for w in words if doc[w])
            if score > 0:
                scores.append((score, c))
        return [c for _, c in sorted(scores, key=lambda pair: pair[0], reverse=True)[:limit]]
