# Report: Performance Anti-Pattern Audit

**Datum:** 2026-01-18
**Fokus:** Performance-Analyse, N+1, Re-renders

---

## Ziel

Identifikation von Performance-Anti-Patterns, N+1-Queries, unnötigen Re-renders und ineffizienten Algorithmen im Codebase.

---

## Kritische Findings

### 1. HIGH SEVERITY: Colormap Regeneration (colormaps.ts)

**File:** `ui-app/lib/colormaps.ts:294-313`

```typescript
export function getColormap(name: ColormapName, size: number = 256): ColorPalette {
  switch (name) {
    case 'resonant':
      return generateResonantPalette(size); // Creates 256 RGB objects EVERY call
    // ... 6 more cases
  }
}
```

**Problem:** Every call generates a fresh palette with 256 RGB objects. At 60 FPS with FractalCanvas, this creates ~15,360 objects/second.

**Impact:** High memory churn, GC pressure, potential jank

**Fix:** Add module-level cache:
```typescript
const COLORMAP_CACHE = new Map<string, ColorPalette>();

export function getColormap(name: ColormapName, size: number = 256): ColorPalette {
  const key = `${name}:${size}`;
  if (!COLORMAP_CACHE.has(key)) {
    COLORMAP_CACHE.set(key, generatePalette(name, size));
  }
  return COLORMAP_CACHE.get(key)!;
}
```

---

### 2. HIGH SEVERITY: Fractal Calculation Blocking Main Thread (FractalCanvas.tsx)

**File:** `ui-app/components/fractalsense/FractalCanvas.tsx`

**Problem:** Synchronous nested loops for fractal calculation block the main thread:
```typescript
for (let py = 0; py < height; py++) {
  for (let px = 0; px < width; px++) {
    const iter = calculateIteration(px, py, width, height);
    // ... O(width × height) operations
  }
}
```

**Impact:** For 800×600 canvas = 480,000 calculations per frame, blocking UI

**Fix:** Move calculation to Web Worker or use OffscreenCanvas

---

### 3. MEDIUM SEVERITY: Multiple Filter Passes (N+1 Pattern)

#### GuardGrid.tsx:27-29
```typescript
const okCount = guards.filter(g => g.status === 'ok').length;      // Pass 1
const warningCount = guards.filter(g => g.status === 'warning').length; // Pass 2
const errorCount = guards.filter(g => g.status === 'error').length;   // Pass 3
```

**Impact:** O(3n) instead of O(n)

**Fix:** Single pass with reduce:
```typescript
const counts = guards.reduce((acc, g) => {
  acc[g.status] = (acc[g.status] || 0) + 1;
  return acc;
}, {} as Record<string, number>);
```

#### voidmap-parser.ts:206-216
```typescript
return {
  total: voids.length,
  open: voids.filter(v => v.status === 'OPEN').length,           // Pass 1
  inProgress: voids.filter(v => v.status === 'IN_PROGRESS').length, // Pass 2
  closed: voids.filter(v => v.status === 'CLOSED').length,        // Pass 3
  critical: voids.filter(v => v.priority === 'critical' && v.status !== 'CLOSED').length, // Pass 4
  high: voids.filter(v => v.priority === 'high' && v.status !== 'CLOSED').length, // Pass 5
};
```

**Impact:** O(5n) instead of O(n)

---

### 4. MEDIUM SEVERITY: File I/O Inefficiency (ledger.py)

**File:** `src/core/ledger.py:116-133`

```python
def _load_last_hash(self) -> None:
    last_line = None
    with open(self.path, encoding="utf-8") as f:
        for line in f:  # Reads ENTIRE file sequentially
            line = line.strip()
            if line:
                last_line = line  # Just to get the last line
```

**Problem:** Reads entire file from start to end just to get the last line.

**Impact:** O(n) where n = file size. For large ledgers, this becomes slow.

**Fix:** Read backwards from end of file:
```python
import os

def _load_last_hash(self) -> None:
    if not self.path or not self.path.exists():
        return
    with open(self.path, 'rb') as f:
        f.seek(0, os.SEEK_END)
        pos = f.tell()
        # Read backwards to find last complete line
        # ... (implementation)
```

---

### 5. LOW SEVERITY: Regex Recompilation (Python tools)

#### verify_pointers.py:55-60
```python
def is_optional_context(text: str) -> bool:
    for pattern in OPTIONAL_MARKERS:  # 4 patterns
        if re.search(pattern, text, re.IGNORECASE):  # Recompiles each call
            return True
    return False
```

**Fix:** Compile patterns once at module level:
```python
OPTIONAL_PATTERNS = [re.compile(p, re.IGNORECASE) for p in OPTIONAL_MARKERS]
```

#### claim_lint.py:109-110
Same pattern with 18 patterns per line.

---

### 6. LOW SEVERITY: Eager Colormap Initialization (color_generator.py)

**File:** `Fractalsense/color_generator.py`

```python
def __init__(self):
    self.custom_colormaps = {}
    self.create_default_colormaps()  # Generates ALL 5 colormaps immediately
```

**Problem:** Generates all colormaps at startup even if unused.

**Impact:** 5 × 256 × ~50 calculations = 64,000+ operations at init

**Fix:** Lazy generation on first access

---

## Memory Leak Check

| File | Pattern | Status |
|------|---------|--------|
| FractalCanvas.tsx | window.addEventListener cleanup | OK |
| GuardGrid.tsx | setInterval cleanup | OK |
| AttentionStream.tsx | setInterval cleanup | OK |

No critical memory leaks detected.

---

## Summary Table

| Issue | File | Severity | Complexity | Effort |
|-------|------|----------|------------|--------|
| Palette regeneration | colormaps.ts | HIGH | O(256)/call | Low |
| Fractal blocking | FractalCanvas.tsx | HIGH | O(WxH)/frame | Medium |
| Multiple filters | GuardGrid.tsx | MEDIUM | O(3n)→O(n) | Low |
| Multiple filters | voidmap-parser.ts | MEDIUM | O(5n)→O(n) | Low |
| File read all | ledger.py | MEDIUM | O(n)→O(1) | Medium |
| Regex recompile | verify_pointers.py | LOW | Startup | Low |
| Eager init | color_generator.py | LOW | Startup | Low |

---

## Recommended Priority

1. **Immediate:** Cache colormap results (biggest impact, lowest effort)
2. **Short-term:** Replace multiple filters with single-pass reduce
3. **Medium-term:** Move fractal calculations to Web Worker
4. **Low-priority:** Python tool optimizations (only affects CLI startup)

---

## Nicht getan

- Did not modify any code (read-only analysis)
- Did not check external dependencies for performance
- Did not profile actual runtime metrics

---

## Risiken

- Colormap caching could cause memory growth if many different sizes requested
- Web Worker implementation requires message serialization overhead
- Ledger file reverse-read needs careful newline handling

---

## Offene Punkte

- [ ] Implement colormap caching
- [ ] Profile actual FractalCanvas render times
- [ ] Consider React.memo for GuardStatusCard components
- [ ] Evaluate if 10s polling interval in GuardGrid is necessary

---

## Artefakte

- `ui-app/lib/colormaps.ts` - Needs caching
- `ui-app/components/guards/GuardGrid.tsx` - N+1 filter pattern
- `ui-app/lib/voidmap-parser.ts` - N+1 filter pattern
- `src/core/ledger.py` - File read inefficiency
- `tools/verify_pointers.py` - Regex recompilation
- `Fractalsense/color_generator.py` - Eager initialization
