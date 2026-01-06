from pathlib import Path
from git import Repo
import shutil
import os

def get_repo_name_from_url(repo_url:str) -> str:
    """Extract repositories name from Github URL's"""
    return repo_url.rstrip("/").split("/")[-1].replace(".git" , "")


def ingest_repo(repo_url:str) -> Path:
    """Clone Github repository locally"""

    base_dir = Path.cwd() / "Cloned_repos"
    base_dir.mkdir(parents=True , exist_ok=True)

    repo_name = get_repo_name_from_url(repo_url)
    repo_dir = base_dir / repo_name

    if repo_dir.exists():
        shutil.rmtree(repo_dir)


    Repo.clone_from(repo_url , repo_dir)

    return repo_dir







if __name__ =="__main__":

    ingest_repo("https://github.com/Rhinks/knowthecode")