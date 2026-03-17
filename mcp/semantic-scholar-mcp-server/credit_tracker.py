import time
from threading import Lock

# Credit cost per tool
TOOL_CREDITS = {
    "search_papers": 1,
    "search_papers_bulk": 2,
    "match_paper_by_title": 1,
    "get_autocomplete": 1,
    "get_paper_details": 1,
    "get_paper_authors": 1,
    "get_paper_citations": 1,
    "get_paper_references": 1,
    "get_papers_batch": 2,
    "search_by_topic": 1,
    "search_authors": 1,
    "get_author_details": 1,
    "get_author_papers": 1,
    "get_authors_batch": 2,
    "search_snippets": 1,
    "get_recommendations_for_paper": 1,
    "get_recommendations_bulk": 1,
}


class CreditTracker:
    def __init__(self):
        self._lock = Lock()
        self._total = 0
        self._calls: list[dict] = []

    def record(self, tool_name: str):
        cost = TOOL_CREDITS.get(tool_name, 0)
        with self._lock:
            self._total += cost
            self._calls.append({
                "tool": tool_name,
                "cost": cost,
                "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            })

    @property
    def total(self) -> int:
        with self._lock:
            return self._total

    @property
    def call_count(self) -> int:
        with self._lock:
            return len(self._calls)

    def summary(self) -> str:
        with self._lock:
            if not self._calls:
                return "No API calls recorded yet."
            lines = [f"Total credits used: {self._total} | Total calls: {len(self._calls)}\n"]
            # Group by tool
            tool_stats: dict[str, dict] = {}
            for call in self._calls:
                name = call["tool"]
                if name not in tool_stats:
                    tool_stats[name] = {"count": 0, "cost": 0}
                tool_stats[name]["count"] += 1
                tool_stats[name]["cost"] += call["cost"]
            for name, stats in sorted(tool_stats.items(), key=lambda x: -x[1]["cost"]):
                lines.append(f"  {name}: {stats['count']} calls, {stats['cost']} credits")
            # Recent calls
            lines.append(f"\nRecent calls (last 10):")
            for call in self._calls[-10:]:
                lines.append(f"  [{call['time']}] {call['tool']} (-{call['cost']})")
            return "\n".join(lines)

    def reset(self):
        with self._lock:
            self._total = 0
            self._calls.clear()


# Singleton
tracker = CreditTracker()
