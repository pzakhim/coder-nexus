/* coder-nexus UX kit runtime. Works from file:// (no server, no network).
 * Screen pages:  states ([data-state]), notes (.note), mock binding ([data-mock] <- window.MOCK),
 *                step links ([data-next] / href to another screen), walkthrough targets
 *                ([data-ux-target]) driven by ux:tap / ux:type / ux:highlight messages.
 * Index page:    UX.index() renders workflows (window.UX_FLOWS) in a device frame sized by
 *                window.UX_VIEWPORTS (kit/viewports.js: platforms with width/height and allowed orientations),
 *                and plays each workflow's walkthrough (uiux.md "## 8. Walkthrough"):
 *                UX.play / UX.pause / UX.stepOnce / UX.setSpeed / UX.stop / UX.setOrientation.
 *                ?platform=tablet&orientation=landscape picks the frame (kept in the URL when changed);
 *                index.html?play=W-01&platform=mobile&orientation=portrait&speed=1&chrome=off autoplays (`ux record`).
 *                The index shell is generated (`coder-nexus ux new`); never edit index.html or this file.
 *                A walkthrough is a scripted MOCK simulation; it does not run app logic.
 * Page <-> frame talk via postMessage only (file:// pages have opaque origins). */
(function () {
  "use strict";
  var UX = (window.UX = window.UX || {});
  var params = new URLSearchParams(location.search);
  var inFrame = window.parent !== window;
  var root = document.documentElement;

  function uniq(list) { return list.filter(function (v, i) { return list.indexOf(v) === i; }); }
  function get(obj, path) {
    return path.split(".").reduce(function (o, k) {
      if (o == null) return undefined;
      var m = k.match(/^(\w+)\[(\d+)\]$/);
      return m ? (o[m[1]] || [])[+m[2]] : o[k];
    }, obj);
  }
  function post(msg) { if (inFrame) window.parent.postMessage(msg, "*"); }

  // ------------------------------------------------------------------ screen page
  function screenEl() { return document.querySelector("[data-screen]"); }
  function stateEls() { var s = screenEl(); return s ? s.querySelectorAll("[data-state]") : []; }
  function states() {
    return uniq([].map.call(stateEls(), function (e) { return e.getAttribute("data-state"); }));
  }
  function setState(name) {
    var all = states();
    if (!all.length) return;
    if (all.indexOf(name) < 0) name = all.indexOf("default") >= 0 ? "default" : all[0];
    [].forEach.call(stateEls(), function (el) { el.hidden = el.getAttribute("data-state") !== name; });
    root.setAttribute("data-state", name);
    if (cursor) cursor.hidden = true;
    refreshToolbar();
    post({ type: "ux:state", state: name });
  }
  function setNotes(on) { root.setAttribute("data-notes", on ? "on" : "off"); refreshToolbar(); }
  function bindMock() {
    if (!window.MOCK) return;
    document.querySelectorAll("[data-mock]").forEach(function (el) {
      var v = get(window.MOCK, el.getAttribute("data-mock"));
      if (v === undefined || v === null) { el.classList.add("mock-missing"); el.title = "MOCK missing: " + el.getAttribute("data-mock"); return; }
      if (el.tagName === "INPUT" || el.tagName === "TEXTAREA" || el.tagName === "SELECT") el.value = v; else el.textContent = v;
    });
  }
  function bindNavigation() {
    document.addEventListener("click", function (ev) {
      var a = ev.target.closest && ev.target.closest("a[href]");
      if (!a) return;
      var href = a.getAttribute("href");
      if (!href || href.charAt(0) === "#" || /^[a-z]+:/i.test(href) || !/\.html(\?|$)/.test(href)) return;
      ev.preventDefault();
      if (inFrame) { post({ type: "ux:navigate", href: href }); return; }
      var q = new URLSearchParams();
      q.set("notes", root.getAttribute("data-notes") || "on");
      location.href = href.split("?")[0] + "?" + q.toString();
    });
  }
  var toolbar;
  function refreshToolbar() {
    if (!toolbar) return;
    var cur = root.getAttribute("data-state"), notes = root.getAttribute("data-notes") !== "off";
    toolbar.querySelectorAll("button").forEach(function (b) {
      if (b.dataset.uxState) b.classList.toggle("on", b.dataset.uxState === cur);
      if (b.dataset.uxNotes) b.classList.toggle("on", notes);
    });
  }
  function buildToolbar() {
    if (inFrame || !screenEl()) return;
    toolbar = document.createElement("div");
    toolbar.className = "ux-toolbar";
    states().forEach(function (s) {
      var b = document.createElement("button"); b.textContent = s; b.dataset.uxState = s;
      b.onclick = function () { setState(s); }; toolbar.appendChild(b);
    });
    var n = document.createElement("button"); n.textContent = "notes"; n.dataset.uxNotes = "1";
    n.onclick = function () { setNotes(root.getAttribute("data-notes") === "off"); }; toolbar.appendChild(n);
    document.body.appendChild(toolbar);
  }
  // walkthrough targets: a data-ux-target name (visible state first), a CSS selector as fallback
  function visible(el) { return !el.closest("[data-state][hidden]"); }
  function findTarget(name) {
    if (!name) return null;
    var list = [].slice.call(document.querySelectorAll('[data-ux-target="' + name.replace(/"/g, "") + '"]'));
    if (!list.length) { try { list = [].slice.call(document.querySelectorAll(name)); } catch (e) { list = []; } }
    return list.filter(visible)[0] || null;
  }
  var cursor;
  function moveCursor(el, ms, done) {
    if (!cursor) { cursor = document.createElement("div"); cursor.className = "ux-cursor"; document.body.appendChild(cursor); }
    if (!el) { done(); return; }
    el.scrollIntoView({ block: "nearest" });
    var r = el.getBoundingClientRect();
    cursor.style.transitionDuration = ms + "ms";
    cursor.style.left = r.left + r.width / 2 + "px"; cursor.style.top = r.top + r.height / 2 + "px";
    cursor.hidden = false;
    setTimeout(done, ms);
  }
  function ripple(el) {
    if (!el) return;
    var r = el.getBoundingClientRect(), d = document.createElement("div");
    d.className = "ux-ripple"; d.style.left = r.left + r.width / 2 + "px"; d.style.top = r.top + r.height / 2 + "px";
    document.body.appendChild(d); setTimeout(function () { d.remove(); }, 600);
  }
  function highlight(el, on, kind) {
    if (!el) return;
    el.classList.toggle("ux-hl", !!on);
    el.classList.toggle("ux-scan", !!on && kind === "scan");
  }
  function typeInto(el, text, perChar, done) {
    var field = el && (/^(INPUT|TEXTAREA)$/.test(el.tagName) ? el : el.querySelector("input, textarea")) || el;
    if (!field) { done(); return; }
    var isInput = /^(INPUT|TEXTAREA)$/.test(field.tagName), i = 0;
    if (isInput) { field.value = ""; field.focus({ preventScroll: true }); } else field.textContent = "";
    (function next() {
      if (i >= text.length) { done(); return; }
      i += 1;
      if (isInput) field.value = text.slice(0, i); else field.textContent = text.slice(0, i);
      setTimeout(next, perChar);
    })();
  }
  function onPlayer(d) {
    var speed = d.speed || 1, el = findTarget(d.target);
    function done() { post({ type: "ux:done", id: d.id, found: !!el }); }
    if (d.type === "ux:highlight") { highlight(el, d.on !== false, d.kind); done(); return; }
    if (d.type === "ux:tap") {
      moveCursor(el, 450 / speed, function () { ripple(el); highlight(el, true); setTimeout(function () { highlight(el, false); done(); }, 250 / speed); });
      return;
    }
    if (d.type === "ux:type") {
      var value = String(d.value == null ? "" : d.value);
      if (value.charAt(0) === "@" && window.MOCK) { var m = get(window.MOCK, value.slice(1)); if (m != null) value = String(m); }
      if (d.scan) {  // a scanner types the whole code at once into the focused field
        highlight(el, true, "scan");
        setTimeout(function () { typeInto(el, value, 0, function () { setTimeout(function () { highlight(el, false); done(); }, 300 / speed); }); }, 350 / speed);
        return;
      }
      moveCursor(el, 400 / speed, function () { ripple(el); highlight(el, true); typeInto(el, value, 90 / speed, function () { highlight(el, false); done(); }); });
    }
  }

  function initScreen() {
    var el = screenEl();
    if (!el) return;
    bindMock();
    bindNavigation();
    buildToolbar();
    setNotes(params.get("notes") !== "off");
    setState(params.get("state") || "default");
    window.addEventListener("message", function (ev) {
      var d = ev.data || {};
      if (d.type === "ux:setState") setState(d.state);
      if (d.type === "ux:setNotes") setNotes(!!d.on);
      if (d.type === "ux:tap" || d.type === "ux:type" || d.type === "ux:highlight") onPlayer(d);
    });
    post({ type: "ux:ready", screen: el.getAttribute("data-screen"), states: states(), title: document.title });
  }

  // ------------------------------------------------------------------ index page
  UX.index = function (mount) {
    var cfg = window.UX_FLOWS || { title: "UI/UX design", flows: [], screens: [] };
    var vp = window.UX_VIEWPORTS || { platforms: { mobile: { width: 390, height: 844 } }, confirmed: false };
    var platforms = Object.keys(vp.platforms || {});
    var cur = { platform: platforms[0], orientation: null, file: null, flow: null, step: -1, state: "default", notes: true, states: [] };
    if (platforms.indexOf(params.get("platform")) >= 0) cur.platform = params.get("platform");
    function orientations(p) {
      var v = vp.platforms[p] || {};
      if ((v.orientations || []).length) return v.orientations;
      return [v.orientation || (v.width > v.height ? "landscape" : "portrait")];  // schema-1 viewports.js
    }
    function dims(p, o) {
      var v = vp.platforms[p] || { width: 390, height: 844 }, native = v.width > v.height ? "landscape" : "portrait";
      return o === native || v.width === v.height ? [v.width, v.height] : [v.height, v.width];
    }
    function pickOrientation(o) { var all = orientations(cur.platform); cur.orientation = all.indexOf(o) >= 0 ? o : all[0]; }
    pickOrientation(params.get("orientation"));
    function syncUrl() {
      try {
        var q = new URLSearchParams(location.search);
        q.set("platform", cur.platform); q.set("orientation", cur.orientation);
        history.replaceState(null, "", location.pathname + "?" + q.toString() + location.hash);
      } catch (e) { /* some browsers refuse replaceState on file:// */ }
    }
    var expanded = {}, filter = "";
    var SPEEDS = [1, 1.5, 2];
    var player = { flow: null, i: 0, playing: false, busy: false, token: 0, speed: Math.min(2, Math.max(1, +params.get("speed") || 1)) };
    var el = typeof mount === "string" ? document.querySelector(mount) : mount || document.body;

    el.innerHTML =
      '<div class="ux-index"><aside class="ux-side"></aside><section class="ux-main">' +
      (vp.confirmed ? "" : '<div class="ux-warn">Viewport sizes are not confirmed for this project yet (run: coder-nexus ux viewports).</div>') +
      '<div class="ux-bar"></div><div class="ux-stage"><div class="ux-device"><iframe title="screen"></iframe></div>' +
      '<div class="ux-mocklabel" hidden>Mô phỏng — MOCK</div><div class="ux-countdown" hidden></div><div class="ux-caption" hidden></div>' +
      "</div></section></div>";
    var side = el.querySelector(".ux-side"), bar = el.querySelector(".ux-bar"),
        stage = el.querySelector(".ux-stage"), device = el.querySelector(".ux-device"), frame = el.querySelector("iframe"),
        mockLabel = el.querySelector(".ux-mocklabel"), badge = el.querySelector(".ux-countdown"), caption = el.querySelector(".ux-caption");
    if (params.get("chrome") === "off") el.querySelector(".ux-index").classList.add("ux-rec");

    function screenById(id) { return (cfg.screens || []).filter(function (s) { return s.id === id; })[0]; }

    function esc(t) { return String(t == null ? "" : t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
    side.innerHTML = "<div><h1>" + esc(cfg.title) + "</h1><div class=\"meta\">" + (cfg.revision ? "Revision " + esc(cfg.revision) : "") +
      (cfg.approval ? " · " + esc(cfg.approval) : "") + "</div></div>" +
      ((cfg.flows || []).length > 6 ? '<input class="ux-filter" type="search" placeholder="Lọc workflow… (W-01, tên, bước)">' : "") +
      '<div class="ux-flows"></div>';
    var flowsBox = side.querySelector(".ux-flows"), filterBox = side.querySelector(".ux-filter");
    if (filterBox) filterBox.oninput = function () { filter = filterBox.value.trim().toLowerCase(); renderSide(); };
    function matches(f) {
      if (!filter) return true;
      var hay = [f.id, f.title, f.goals].concat((f.steps || []).map(function (st) { return st.title + " " + st.screen; })).join(" ").toLowerCase();
      return hay.indexOf(filter) >= 0;
    }
    function renderSide() {
      var h = "", active = player.flow !== null ? player.flow : cur.flow;
      (cfg.flows || []).forEach(function (f, fi) {
        if (!matches(f)) return;
        var open = expanded[fi] !== undefined ? expanded[fi] : fi === active;
        h += '<div class="ux-flow' + (open ? " open" : "") + (fi === active ? " current" : "") + '"><h2 class="head" data-f="' + fi + '" title="' + (open ? "Thu gọn" : "Mở") + '">' +
          '<span class="caret">' + (open ? "▾" : "▸") + "</span><span>" + esc(f.id) + " · " + esc(f.title) + "</span>" +
          ((f.walkthrough || []).length ? '<span class="wt" title="Có walkthrough tự chạy">' + (player.flow === fi && player.playing ? "⏸" : "▶") + "</span>" : "") +
          '<span class="count">' + (f.steps || []).length + "</span></h2>";
        if (!open) { h += "</div>"; return; }
        h += f.goals ? '<div class="goal">Goal: ' + esc(f.goals) + "</div>" : "";
        if ((f.walkthrough || []).length) {
          var mine = player.flow === fi, playing = mine && player.playing;
          h += '<div class="ux-play' + (mine ? " active" : "") + '" data-f="' + fi + '"><button class="play">' + (playing ? "⏸ Pause" : "▶ Play") + "</button>" +
            '<button class="one" title="next walkthrough step">⏭ Step</button><select class="speed" title="playback speed">' +
            SPEEDS.map(function (x) { return "<option value=\"" + x + "\"" + (x === player.speed ? " selected" : "") + ">" + x + "×</option>"; }).join("") +
            '</select><span class="pos">' + (mine ? player.i : 0) + "/" + f.walkthrough.length + "</span></div>";
        }
        (f.steps || []).forEach(function (st, si) {
          var s = screenById(st.screen) || {};
          var on = cur.flow === fi && cur.step === si;
          h += '<button class="ux-step' + (on ? " active" : "") + '" data-f="' + fi + '" data-s="' + si + '" title="' + esc(st.screen + " · " + (s.title || "") + (st.state ? " · state " + st.state : "")) + '">' +
            '<span class="n">' + esc(st.n || si + 1) + '</span><span class="label">' + esc(st.title || s.title || st.screen) + "</span>" +
            '<span class="sid">' + esc(st.screen + (st.state ? ":" + st.state : "")) + "</span>" +
            (s.kind ? '<span class="tag ' + esc(s.kind) + '">' + esc(s.kind) + "</span>" : "") + "</button>";
        });
        h += "</div>";
      });
      var orphan = (cfg.screens || []).filter(function (s) {
        return !(cfg.flows || []).some(function (f) { return (f.steps || []).some(function (st) { return st.screen === s.id; }); });
      });
      if (orphan.length) {
        h += '<div class="ux-flow"><h2>Screens not in a workflow</h2>';
        orphan.forEach(function (s) { h += '<button class="ux-step" data-file="' + esc(s.file) + '"><span class="n">!</span><span class="label">' + esc(s.title) + '</span><span class="sid">' + esc(s.id) + "</span></button>"; });
        h += "</div>";
      }
      if (!h && filter) h = '<div class="goal">Không có workflow khớp "' + esc(filter) + '".</div>';
      flowsBox.innerHTML = h;
      side.querySelectorAll(".ux-flow .head").forEach(function (head) {
        head.onclick = function () { var fi = +head.dataset.f; expanded[fi] = !head.parentNode.classList.contains("open"); renderSide(); };
        var wt = head.querySelector(".wt");
        if (wt) wt.onclick = function (ev) {  // play straight from a collapsed workflow
          ev.stopPropagation();
          var fi = +head.dataset.f;
          expanded[fi] = true;
          if (player.flow === fi && player.playing) UX.pause(); else UX.play(cfg.flows[fi].id);
        };
      });
      side.querySelectorAll(".ux-play").forEach(function (box) {
        var id = cfg.flows[+box.dataset.f].id;
        box.querySelector(".play").onclick = function () { if (player.flow === +box.dataset.f && player.playing) UX.pause(); else UX.play(id); };
        box.querySelector(".one").onclick = function () { UX.stepOnce(id); };
        box.querySelector(".speed").onchange = function (e) { UX.setSpeed(e.target.value); };
      });
      side.querySelectorAll(".ux-step").forEach(function (b) {
        b.onclick = function () {
          UX.stop();
          if (b.dataset.file) { cur.flow = null; cur.step = -1; load(b.dataset.file); return; }
          go(+b.dataset.f, +b.dataset.s);
        };
      });
    }
    function renderBar() {
      var h = '<span class="title">' + (cur.file ? cur.file.replace(/^screens\//, "") : "") + '</span><span class="group">';
      platforms.forEach(function (p) {
        var d = dims(p, p === cur.platform ? cur.orientation : orientations(p)[0]);
        h += '<button data-p="' + p + '" class="' + (p === cur.platform ? "on" : "") + '">' + p + " " + d[0] + "×" + d[1] + "</button>";
      });
      h += "</span>";
      if (orientations(cur.platform).length > 1)
        h += '<button class="rot" title="Xoay: dọc / ngang (portrait / landscape)">⟲ ' + (cur.orientation === "landscape" ? "ngang" : "dọc") + "</button>";
      h += '<label class="stl" title="Trạng thái (data-state) của màn đang xem: default, loading, empty, error, …">Trạng thái <select class="st">' + cur.states.map(function (s) { return "<option" + (s === cur.state ? " selected" : "") + ">" + s + "</option>"; }).join("") +
        '</select></label><button class="nt ' + (cur.notes ? "on" : "") + '">notes</button>' +
        '<span class="group"><button class="prev">◀ step</button><button class="next">step ▶</button></span>';
      bar.innerHTML = h;
      bar.querySelectorAll("[data-p]").forEach(function (b) {
        b.onclick = function () { cur.platform = b.dataset.p; pickOrientation(cur.orientation); size(); renderBar(); syncUrl(); };
      });
      var rot = bar.querySelector(".rot");
      if (rot) rot.onclick = function () { UX.setOrientation(cur.orientation === "landscape" ? "portrait" : "landscape"); };
      bar.querySelector(".st").onchange = function (e) { cur.state = e.target.value; send({ type: "ux:setState", state: cur.state }); };
      bar.querySelector(".nt").onclick = function () { cur.notes = !cur.notes; send({ type: "ux:setNotes", on: cur.notes }); renderBar(); };
      bar.querySelector(".prev").onclick = function () { UX.stop(); step(-1); };
      bar.querySelector(".next").onclick = function () { UX.stop(); step(1); };
    }
    function send(m) { if (frame.contentWindow) frame.contentWindow.postMessage(m, "*"); }
    function size() {
      var d = dims(cur.platform, cur.orientation), pad = 40;
      device.className = "ux-device " + cur.platform + " " + cur.orientation;
      frame.style.width = d[0] + "px"; frame.style.height = d[1] + "px";
      var sx = (stage.clientWidth - 32) / (d[0] + pad), sy = (stage.clientHeight - 32) / (d[1] + pad);
      device.style.transform = "scale(" + Math.min(1, sx, sy) + ")";
    }
    function load(file, state) {
      cur.file = file; cur.state = state || "default";
      frame.src = file + "?notes=" + (cur.notes ? "on" : "off") + (state ? "&state=" + encodeURIComponent(state) : "");
      renderSide(); renderBar();
    }
    function go(fi, si) {
      var f = (cfg.flows || [])[fi]; if (!f || !f.steps[si]) return;
      cur.flow = fi; cur.step = si;
      var s = screenById(f.steps[si].screen);
      load(s ? s.file : f.steps[si].file, f.steps[si].state || null);
    }
    function step(d) {
      if (cur.flow === null) return;
      var f = cfg.flows[cur.flow], n = cur.step + d;
      if (n >= 0 && n < f.steps.length) go(cur.flow, n);
    }
    // ---------------------------------------------------------------- walkthrough player
    var waiters = {}, readyWaiter = null, reqId = 0;
    function sleep(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
    function request(msg, timeout) {
      return new Promise(function (resolve) {
        var id = ++reqId, t = setTimeout(function () { delete waiters[id]; resolve({}); }, timeout || 8000);
        waiters[id] = function (d) { clearTimeout(t); delete waiters[id]; resolve(d); };
        msg.id = id; msg.speed = player.speed; send(msg);
      });
    }
    function walk() { return player.flow === null ? [] : cfg.flows[player.flow].walkthrough || []; }
    function setCaption(text) { if (text) { caption.textContent = text; caption.hidden = false; } }
    function showScreen(sid, state) {
      var s = screenById(sid);
      if (!s) return Promise.resolve();
      if (s.file === cur.file) {
        if (state) { cur.state = state; send({ type: "ux:setState", state: state }); }
        return Promise.resolve();
      }
      return new Promise(function (resolve) {
        var t = setTimeout(function () { readyWaiter = null; resolve(); }, 8000);
        readyWaiter = function (d) { if (d.screen === sid) { clearTimeout(t); readyWaiter = null; resolve(); } };
        load(s.file, state);
      });
    }
    function seconds(v) {
      var m = String(v || "").match(/^(\d+(?:\.\d+)?)\s*(ms|s)?$/);
      return m ? (m[2] === "ms" ? +m[1] / 1000 : +m[1]) : 0;
    }
    function countdown(row, token) {
      // The badge always shows the real duration; only playback time is compressed (Wait (ms) or speed).
      var real = seconds(row.value), play = (row.wait || real * 1000) / player.speed, start = Date.now();
      var fast = play > 0 ? real * 1000 / play : 1;
      if (row.target) send({ type: "ux:highlight", target: row.target, on: true });
      badge.hidden = false;
      return new Promise(function (resolve) {
        (function tick() {
          var k = play > 0 ? Math.min(1, (Date.now() - start) / play) : 1;
          badge.innerHTML = "⏱ " + Math.ceil(real * (1 - k)) + "s / " + real + "s" + (fast > 1.05 ? " <small>⏩ ×" + Math.round(fast * 10) / 10 + "</small>" : "");
          if (k >= 1 || token !== player.token) {
            badge.hidden = true;
            if (row.target) send({ type: "ux:highlight", target: row.target, on: false });
            resolve(); return;
          }
          setTimeout(tick, 100);
        })();
      });
    }
    function markStep(row) {
      var f = cfg.flows[player.flow], hit = -1;
      f.steps.forEach(function (st, i) { if ((row.step && st.n === row.step) || (!row.step && hit < 0 && st.screen === row.screen)) hit = i; });
      if (hit >= 0) { cur.flow = player.flow; cur.step = hit; }
    }
    function runStep(row, token) {
      markStep(row);
      setCaption(row.caption);
      var a = row.action;
      return showScreen(row.screen, a === "show" ? row.state || "default" : null).then(function () {
        if (token !== player.token) return;
        if (a === "tap") return request({ type: "ux:tap", target: row.target });
        if (a === "type" || a === "scan") return request({ type: "ux:type", target: row.target, value: row.value, scan: a === "scan" }, 30000);
        if (a === "timer") return countdown(row, token);
      }).then(function () {
        if (token !== player.token) return;
        if (row.state && a !== "show") { cur.state = row.state; send({ type: "ux:setState", state: row.state }); }
        var pause = a === "timer" ? 300 : row.wait != null ? row.wait : a === "wait" ? 1000 : 900;
        return sleep(pause / player.speed);
      });
    }
    function finish() { player.playing = false; root.setAttribute("data-ux-play", "done"); renderSide(); }
    function loop(token) {
      if (!player.playing || token !== player.token) return;
      if (player.i >= walk().length) { finish(); return; }
      var row = walk()[player.i++];
      player.busy = true; renderSide();
      runStep(row, token).then(function () {
        player.busy = false;
        if (token !== player.token) return;
        if (player.i >= walk().length) finish(); else { renderSide(); loop(token); }
      });
    }
    function select(id) {
      var fi = -1;
      (cfg.flows || []).forEach(function (f, i) { if (f.id === id && (f.walkthrough || []).length) fi = i; });
      if (fi < 0) return false;
      if (player.flow !== fi || player.i >= walk().length) {
        player.token++; player.flow = fi; player.i = 0; player.busy = false; caption.hidden = true;
      }
      mockLabel.hidden = false;
      root.setAttribute("data-ux-play", "playing");
      return true;
    }
    UX.play = function (id) {
      if (!select(id)) return false;
      player.playing = true;
      if (!player.busy) loop(player.token); else renderSide();
      return true;
    };
    UX.pause = function () { player.playing = false; renderSide(); };
    UX.stepOnce = function (id) {
      if (!select(id || (player.flow !== null && cfg.flows[player.flow].id)) || player.busy) return false;
      player.playing = false;
      var token = player.token, row = walk()[player.i++];
      player.busy = true; renderSide();
      runStep(row, token).then(function () { player.busy = false; if (token !== player.token) return; if (player.i >= walk().length) finish(); else renderSide(); });
      return true;
    };
    UX.setOrientation = function (o) {
      if (orientations(cur.platform).indexOf(o) < 0) return false;
      cur.orientation = o; size(); renderBar(); syncUrl();
      return true;
    };
    UX.setSpeed = function (x) { player.speed = Math.min(2, Math.max(1, +x || 1)); renderSide(); };
    UX.stop = function () {
      if (player.flow === null) return;
      player.token++; player.playing = false; player.busy = false; player.flow = null; player.i = 0;
      mockLabel.hidden = true; badge.hidden = true; caption.hidden = true;
      root.setAttribute("data-ux-play", "stopped");
      renderSide();
    };

    window.addEventListener("message", function (ev) {
      var d = ev.data || {};
      if (d.type === "ux:done" && waiters[d.id]) waiters[d.id](d);
      if (d.type === "ux:ready") { cur.states = d.states || []; renderBar(); if (readyWaiter) readyWaiter(d); }
      if (d.type === "ux:state") { cur.state = d.state; renderBar(); }
      if (d.type === "ux:navigate") {
        var base = cur.file ? cur.file.replace(/[^/]*$/, "") : "";
        var target = (base + d.href.split("?")[0]).replace(/[^/]+\/\.\.\//g, "");
        var hits = [];
        if (cur.flow !== null) cfg.flows[cur.flow].steps.forEach(function (st, i) { var s = screenById(st.screen); if (s && s.file === target) hits.push(i); });
        var hit = hits.filter(function (i) { return i > cur.step; }).concat(hits)[0];
        if (hit === undefined) hit = -1;
        UX.stop();
        if (hit >= 0) go(cur.flow, hit); else load(target);
      }
    });
    window.addEventListener("resize", size);
    size();
    if (params.get("play")) {
      if (UX.play(params.get("play"))) return;
      root.setAttribute("data-ux-play", "missing");
    }
    if ((cfg.flows || []).length && cfg.flows[0].steps.length) go(0, 0);
    else if ((cfg.screens || []).length) load(cfg.screens[0].file);
    else { renderSide(); renderBar(); }
  };

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", initScreen); else initScreen();
})();
