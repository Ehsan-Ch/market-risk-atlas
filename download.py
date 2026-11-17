"""Download only the fixed study's source archives, with checksum verification."""
import json
from ingest import acquire,ROOT
if __name__=='__main__':acquire(json.loads((ROOT/'config.json').read_text()))
