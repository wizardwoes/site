---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: true
---

{{< glas/display-bundle .Name >}}