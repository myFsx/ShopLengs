# ShopLens SSE 事件协议 v0.1

所有事件通过 `text/event-stream` 传输，每条事件的 `data` 为 JSON 字符串。
前端按 `event` 字段分发，**只增不改**：新增事件类型向下兼容，已有字段不删不改语义。

## 事件类型

| event | 触发时机 | data 字段 | 前端行为 |
|---|---|---|---|
| `stage` | Agent 进入某阶段 | `{ "stage": "routing"\|"generating"\|"validating"\|"executing"\|"charting"\|"rewriting" }` | 更新状态条文字 |
| `token` | 模型流式输出文字 | `{ "text": "..." }` | 追加到消息气泡（打字机） |
| `sql` | 生成/重写了 SQL | `{ "sql": "SELECT ...", "version": 1 }` | 存入消息对象，Trace 面板展示，不直接渲染 |
| `chart` | 图表声明就绪 | `{ "chart_type": "bar"\|"line"\|"pie"\|"table", "x_field": "...", "y_field": "...", "title": "...", "data": [{...}] }` | 交给 `ChartBlock.vue` 渲染 |
| `trace` | 单步决策记录 | `{ "step": "...", "status": "ok"\|"error", "detail": "...", "elapsed_ms": 123 }` | 追加到 Trace 时间线 |
| `error` | 出错 | `{ "code": "sql_invalid"\|"llm_error"\|"tool_timeout", "message": "...", "recoverable": true }` | `recoverable=true` 显示“正在修复”，否则显示失败 |
| `done` | 流正常结束 | `{}` | 关闭连接，恢复输入框 |

## 示例流（一次成功问数）

```
event: stage
data: {"stage":"routing"}

event: stage
data: {"stage":"generating"}

event: sql
data: {"sql":"SELECT ...","version":1}

event: stage
data: {"stage":"validating"}

event: trace
data: {"step":"sql_guard","status":"ok","detail":"只读校验通过","elapsed_ms":12}

event: stage
data: {"stage":"executing"}

event: chart
data: {"chart_type":"bar","x_field":"name","y_field":"sales","title":"近7天销量TOP5","data":[...]}

event: token
data: {"text":"近 7 天销量最高的是..."}

event: done
data: {}
```

## 约定

- 一次请求以 `done` 或 `error(recoverable=false)` 结束，二者必居其一。
- `sql` 事件可能出现多次（重写时 `version` 递增）。
- 前端不得假设事件顺序绝对固定，但 `done` 一定在最后。
- 心跳由后端 `sse-starlette` 自动发送（15s），前端忽略注释行（`:` 开头）。
