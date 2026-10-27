# Source and Acquisition Record

Retrieved October 27, 2026.

## CASE

Casebook Preliminary IBSC 2026, transcribed in incoming handoff

- URL: Incoming handoff
- Access: Incoming Markdown read completely. Original PDF NOT supplied/inspected.
- Scope: Fictional Nexora, Indonesia; pp.7–12
- Observation: 2bn parcels; 50% internal; Rp8,000/Rp12,000; Rp5tn operating profit; see full brief.
- License: User-supplied extract; original copyright retained.

## SRC_GEOAI

opengeos. geoai-skills

- URL: https://github.com/opengeos/geoai-skills
- Access: README and overture-data instructions inspected through research service; raw endpoint403; plugin NOT executed.
- Scope: Claude Code plugin using geoai-py
- Observation: Python3.10+, geoai-py and optional extras; mapped features before object detection.
- License: MIT for repository code.

## SRC_OVERTURE

Overture Maps Foundation. Transportation Guide

- URL: https://docs.overturemaps.org/guides/transportation/
- Access: Documentation inspected; NO Overture dataset downloaded.
- Scope: Global segment/connector schema, access and direction rules
- Observation: Topology uses connectors; conditional restrictions cannot be inferred from a line crossing.
- License: Dataset-specific attribution/licensing; documentation is not a data acquisition.

## SRC_BPJT

BPJT. Dirgahayu Kota Jakarta Ke-496, ini dia beragam jalan tol yang ada di Jakarta

- URL: https://bpjt.pu.go.id/dirgahayu-kota-jakarta-ke-496-ini-dia-beragam-jalan-tol-yang-ada-di-jakarta/
- Access: Page text inspected through research service.
- Scope: Greater Jakarta toll-road concession lengths, km; NOT street geometry or traffic
- Observation: Jakarta–Tangerang33; CTC23.5; eastern inner ring27.05; W2 North7.87; JORR South14.25; Pondok Aren5.55; Becakayu15.28; Desari12.1.
- License: Government factual attributes attributed; original page not redistributed wholesale.

## SRC_KEPPRES

Republic of Indonesia. Keputusan Presiden Nomor38 Tahun1981

- URL: https://bphn.go.id/data/documents/81kp038.pdf
- Access: Research service PDF text inspected, Appendix p.3; no local PDF acquired.
- Scope: Historical Cawang–Tomang route,16km
- Observation: Historical alignment; current equivalence is an explicit assumption.
- License: Indonesian legal text; source attributed.

## SRC_BPS_DKI

BPS DKI Jakarta. Population by regency/municipality,2025

- URL: https://jakarta.bps.go.id/en/statistics-table/3/V1ZSbFRUY3lTbFpEYTNsVWNGcDZjek53YkhsNFFUMDkjMyMzMTAw/jumlah-penduduk--laju-pertumbuhan-penduduk--distribusi-persentase-penduduk--kepadatan-penduduk--rasio-jenis-kelamin-penduduk-menurut-kabupaten-kota-di-provinsi-dki-jakarta.html?year=2025
- Access: Search-index table observations only; direct page403.
- Scope: Projected resident population, persons; not customers/orders
- Observation: East3,085,058; West2,487,199; South2,219,220. Used as broad catchment proxies.
- License: BPS attribution; no boundaries/raster downloaded.

## SRC_BPS_JABAR

BPS Jawa Barat. Population projections by sex and regency/municipality

- URL: https://jabar.bps.go.id/id/statistics-table/2/OTY3IzI%3D/proyeksi-penduduk-di-provinsi-jawa-barat-menurut-jenis-kelamin-dan-kabupaten-kota.html
- Access: Search-index observations only; direct page403.
- Scope: Projected resident population, persons
- Observation: Depok2,167,961; Bekasi city approximately2,648,300. City and regency not combined.
- License: BPS attribution.

## SRC_DJP

Direktorat Jenderal Pajak. Income Tax Calculation Mechanism Entity

- URL: https://www.pajak.go.id/id/node/80250
- Access: Official page inspected.
- Scope: Indonesia corporate income tax; company-specific relief unknown
- Observation: General corporate rate22%; listed-company19% is conditional and NOT assumed.
- License: Source attributed; model tax treatment remains an assumption.

## SRC_BI

Bank Indonesia. BI-Rate tetap5,75%: memperkuat stabilitas, mendorong pertumbuhan ekonomi

- URL: https://www.bi.go.id/id/publikasi/ruang-media/news-release/Pages/sp_2823326.aspx
- Access: Official current release verified through both research engines.
- Scope: IDR policy rate and inflation target
- Observation: BI-Rate5.75%; inflation target2.5±1% for2026/2027. Policy rate is not project WACC.
- License: Official release attributed.

## SRC_ADB

Asian Development Bank. AsianBondsOnline: Indonesia Market Watch

- URL: https://asianbondsonline.adb.org/indonesia/
- Access: Primary market-data portal verified through both research engines.
- Scope: Indonesia nominal government bond yields
- Observation: 5yr7.245%;10yr7.446%. Risk-premium spread to project discount rate is authored.
- License: Factual snapshot with attribution; no proprietary feed redistributed.

## SRC_JT

J&T Express. Reports18.5% YoY revenue growth forFY2025

- URL: https://www.jtexpress.sg/insights/press-jt-express-reports-18.5-yoy-growth?hs_amp=true
- Access: Operator page inspected.
- Scope: SEA multi-country network; own accounting and franchise scope
- Observation: SEA parcel volume7.66bn, growth67.8%; cost/parcelUS$0.48. Plausibility evidence only; no Nexora coefficient imported.
- License: Operator release attributed.

## SRC_ARCGIS

DKI Jakarta. Peta Jalan DKI FeatureServer

- URL: https://gis-dpmptsp.jakarta.go.id/arcgis/rest/services/Hosted/Peta_Jalan_DKI/FeatureServer/1
- Access: Metadata found in search; feature query inaccessible; cloud browser environment denied URL. NO features downloaded.
- Scope: DKI road linework metadata; outside-city coverage not established
- Observation: Potential official GIS source; catalogued only.
- License: Redistribution terms not verified; no source data redistributed.

## SRC_OSM

OpenStreetMap contributors. Overpass/API endpoints

- URL: https://overpass-api.de/api/interpreter
- Access: Direct API403; research-service API queries inaccessible. NO road extract acquired.
- Scope: Requested Greater Jakarta bounding box and buffer
- Observation: Optional retrieval/preparation script supplied; not used for headline routing.
- License: ODbL1.0 if subsequently downloaded. https://www.openstreetmap.org/copyright