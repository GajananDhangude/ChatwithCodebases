from pathlib import Path
import os



IGNORE_DIRS = {".git" , "node_modules" , "dist" , "build" , "__pycache__"}
SUPPORTED_EXTENSIONS =  ('.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h', '.go', '.rs', '.php',
        '.html', '.css', '.scss', '.json', '.yaml', '.yml', '.xml', '.md', '.Rmd', '.ipynb')


def load_repository(repo_path:str):
    documents =[]

    repo_path = os.path.abspath(repo_path)

    for root , dirs , files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            if file.endswith(SUPPORTED_EXTENSIONS):
                file_path = os.path.join(root , file)

                try:
                    with open(file_path , "r" , encoding="utf-8" , errors="ignore") as f:
                        content = f.read()

                        blocks = parse_code(content , file_path)

                        if blocks:
                            for b in blocks:
                                documents.append({
                                    "path": file_path,
                                    "symbol": b["symbol"],
                                    "type": b["type"],
                                    "start_line": b["start_line"],
                                    "end_line": b["end_line"],
                                    "content": b["code"]
                                })

                        else:
                            #fallback: whole file (important)
                            documents.append({
                            "path": file_path,
                            "symbol": "file",
                            "type": "file",
                            "start_line": 1,
                            "end_line": len(content.splitlines()),
                            "content": content
                        })
                            
                except Exception as e:
                    print(f"Failed to load{file_path} : {e}")

    return documents