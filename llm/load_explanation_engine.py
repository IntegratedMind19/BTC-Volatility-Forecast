from pathlib import Path
def load_knowledge_base(directory: str | Path) -> str:
  directory = Path(directory)
  if not directory.exists():
    raise FileNotFoundError("Knowledge base directory does not exist")
  markdown_files = sorted(directory.glob("*.md"))
  sections = list()
  for file_path in markdown_files[1:]:
    content = file_path.read_text(encoding="utf-8").strip()
    sections.append(f"# Source: {file_path.name}\n\n{content}")
  return "\n\n---\n\n".join(sections)
    
