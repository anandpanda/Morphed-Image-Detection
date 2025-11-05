import os, random, shutil
from pathlib import Path

# ---------- CONFIG ----------
SRC_ROOT = Path('Dataset') # your original root
DST_ROOT =  Path('Dataset_reduced') # new reduced copy
random.seed(42)

# Option A targets (per class)
TARGETS = {
    'train':   {'real': 5000, 'fake': 5000},
    'validation': {'real': 2000, 'fake': 2000},
    'test':    {'real': 2000, 'fake': 2000},
}

# If your class folder name is 'fake' not 'morphed', change the keys appropriately.

# ---------- FUNCTION ----------
def reduce_and_copy(src_root: Path, dst_root: Path, targets: dict, classes=('real','fake')):
    dst_root.mkdir(parents=True, exist_ok=True)
    summary = {}
    for split, counts in targets.items():
        summary[split] = {}
        for cls in classes:
            src_dir = src_root / split / cls
            dst_dir = dst_root / split / cls
            dst_dir.mkdir(parents=True, exist_ok=True)

            if not src_dir.exists():
                print(f"Warning: {src_dir} does not exist. Skipping.")
                summary[split][cls] = 0
                continue

            files = [p for p in src_dir.iterdir() if p.suffix.lower() in ('.jpg','.jpeg','.png')]
            n_available = len(files)
            n_pick = min(counts.get(cls, 0), n_available)

            # Shuffle and sample
            random.shuffle(files)
            picked = files[:n_pick]

            # Copy
            for p in picked:
                shutil.copy2(p, dst_dir / p.name)

            summary[split][cls] = n_pick
            print(f"Copied {n_pick}/{n_available} for {split}/{cls} -> {dst_dir}")

    print("\nDone. Summary:")
    for split, d in summary.items():
        print(split, d)

# ---------- RUN ----------
reduce_and_copy(SRC_ROOT, DST_ROOT, TARGETS)
