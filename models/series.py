from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class Series:
    id: int
    name: str
    language: str
    genres: List[str]
    rating: Optional[float]
    status: str
    premiered: str
    ended: str
    runtime: Optional[int]
    summary: str

    @classmethod
    def from_tvmaze_dict(cls, data: Dict[str, Any]) -> Optional["Series"]:
        show = data.get("show", data)
        if not show or "id" not in show:
            return None

        rating_data = show.get("rating") or {}
        return cls(
            id=show.get("id", 0),
            name=show.get("name", ""),
            language=show.get("language", "") or "",
            genres=show.get("genres", []),
            rating=rating_data.get("average"),
            status=show.get("status", ""),
            premiered=show.get("premiered", "") or "",
            ended=show.get("ended", "") or "",
            runtime=show.get("runtime"),
            summary=show.get("summary", "") or "",
        )

    @classmethod
    def from_tvmaze_show(cls, show: Dict[str, Any]) -> "Series":
        rating_data = show.get("rating") or {}
        return cls(
            id=show.get("id", 0),
            name=show.get("name", ""),
            language=show.get("language", "") or "",
            genres=show.get("genres", []),
            rating=rating_data.get("average"),
            status=show.get("status", ""),
            premiered=show.get("premiered", "") or "",
            ended=show.get("ended", "") or "",
            runtime=show.get("runtime"),
            summary=show.get("summary", "") or "",
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "show": {
                "id": self.id,
                "name": self.name,
                "language": self.language,
                "genres": self.genres,
                "rating": {"average": self.rating},
                "status": self.status,
                "premiered": self.premiered,
                "ended": self.ended,
                "runtime": self.runtime,
                "summary": self.summary,
            }
        }
