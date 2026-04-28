---
date: <% tp.date.now() %>
tags:
  - "#meeting"
attendees: 
description:
---
<%*
const folderName = "Daily/" + tp.date.now().toString() + "/";
if (!tp.file.exists(folderName)){
	await this.app.vault.createFolder(folderName);
}
await tp.file.move(folderName + tp.file.title);
%>
## Agenda

## Notes

## TODO

