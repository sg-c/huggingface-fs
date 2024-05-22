import os
from huggingface_hub import snapshot_download
from http_client import alive_peers, search_model


class ModelManager:
    MODEL_ROOT_PATH = "/tmp"

    def add_model(self, repo_id, branch=None, revision=None):
        self._download_model(repo_id)

    def _model_exists(self, repo_id, branch, revision):
        return os.path.exists(f"{self.MODEL_ROOT_PATH}/{repo_id}/{branch}/{revision}")

    def _download_model(self, repo_id, branch="main", revision=None):
        rev = revision if revision else "abc"
        dir = f"{self.MODEL_ROOT_PATH}/hffs/{branch}/{rev}"
        snapshot_download(repo_id=repo_id, local_dir=dir,
                          allow_patterns=["*.txt", "*.json"])

    async def search_model(self, repo_id, revision=None, file_name=None):
        active_peers = await alive_peers()
        avail_peers = []
        if len(active_peers) > 0:
            avail_peers = await search_model(active_peers, repo_id, revision, file_name)
        return (active_peers, avail_peers)
