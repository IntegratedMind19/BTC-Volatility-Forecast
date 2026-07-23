from pathlib import Path

def load_prompt_template(file_path: str | Path) -> str:
  file_path = Path(file_path)
  if not file_path.exists():
    raise FileNotFoundError("Path does not exist")
  return file_path.read_text().strip()
  
