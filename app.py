from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text

console = Console()

# Logo
logo = Text("opencode", style="bold white")
logo.stylize("grey50", 0, 4)

# Input box text
prompt = Text('Ask anything... "Fix broken tests"', style="grey70")

panel = Panel(
    prompt,
    border_style="blue",
    width=60
)

console.print("\n")
console.print(Align.center(logo))
console.print("\n")
console.print(Align.center(panel))

console.print("\n")
console.print(Align.center("[blue]Build[/blue] [white]GLM-4.7[/white] [grey50]Z.AI Coding Plan[/grey50]"))
console.print("\n")
console.print(Align.center("[yellow]• Tip[/yellow] Press [cyan]F2[/cyan] to switch models"))