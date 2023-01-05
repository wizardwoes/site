---
title: "{{ replace .Name "-" " " }}"
date: {{ .Date }}
draft: false
type: "page"
page: "{{index (split .Name "-") 1}}"
---


