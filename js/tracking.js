/* hyroxtrainingclub.cz – Google Analytics 4 s cookie lištou (Consent Mode v2)
   Načítá se v <head> každé stránky: <script src="/js/tracking.js"></script>
   Bez souhlasu jde do Googlu jen anonymní signál bez cookies. */
(function () {
  var GA4 = 'G-3LCL2EPWD5';
  var KEY = 'str2g_consent';

  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  window.gtag = window.gtag || gtag;
  gtag('consent', 'default', {
    ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied',
    analytics_storage: 'denied', wait_for_update: 500
  });
  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA4;
  document.head.appendChild(s);
  gtag('js', new Date());
  gtag('config', GA4);

  function getConsent() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function setConsent(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  function grant() {
    gtag('consent', 'update', {
      ad_storage: 'granted', ad_user_data: 'granted', ad_personalization: 'granted',
      analytics_storage: 'granted'
    });
  }
  if (getConsent() === 'all') grant();

  // --- Události (kliky na hlavní akce webu) ---
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a) return;
    var h = a.getAttribute('href') || '';
    if (/formfactory\.cz\/calendar|#timetables/.test(h)) {
      var club = (h.match(/\/\/([a-z0-9-]+)\.formfactory\.cz/) || [])[1] || 'all';
      gtag('event', 'book_class_click', { club: club });
      gtag('event', 'generate_lead', { method: 'booking', club: club });
    } else if (/prvni-vstup/.test(h)) gtag('event', 'first_visit_click');
    // Prodej na FF Academy: workshopy (data-ga na odkazu) a 12 Weeks Race Prep
    var ga = a.getAttribute('data-ga');
    var lang = (document.documentElement.lang || 'cs').slice(0, 2);
    var where = (a.closest('section[id],.rp-bar,.rp-promo,header') || {});
    var placement = where.id || (where.className || '').toString().split(' ')[0] || 'other';
    if (ga === 'workshop_buy') {
      gtag('event', 'workshop_buy_click', { workshop: a.getAttribute('data-item'), workshop_name: a.getAttribute('data-name'),
        value: Number(a.getAttribute('data-price')) || 0, currency: 'CZK', page_lang: lang });
    } else if (ga === 'workshop_info') {
      gtag('event', 'workshop_info_click', { workshop: a.getAttribute('data-item'), workshop_name: a.getAttribute('data-name'), page_lang: lang });
    } else if (/ff-academy\.cz/.test(h)) {
      gtag('event', 'race_prep_buy_click', { value: 8999, currency: 'CZK', placement: placement, page_lang: lang });
    }
    if (/^tel:/.test(h)) gtag('event', 'contact', { method: 'phone' });
    else if (/^mailto:/.test(h)) gtag('event', 'contact', { method: 'email' });
  }, true);

  // --- Cookie lišta (CZ / EN / PL / DE podle <html lang>) ---
  var TXT = {
    cs: ['Používáme cookies pro měření návštěvnosti.', 'Povolit vše', 'Jen nezbytné'],
    en: ['We use cookies to measure site traffic.', 'Accept all', 'Essential only'],
    pl: ['Używamy plików cookie do pomiaru ruchu.', 'Akceptuj wszystkie', 'Tylko niezbędne'],
    de: ['Wir nutzen Cookies zur Reichweitenmessung.', 'Alle akzeptieren', 'Nur notwendige']
  };
  function banner() {
    if (document.getElementById('str2g-cookie')) return;
    var t = TXT[(document.documentElement.lang || 'cs').slice(0, 2)] || TXT.en;
    var d = document.createElement('div');
    d.id = 'str2g-cookie';
    d.setAttribute('role', 'dialog');
    d.setAttribute('aria-label', 'Cookies');
    d.style.cssText = 'position:fixed;left:16px;right:16px;bottom:16px;z-index:9999;max-width:560px;margin:0 auto;background:#111;color:#fff;border:1px solid #333;border-radius:10px;padding:16px;font:14px/1.4 system-ui,sans-serif;display:flex;flex-wrap:wrap;gap:10px;align-items:center';
    d.innerHTML = '<span style="flex:1 1 220px">' + t[0] + '</span>' +
      '<button type="button" data-c="necessary" style="background:none;color:#fff;border:1px solid #555;border-radius:6px;padding:8px 12px;cursor:pointer;font:inherit">' + t[2] + '</button>' +
      '<button type="button" data-c="all" style="background:#fff;color:#000;border:0;border-radius:6px;padding:8px 12px;cursor:pointer;font:inherit;font-weight:600">' + t[1] + '</button>';
    d.addEventListener('click', function (e) {
      var c = e.target.getAttribute('data-c'); if (!c) return;
      setConsent(c);
      if (c === 'all') grant();
      else gtag('consent', 'update', {
        ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied',
        analytics_storage: 'denied'
      });
      d.remove();
    });
    document.body.appendChild(d);
  }
  window.cookieSettings = banner; // odkaz „Cookies“ v patičce
  if (!getConsent()) {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', banner);
    else banner();
  }
})();
