```markdown
[Records từ database searching (N = 642)]
↓
[Sau khi xóa duplicate (N = 641)]
↓
┌───────────────────────────────────────────────┐
│ Screened title + abstract (N = 641)           │
│ └── Excluded (N = 612): EC4=610, IC2=2          │
└───────────────────────────────────────────────┘
↓ 29 papers pass
┌───────────────────────────────────────────────┐
│ Full-text assessed (N = 29)                   │
│ └── Excluded (N = 22): EC4=21, Unaccessible/Unsure=1 │
└───────────────────────────────────────────────┘
↓
[Final included (N = 7)]
```

**Kiểm tra nhất quán (tự check trước khi nộp):**
- Rows trong `01_all_records.csv` (641) = N sau dedup (641) ✓
- Count(`v1_decision = EXCLUDE`) trong 02 (612) = Excluded vòng 1 (612) ✓
- Count(`v1_decision = INCLUDE` + `Unsure`) trong 02 (29) = Full-text assessed (29) ✓
- Count(`v2_decision = INCLUDE`) trong 03 (7) = Final included (7) ✓
