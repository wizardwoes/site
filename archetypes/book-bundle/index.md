---
title: "{{ replace .Name "-" " " }}"
date: {{ .Date }}
draft: false
# type: "page"
type: "centered-single"
page: "{{index (split .Name "-") 1}}"
---

{{< img src="page.png" alt="page" >}}
