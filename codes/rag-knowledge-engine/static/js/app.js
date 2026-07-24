// 所有用户内容都通过 textContent 渲染，避免文档或答案注入 HTML。
const $ = (selector) => document.querySelector(selector);
async function api(path, options = {}) {
  const response = await fetch(path, options);
  if (!response.ok) { const body = await response.json().catch(() => ({})); throw new Error(body.detail || body.error?.message || `HTTP ${response.status}`); }
  return response.status === 204 ? null : response.json();
}
async function loadDocuments() {
  const items = await api('/api/v1/documents'); const list = $('#documents'); list.replaceChildren();
  for (const item of items) { const li = document.createElement('li'); li.textContent = `${item.file_name} · ${item.status} · ${item.knowledge_base_id}`; list.append(li); }
}
$('#upload-form').addEventListener('submit', async (event) => {
  event.preventDefault(); const status = $('#upload-status'); status.textContent = '正在解析、切块并构建索引…';
  try { const result = await api('/api/v1/documents', {method: 'POST', body: new FormData(event.target)}); status.textContent = `索引完成：${result.chunk_count} 个 Chunk`; await loadDocuments(); }
  catch (error) { status.textContent = `失败：${error.message}`; }
});
$('#query-form').addEventListener('submit', async (event) => {
  event.preventDefault(); const data = new FormData(event.target); const answer = $('#answer'); answer.className = 'answer empty'; answer.textContent = '正在执行关键词检索、向量检索与融合…';
  try {
    const result = await api('/api/v1/query', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({knowledge_base_id:$('#upload-form [name=knowledge_base_id]').value, question:data.get('question'), options:{include_debug:data.get('debug') === 'on'}})});
    answer.replaceChildren(); answer.className = `answer${result.refused ? ' refused' : ''}`; const text = document.createElement('p'); text.textContent = result.answer; answer.append(text);
    for (const source of result.citations) { const citation = document.createElement('div'); citation.className = 'citation'; const where = source.page_start ? `第 ${source.page_start} 页` : source.sheet_name ? `${source.sheet_name} 第 ${source.row_start} 行` : source.title; citation.textContent = `[${source.citation_id}] ${source.file_name} · ${where}\n${source.quote}`; answer.append(citation); }
    $('#debug-wrap').hidden = !result.debug; $('#debug').textContent = result.debug ? JSON.stringify(result.debug, null, 2) : '';
  } catch (error) { answer.textContent = `请求失败：${error.message}`; }
});
loadDocuments().catch(() => {});
