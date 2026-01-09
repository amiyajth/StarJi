from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple
import re
import pickle

# 依赖 sklearn（大多数环境有；没有的话我再给你纯 Python 版本）
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


KB_DIR = Path(__file__).resolve().parents[3] / "data" / "kb" / "cities"
INDEX_DIR = Path(__file__).resolve().parents[3] / "data" / "kb" / "_index"
INDEX_DIR.mkdir(parents=True, exist_ok=True)


def _clean_text(s: str) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _chunk_text(text: str, chunk_size: int = 450, overlap: int = 80) -> List[str]:
    """
    简单分块：按字符长度切。足够做 V0。
    chunk_size 450 左右通常能控制 prompt 不爆。
    """
    text = _clean_text(text)
    if not text:
        return []

    chunks = []
    i = 0
    while i < len(text):
        chunk = text[i : i + chunk_size]
        chunks.append(chunk)
        i += max(1, chunk_size - overlap)
    return chunks


@dataclass
class CityIndex:
    city: str
    chunks: List[str]
    vectorizer: TfidfVectorizer
    matrix: object  # sparse matrix


def _index_path(city: str) -> Path:
    return INDEX_DIR / f"{city}.pkl"


def build_city_index(city: str) -> CityIndex | None:
    """
    从 data/kb/cities/{city}.md 构建索引并落盘
    """
    md_path = KB_DIR / f"{city}.md"
    if not md_path.exists():
        return None

    text = md_path.read_text(encoding="utf-8", errors="ignore")
    chunks = _chunk_text(text)
    if not chunks:
        return None

    vectorizer = TfidfVectorizer(
        analyzer="char",
        ngram_range=(2, 4),
        min_df=1
    )
    matrix = vectorizer.fit_transform(chunks)
    idx = CityIndex(city=city, chunks=chunks, vectorizer=vectorizer, matrix=matrix)

    with open(_index_path(city), "wb") as f:
        pickle.dump(idx, f)

    return idx


def load_city_index(city: str) -> CityIndex | None:
    p = _index_path(city)
    if p.exists():
        try:
            with open(p, "rb") as f:
                return pickle.load(f)
        except Exception:
            pass
    # 没有索引或坏了就重建
    return build_city_index(city)


def rag_search_city(city: str, query: str, top_k: int = 4) -> List[Tuple[float, str]]:
    """
    返回：[(score, chunk), ...]
    """
    idx = load_city_index(city)
    if not idx:
        return []

    q = _clean_text(query)
    q_vec = idx.vectorizer.transform([q])
    sims = cosine_similarity(q_vec, idx.matrix)[0]  # shape: (n_chunks,)

    # 取 top_k
    ranked = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)[:top_k]
    results = []
    for i, score in ranked:
        if score <= 0:
            continue
        results.append((float(score), idx.chunks[i]))
    return results


def format_rag_results_for_prompt(city: str, results: List[Tuple[float, str]]) -> str:
    if not results:
        return f"（暂无 {city} 攻略知识库命中结果）"

    lines = [f"【{city} 攻略知识库检索结果（Top）】"]
    for score, chunk in results:
        lines.append(f"- 相似度 {score:.3f}：{chunk}")
    return "\n".join(lines)
