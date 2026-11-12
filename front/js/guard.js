/* ============================================
   商城前台 · 同步路由守卫
   在 <head> 中同步加载：未登录访问受限页时，
   在页面内容解析前立即跳转登录页，避免内容闪现。
   auth.js 的 guard() 作为兜底仍然保留。

   注意（踩过的坑）：
   1. 不要调 window.stop()。它是「停止加载当前文档」，会把紧随其后的
      location.replace 一起掐掉，结果停在原地或白屏——这正是「点我的订单没反应」的原因。
   2. 先隐藏再跳转；跳转被浏览器拦下时 600ms 兜底重试一次（仍保持隐藏，
      不闪内容），两次都被拦才恢复可见，交给页面自身的 401 兜底跳登录。
      不允许出现「页面不可见且没跳走」的僵死状态。
   3. 用 visibility 而不是 display:none：后者会让部分浏览器在 bfcache 恢复时
      留下无法恢复的空白，且恢复可见时会闪一次重排。
   ============================================ */
(function (window) {
  'use strict';
  var PROTECTED = ['checkout.html', 'address.html', 'address-add.html', 'address-edit.html',
    'payment.html', 'wechat-pay.html', 'orders.html', 'after-sale.html', 'coupons.html', 'points.html'];
  var page = (window.location.pathname.split('/').pop() || 'index.html');
  if (PROTECTED.indexOf(page) < 0) return;

  var root = window.document.documentElement;

  function hasToken() {
    try { return !!window.localStorage.getItem('shop_token'); } catch (e) { return false; } /* 隐私模式 */
  }

  function hide() {
    if (root) root.style.visibility = 'hidden';
  }

  function show() {
    if (root) root.style.visibility = '';
  }

  function toLogin() {
    var back = page + window.location.search;
    window.location.replace('login.html?redirect=' + encodeURIComponent(back));
  }

  if (!hasToken()) {
    hide();
    toLogin();
    window.setTimeout(function () {
      /* 第一次兜底：跳转可能被浏览器拦下，保持隐藏再试一次，不闪内容 */
      if (hasToken()) { show(); return; }
      toLogin();
      window.setTimeout(function () {
        /* 两次都被拦：恢复可见（不再伪装成空白页），交给页面自身 401 兜底跳登录 */
        if (hasToken()) { show(); return; }
        show();
        toLogin();
      }, 600);
    }, 600);
  }

  /* bfcache 恢复时脚本不会重跑：按当前登录态修正可见性，避免后退回来见到空白页 */
  window.addEventListener('pageshow', function (event) {
    if (!event || !event.persisted) return;
    if (hasToken()) { show(); return; }
    hide();
    toLogin();
  });
})(window);
