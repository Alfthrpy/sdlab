---
id: incident-id                     # equals the file name and the item id in curriculum/case-studies.yaml
title: Judul insiden                # Indonesian
date: 2025-01-01                    # YYYY-MM-DD, the day of the incident
sources: [registry-id]              # registry ids; at least one of type postmortem
concepts: [concept-id]
modelability: modeled               # modeled | illustrative | text-only
sim_spec: content/incidents/incident-id.lab.yaml   # diagnose-mode lab spec; delete for text-only
sim_scenarios: [scenario-id]        # catalog scenario ids; delete for text-only
---

<!-- Written in Indonesian. Keep the five headings and their order. Specific claims carry [^registry-id] markers. -->

## Ringkasan

Apa yang terjadi, dengan kata-katamu sendiri, dalam beberapa kalimat.[^registry-id]

## Kronologi

Urutan kejadian dengan waktu.

## Mekanisme kegagalan

Kenapa kegagalannya terjadi dan menjalar.

## Skenario untuk pemain

Kondisi awal, gejala dan metrik yang terlihat, serta keputusan yang harus diambil.

## Pembahasan

Apa yang bisa dipelajari dan apa yang bisa mencegahnya.

