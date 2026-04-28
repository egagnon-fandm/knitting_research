## Table of content

```dataview
table date, description from "Daily"
sort file.date ASC
```

## Meetings TOC

```dataview
table date, description from "Daily"
where contains(file.tags,"#meeting")
sort file.date ASC
```
## Data

```dataview
table date, description from "Daily"
where contains(file.tags, "#data")
sort file.date ASC
```

## Analysis

```dataview
table date, description from "Daily"
where contains(file.tags, "analysis")
sort file.date ASC
```

## Theory

```dataview
table date, description from "Daily"
where contains(file.tags, "theory")
sort file.date ASC
```
