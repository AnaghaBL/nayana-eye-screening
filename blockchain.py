import hashlib
import json
import os
from datetime import datetime

CHAIN_FILE = "audit_chain.json"

def load_chain():
    if not os.path.exists(CHAIN_FILE):
        return []
    with open(CHAIN_FILE, 'r') as f:
        return json.load(f)

def save_chain(chain):
    with open(CHAIN_FILE, 'w') as f:
        json.dump(chain, f, indent=2)

def get_last_hash():
    chain = load_chain()
    if not chain:
        return "0" * 64
    return chain[-1]['hash']

def add_block(action, case_id, actor, details=""):
    chain = load_chain()
    block = {
        "index":     len(chain),
        "timestamp": datetime.now().isoformat(),
        "action":    action,
        "case_id":   case_id,
        "actor":     actor,
        "details":   details,
        "prev_hash": get_last_hash()
    }
    block_str = json.dumps(block, sort_keys=True)
    block['hash'] = hashlib.sha256(block_str.encode()).hexdigest()
    chain.append(block)
    save_chain(chain)

def verify_chain():
    chain = load_chain()
    for i, block in enumerate(chain):
        stored_hash = block.pop('hash')
        computed    = hashlib.sha256(
            json.dumps(block, sort_keys=True).encode()
        ).hexdigest()
        block['hash'] = stored_hash
        if stored_hash != computed:
            return False, f"Tampered at block {i}"
        if i > 0 and block['prev_hash'] != chain[i-1]['hash']:
            return False, f"Chain broken at block {i}"
    return True, "Chain intact"