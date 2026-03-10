#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "rich"]
# ///
"""Hacker News CLI - Browse HN stories and comments."""

import argparse
import httpx
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from html import unescape
import re
import asyncio

console = Console()
BASE_URL = "https://hacker-news.firebaseio.com/v0"
ALGOLIA_URL = "https://hn.algolia.com/api/v1"

def strip_html(text: str) -> str:
    """Remove HTML tags and decode entities."""
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', '', text)
    return unescape(text)

async def async_fetch_item(client: httpx.AsyncClient, item_id: int) -> dict:
    try:
        r = await client.get(f"{BASE_URL}/item/{item_id}.json")
        if r.status_code == 200:
            return r.json() or {}
    except Exception:
        pass
    return {}

async def async_fetch_items(item_ids: list[int]) -> list[dict]:
    async with httpx.AsyncClient(timeout=10) as client:
        tasks = [async_fetch_item(client, i) for i in item_ids]
        results = await asyncio.gather(*tasks)
        return [r for r in results if r]

def fetch_item(item_id: int) -> dict:
    """Fetch a single item (story, comment, etc)."""
    try:
        r = httpx.get(f"{BASE_URL}/item/{item_id}.json", timeout=10)
        return r.json() if r.status_code == 200 else {}
    except Exception:
        return {}

def fetch_stories(endpoint: str, limit: int = 10) -> list[dict]:
    """Fetch stories from an endpoint."""
    try:
        r = httpx.get(f"{BASE_URL}/{endpoint}.json", timeout=10)
        if r.status_code != 200:
            return []
        ids = r.json()[:limit]
        return asyncio.run(async_fetch_items(ids))
    except Exception:
        return []

def display_stories(stories: list[dict], title: str):
    """Display stories in a table."""
    table = Table(title=title, show_lines=False)
    table.add_column("#", style="dim", width=3)
    table.add_column("Pts", style="green", width=5)
    table.add_column("Title", style="bold", overflow="fold")
    table.add_column("Domain", style="blue")
    table.add_column("Comments", style="cyan", width=8)
    table.add_column("ID", style="dim", width=10)

    for i, s in enumerate(stories, 1):
        url = s.get('url', '')
        domain = ""
        if url:
            try:
                domain = url.split('/')[2] if '//' in url else url
            except Exception:
                pass
        
        table.add_row(
            str(i),
            str(s.get('score', 0)),
            s.get('title', 'No title'),
            domain,
            str(s.get('descendants', 0)),
            str(s.get('id', ''))
        )
    console.print(table)

def display_story(story: dict, comment_limit: int = 10):
    """Display a story with comments."""
    rprint(f"\n[bold]{story.get('title', 'No title')}[/bold]")
    rprint(f"[green]{story.get('score', 0)} points[/green] by [cyan]{story.get('by', 'unknown')}[/cyan]") 
    if story.get('url'):
        rprint(f"[blue]{story.get('url')}[/blue]")
    if story.get('text'):
        rprint(f"\n{strip_html(story.get('text'))}")

    kids = story.get('kids', [])[:comment_limit]
    if kids:
        rprint(f"\n[bold]Top {len(kids)} comments:[/bold]\n")
        comments = asyncio.run(async_fetch_items(kids))
        for comment in comments:
            if comment and comment.get('text'):
                author = comment.get('by', 'unknown')
                text = strip_html(comment.get('text', ''))
                if len(text) > 800:
                    text = text[:800] + "..."
                rprint(f"[cyan]{author}[/cyan]: {text}\n")

def search_stories(query: str, limit: int = 10):
    """Search HN via Algolia."""
    try:
        r = httpx.get(f"{ALGOLIA_URL}/search", params={"query": query, "hitsPerPage": limit}, timeout=10)     
        if r.status_code != 200:
            rprint("[red]Search failed[/red]")
            return

        hits = r.json().get('hits', [])
        table = Table(title=f"Search: {query}", show_lines=False)
        table.add_column("#", style="dim", width=3)
        table.add_column("Pts", style="green", width=5)
        table.add_column("Title", style="bold", overflow="fold")
        table.add_column("Domain", style="blue")
        table.add_column("Comments", style="cyan", width=8)
        table.add_column("ID", style="dim", width=10)

        for i, h in enumerate(hits, 1):
            url = h.get('url', '')
            domain = ""
            if url:
                try:
                    domain = url.split('/')[2] if '//' in url else url
                except Exception:
                    pass
            
            table.add_row(
                str(i),
                str(h.get('points', 0) or 0),
                h.get('title') or 'No title',
                domain,
                str(h.get('num_comments', 0) or 0),
                str(h.get('objectID', ''))
            )
        console.print(table)
    except Exception:
        rprint("[red]Search failed due to connection error[/red]")


def main():
    parser = argparse.ArgumentParser(description="Hacker News CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Feed commands
    for feed in ['top', 'new', 'best', 'ask', 'show', 'jobs']:
        p = subparsers.add_parser(feed, help=f"{feed.title()} stories")
        p.add_argument('-n', '--limit', type=int, default=10, help='Number of stories')

    # Story command
    story_p = subparsers.add_parser('story', help='Get story details')
    story_p.add_argument('id', type=int, help='Story ID')
    story_p.add_argument('--comments', type=int, default=10, help='Number of comments')

    # Search command
    search_p = subparsers.add_parser('search', help='Search stories')
    search_p.add_argument('query', nargs='+', help='Search query')
    search_p.add_argument('-n', '--limit', type=int, default=10, help='Max results')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    endpoints = {
        'top': 'topstories',
        'new': 'newstories',
        'best': 'beststories',
        'ask': 'askstories',
        'show': 'showstories',
        'jobs': 'jobstories'
    }

    if args.command in endpoints:
        stories = fetch_stories(endpoints[args.command], args.limit)
        display_stories(stories, f"HN {args.command.title()}")
    elif args.command == 'story':
        story = fetch_item(args.id)
        if story:
            display_story(story, args.comments)
        else:
            rprint("[red]Story not found[/red]")
    elif args.command == 'search':
        search_stories(' '.join(args.query), args.limit)

if __name__ == "__main__":
    main()
