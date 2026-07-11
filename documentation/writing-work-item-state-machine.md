# Writing Work-Item State Machine

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

Valid states are `intake`, `research`, `planned`, `drafted`, `fact-checked`, `style-reviewed`, `editor-review`, `approved`, `published`, and `archived`. Transitions are forward-only except an editor may return a work item to `research`, `planned`, or `drafted` with a reason recorded.