/* ============================================
   商城后台 · 同步登录守卫
   在 <head> 中同步加载：未登录时在页面解析前
   立即跳转登录页，避免后台骨架内容闪现。
   common.js 的 initPage() 守卫作为兜底仍然保留。
   ============================================ */
(function (window) {
  'use strict';
  var page = (window.location.pathname.split('/').pop() || 'index.html');
  if (page === 'login.html') return;
  var raw = '';
  try { raw = window.localStorage.getItem('mall_admin_session') || ''; } catch (e) { /* 隐私模式 */ }
  var ok = false;
  try {
    var s = JSON.parse(raw);
    ok = !!(s && s.token);
  } catch (e) { ok = false; }
  if (!ok) {
    // pages/ 二级目录页面需要回退两级才能到 manager 根
    var root = /\/pages\//i.test(window.location.pathname) ? '../../' : '';
    window.location.replace(root + 'login.html');
    try { window.stop(); } catch (e) { /* 旧浏览器忽略 */ }
    if (window.document.documentElement) window.document.documentElement.style.display = 'none';
  }
})(window);
