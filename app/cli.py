import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.style import Style
from typing import List
from .searcher import VectorSearcher
from .indexer import AirbnbIndexer
from .models import SearchResult
import sys

app = typer.Typer()
console = Console()
error_console = Console(stderr=True, style="bold red")


def display_results(results: List[SearchResult]):
    """検索結果を整形して表示"""
    if not results:
        console.print("[yellow]検索結果が見つかりませんでした。[/yellow]")
        return

    for idx, result in enumerate(results, 1):
        console.print(
            Panel(
                f"""
[bold blue]#{idx} {result.name}[/bold blue]
[bold]ID:[/bold] {result._id}
[bold]Space:[/bold] {result.space}
[bold]Price:[/bold] ${result.price:,.2f}
[bold]Similarity Score:[/bold] {result.similarity_score:.4f}

[bold]Amenities:[/bold]{result.format_amenities()}
""",
                expand=False,
            )
        )
        console.print("---")


@app.command()
def create_index():
    """インデックスを作成"""
    try:
        with console.status("[bold green]インデックスを作成中...[/bold green]"):
            indexer = AirbnbIndexer()
            indexer.create_index("data/index")
        console.print("[bold green]インデックスの作成が完了しました！[/bold green]")
    except Exception as e:
        error_console.print(f"インデックスの作成に失敗しました: {str(e)}")
        sys.exit(1)


@app.command()
def search():
    """インタラクティブな検索インターフェース"""
    try:
        searcher = VectorSearcher("data/index")
    except Exception as e:
        error_console.print(f"インデックスの読み込みに失敗しました: {str(e)}")
        sys.exit(1)

    # 検索ワード入力
    query = typer.prompt("検索ワードを入力してください")

    # 価格範囲
    min_price = typer.prompt("最小価格を入力してください", type=int, default=0)
    max_price = typer.prompt("最大価格を入力してください", type=int, default=99999)

    # WiFiフィルター
    wifi_required = typer.confirm("WiFiは必須ですか？")

    try:
        with console.status("[bold green]検索中...[/bold green]"):
            results = searcher.search(
                query=query,
                min_price=min_price,
                max_price=max_price,
                wifi_required=wifi_required,
                limit=5,
            )

        # 結果表示
        display_results(results)
    except Exception as e:
        error_console.print(f"検索中にエラーが発生しました: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    app()
