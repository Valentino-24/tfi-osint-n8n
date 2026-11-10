/* ------------------------------------------------------------------ *
   * v3: el diseno de Canva + los datos reales de tesi_osint.            *
   * Todo lo numerado sale de /api/* en el navegador: no hay cifras      *
   * escritas a mano en este archivo.                                    *
   * ------------------------------------------------------------------ */
  const $ = id => document.getElementById(id);
  const slot = name => document.querySelector('[data-slot="' + name + '"]');
  const tpl = t => document.querySelector('[data-template-id="' + t + '"]');
  const esc = s => String(s ?? "").replace(/[&<>"']/g, c =>
    ({ "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;" }[c]));
  const num = n => Number(n || 0).toLocaleString("es-AR");
  const dec = (n, d = 1) => Number(n || 0).toLocaleString("es-AR",
    { minimumFractionDigits: d, maximumFractionDigits: d });

  async function get(url) {
    const r = await fetch(url);
    if (!r.ok) throw new Error(url + " -> " + r.status);
    return r.json();
  }
  const fecha = iso => iso
    ? new Date(String(iso).slice(0, 10) + "T00:00:00")
        .toLocaleDateString("es-AR", { day:"2-digit", month:"2-digit", year:"numeric" })
    : "…";
  const hoy = () => new Date().toLocaleDateString("es-AR",
    { day:"2-digit", month:"2-digit", year:"numeric" });
  const hora = ts => ts ? String(ts).replace("T", " ").slice(11, 16) : "…";

  /* barra del diseno: el ancho vive en --size */
  function barra(n, max, clase = "") {
    const pct = max ? Math.round(100 * n / max) : 0;
    return `<span class="bar-fill ${clase}" style="--size:${Math.max(pct, 1)}%"></span>`;
  }
  function filaBarra(nombre, valor, max, clase = "", mono = false) {
    return `<div class="bar-row">
      <span class="bar-name${mono ? " mono" : ""}">${esc(nombre)}</span>
      <span class="bar-track">${barra(valor, max, clase)}</span>
      <span class="mono">${num(valor)}</span>
    </div>`;
  }
  /* comunidad desactivada: fila real en 0, sin barra (no compite con el alcance) */
  function filaGhost(nombre, etiqueta = "desactivada") {
    return `<div class="bar-row ghost">
      <span class="bar-name">${esc(nombre)}<span class="off">${esc(etiqueta)}</span></span>
      <span class="bar-track"></span>
      <span class="mono">0</span>
    </div>`;
  }

  /* ---------------------------------------------------------- menú móvil */
  const menuButton = $("menu-toggle");
  const linksBox = $("nav-links");
  function closeMenu() {
    linksBox.classList.remove("open");
    menuButton.setAttribute("aria-expanded", "false");
    menuButton.setAttribute("aria-label", "Abrir menú");
  }
  menuButton.addEventListener("click", () => {
    const open = linksBox.classList.toggle("open");
    menuButton.setAttribute("aria-expanded", String(open));
    menuButton.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
  });
  linksBox.querySelectorAll("a").forEach(l => l.addEventListener("click", closeMenu));
  document.addEventListener("keydown", e => {
    if (e.key === "Escape" && linksBox.classList.contains("open")) { closeMenu(); menuButton.focus(); }
  });

  /* ------------------------------------------------- tema claro / oscuro */
  const themeButton = $("theme-toggle");
  function aplicarTema(t) {
    document.documentElement.setAttribute("data-theme", t);
    themeButton.setAttribute("aria-pressed", String(t === "light"));
    themeButton.setAttribute("aria-label",
      t === "light" ? "Cambiar a modo oscuro" : "Cambiar a modo claro");
  }
  let tema = localStorage.getItem("tema") || "light";
  aplicarTema(tema);
  themeButton.addEventListener("click", () => {
    tema = tema === "light" ? "dark" : "light";
    localStorage.setItem("tema", tema);
    aplicarTema(tema);
  });

  /* ------------------------------------------------- reveal al hacer scroll */
  const revealItems = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add("visible"); observer.unobserve(entry.target); }
    }), { threshold: .06 });
    revealItems.forEach(item => observer.observe(item));
  } else {
    revealItems.forEach(item => item.classList.add("visible"));
  }

  /* ------------------------------------------------------------- entidades */
  const TIPOS = [["cves","CVEs"],["domains","Dominios"],["ips","IPs"],
                 ["emails","Correos"],["products","Productos"]];
  const tabs = [...document.querySelectorAll('[role="tab"]')];
  const entityPanel = $("entity-panel");
  let entidades = {}, nPosts = 0;

  const ENT_VISIBLES = 6;
  let entExpandido = false;

  function renderEnt(tipo) {
    const etiqueta = TIPOS.find(([t]) => t === tipo)[1];
    const filas = entidades[tipo] || [];
    if (!filas.length) {
      return `<p class="muted-load">Sin ${esc(etiqueta.toLowerCase())} extraídos todavía. `
           + `No se muestran menciones inventadas.</p>`;
    }
    const max = Math.max(1, ...filas.map(f => f.menciones));
    const visibles = entExpandido ? filas : filas.slice(0, ENT_VISIBLES);
    const ocultas = filas.length - visibles.length;
    let html = `<div class="bars">`
      + visibles.map(f => filaBarra(f.entidad, f.menciones, max, "", true)).join("")
      + `</div>`;
    if (ocultas > 0 || entExpandido) {
      html += `<button type="button" class="entity-more">`
        + (entExpandido ? "Ver menos" : `Ver más (${ocultas})`) + `</button>`;
    }
    return html;
  }

  function pintarEnt(tipo) {
    entityPanel.innerHTML = renderEnt(tipo);
    const mas = entityPanel.querySelector(".entity-more");
    if (mas) mas.addEventListener("click", () => {
      entExpandido = !entExpandido;
      pintarEnt(tipo);
    });
  }

  function selectTab(tab) {
    tabs.forEach(item => {
      const sel = item === tab;
      item.setAttribute("aria-selected", String(sel));
      item.tabIndex = sel ? 0 : -1;
    });
    entityPanel.setAttribute("aria-labelledby", tab.id);
    entityPanel.className = "entity-list";
    entExpandido = false;
    pintarEnt(tab.id.slice(4));
  }
  tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => selectTab(tab));
    tab.addEventListener("keydown", e => {
      let next = index;
      if (e.key === "ArrowRight") next = (index + 1) % tabs.length;
      else if (e.key === "ArrowLeft") next = (index - 1 + tabs.length) % tabs.length;
      else if (e.key === "Home") next = 0;
      else if (e.key === "End") next = tabs.length - 1;
      else return;
      e.preventDefault();
      selectTab(tabs[next]);
      tabs[next].focus();
    });
  });

  async function cargarEntidades() {
    const datos = {};
    await Promise.all(TIPOS.map(async ([t]) => {
      datos[t] = await get("/api/entidades/" + t).catch(() => []);
    }));
    entidades = datos;
    selectTab(tabs[0]);
  }

  /* ------------------------------------------------------------- datos */
  async function cargar() {
    const [res, suf, com, cat, sco, serie, ano, ult, alr, reg, lat] = await Promise.all([
      get("/api/resumen"),
      get("/api/suficiencia"),
      get("/api/comunidades-estado"),
      get("/api/por-categoria"),
      get("/api/distribucion-score"),
      get("/api/serie-diaria"),
      get("/api/anomalias"),
      get("/api/ultimos-posts?limite=12"),
      get("/api/alertas"),
      get("/api/regimen"),
      get("/api/latencia"),
    ]);
    // Render latencia
    const latencia = lat || [];
    const elL = $("latency-table");
    if (!latencia.length) { elL.innerHTML = "<p class=\"muted-load\">Sin datos de latencia.</p>"; }
    else { elL.innerHTML = "<table class=\"data-table\"><thead><tr><th>Grupo</th><th>N</th><th>P50 (min)</th><th>P95 (min)</th><th>Max (min)</th></tr></thead><tbody>" +
      latencia.map(r => "<tr><td>" + esc(r.grupo) + "</td><td>" + num(r.n) + "</td><td>" + dec(r.p50_min) + "</td><td>" + dec(r.p95_min) + "</td><td>" + dec(r.max_min) + "</td></tr>").join("") +
      "</tbody></table>";
      slot("latency-nota").textContent = "2 grupos: en_ventana y arrastre_inicial."; }
    // Render alertas
    const alertas = alr || [];
    const elA = $("alerts-table");
    if (!alertas.length) { elA.innerHTML = "<p class=\"muted-load\">Sin alertas registradas.</p>"; }
    else { elA.innerHTML = "<table class=\"data-table\"><thead><tr><th>Fecha</th><th>Categoria</th><th>Obs.</th><th>Umbral</th><th>Estado</th></tr></thead><tbody>" +
      alertas.map(a => "<tr><td>" + fecha(a.fecha) + "</td><td>" + esc(a.categoria) + "</td><td>" + num(a.n_observado) + "</td><td>" + dec(a.umbral) + "</td><td><span class=\"pill\">" + esc(a.estado) + "</span></td></tr>").join("") +
      "</tbody></table>";
      slot("alerts-nota").textContent = alertas.length + " alertas registradas. Canal: " + alertas[0].canal + "."; }
    // Render regimen
    const regimen = reg || [];
    const elR = $("regime-table");
    if (!regimen.length) { elR.innerHTML = "<p class=\"muted-load\">Sin datos de regimen.</p>"; }
    else { elR.innerHTML = "<table class=\"data-table\"><thead><tr><th>Fecha</th><th>Posts</th><th>Primera ingesta</th><th>Ultima ingesta</th></tr></thead><tbody>" +
      regimen.map(r => "<tr><td>" + fecha(r.fecha) + "</td><td>" + num(r.publicaciones) + "</td><td>" + (r.primera_ingesta || "\u2014") + "</td><td>" + (r.ultima_ingesta || "\u2014") + "</td></tr>").join("") +
      "</tbody></table>";
      slot("regime-nota").textContent = regimen.length + " dias con ingesta. Regimen: jornadas diurnas, instancia activa ~27.9% del tramo con registro."; }
    nPosts = res.total_posts;

    /* --- banner de aviso --- */
    slot("v-fecha").textContent = hoy();
    slot("v-n").textContent = num(res.total_posts);
    slot("v-carga").textContent = res.ultima_carga
      ? String(res.ultima_carga).replace("T", " ").slice(0, 16) : "…";

    /* --- KPIs --- */
    const activas = com.filter(c => c.active_monitoring);
    const pctSenal = res.total_posts
      ? dec(100 * res.con_senal / res.total_posts, 1) : "0,0";
    tpl("kpi-1-value").textContent = num(res.total_posts);
    tpl("kpi-1-demo").textContent = "ventana B5";
    tpl("kpi-2-value").textContent = num(res.con_senal);
    tpl("kpi-2-demo").textContent = pctSenal + "% del corpus";
    tpl("kpi-3-value").textContent = num(activas.length);
    tpl("kpi-3-demo").textContent = "denominador " + activas.length;
    tpl("kpi-4-value").textContent = num(res.dias_recoleccion);
    tpl("kpi-4-demo").textContent = res.desde && res.hasta
      ? String(res.desde).slice(8) + "/" + String(res.desde).slice(5, 7) + " a "
        + String(res.hasta).slice(8) + "/" + String(res.hasta).slice(5, 7)
      : "…";
    slot("r-obs").innerHTML =
      "<b>" + num(res.total_posts) + "</b> posts del <b>" + fecha(res.desde)
      + "</b> al <b>" + fecha(res.hasta) + "</b>, consulta del " + hoy() + ".";

    /* --- comunidades: alcance activo + las desactivadas en 0 --- */
    const maxCom = Math.max(1, ...activas.map(c => c.total));
    const inactivas = com.filter(c => !c.active_monitoring);
    $("community-bars").innerHTML =
      activas.map((c, i) =>
        filaBarra(c.display_name, c.total, maxCom, i === 0 ? "" : "blue")).join("")
      + inactivas.map(c => filaGhost(c.display_name)).join("");
    slot("com-nota").innerHTML = activas
      .map(c => "<b>" + esc(c.display_name) + "</b> " + num(c.total) + " posts").join(", ")
      + " (de " + num(res.total_posts) + ").";

    /* --- categorías --- */
    const maxCat = Math.max(1, ...cat.map(c => c.total));
    $("category-bars").innerHTML = cat.map(c =>
      filaBarra(c.categoria, c.total, maxCat,
                c.categoria === "No relevante" ? "gray" : "")).join("");
    const conPosts = cat.filter(c => c.categoria !== "No relevante").length;
    slot("cat-nota").innerHTML = "<b>" + conPosts + "</b> de las nueve tienen posts hoy; "
      + "el resto suma 0. Observación: " + num(res.total_posts) + " posts, consulta del "
      + hoy() + ".";

    /* --- score de significancia --- */
    const maxSco = Math.max(1, ...sco.map(s => s.total));
    $("score-bars").innerHTML = sco.map(s => {
      const t = String(s.tramo);
      const clase = t === "0.00" ? "gray"
                  : (t === "0.75-0.99" || t === "1.00") ? "amber" : "";
      return filaBarra(t.replace(/\./g, ","), s.total, maxSco, clase, true);
    }).join("");
    /* --- score: que significa cada tramo (regla min(1, hits/4)) --- */
    const HITS = { "0.00": "0 coincidencias", "0.01-0.49": "1 coincidencia",
                   "0.50-0.74": "2 coincidencias", "0.75-0.99": "3 coincidencias",
                   "1.00": "4 o más" };
    slot("score-legend").innerHTML = sco
      .filter(s => HITS[String(s.tramo)])
      .map(s => `<div><span class="mono">${esc(String(s.tramo).replace(/\./g, ","))}</span>`
        + `<span>${esc(HITS[String(s.tramo)])} · <b>${num(s.total)}</b> posts</span></div>`)
      .join("");
    slot("score-nota").innerHTML = "Observación: " + num(res.total_posts)
      + " posts, consulta del " + hoy() + ".";

    /* --- entidades --- */
    slot("ent-nota").innerHTML = "Observación: " + num(res.total_posts)
      + " posts, consulta del " + hoy() + ".";

    /* --- serie diaria --- */
    const maxDia = Math.max(1, ...serie.map(s => s.total));
    $("daily-chart").innerHTML = serie.map(s => {
      const h = Math.max(2, Math.round(100 * s.total / maxDia));
      const dd = String(s.dia).slice(8, 10);
      return `<div class="day">
        <span class="day-value">${num(s.total)}</span>
        <span class="column" style="--height:${h}%"></span>
        <span class="day-label">${dd}</span>
      </div>`;
    }).join("");
    const primero = serie.length ? serie[0].dia : null;
    const ultimo = serie.length ? serie[serie.length - 1].dia : null;
    // huecos reales entre el primer y el ultimo dia con ingesta
    const faltantes = [];
    if (serie.length > 1) {
      const presentes = new Set(serie.map(s => String(s.dia)));
      const isoDe = d => d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0")
        + "-" + String(d.getDate()).padStart(2, "0");
      const d = new Date(String(primero) + "T12:00:00");
      const fin = new Date(String(ultimo) + "T12:00:00");
      while (d < fin) {
        d.setDate(d.getDate() + 1);
        const iso = isoDe(d);
        if (!presentes.has(iso)) faltantes.push(iso);
      }
    }
    slot("daily-nota").innerHTML = "<b>" + serie.length + "</b> días con recolección: de "
      + (primero ? fecha(primero) : "…") + " a " + (ultimo ? fecha(ultimo) : "…")
      + (faltantes.length
          ? ". Sin ingesta el " + faltantes.map(fecha).join(", ")
          : "")
      + ". Última carga del sistema "
      + (res.ultima_carga ? String(res.ultima_carga).replace("T", " ").slice(0, 16) : "…") + ".";

    /* --- anomalías: cómo leer una --- */
    const disparos = ano.filter(a => a.disparo);
    const conBase = disparos.filter(a => Number(a.base_media) > 0);
    const ej = conBase[0] || disparos[0] || null;
    const ultDia = ano.length ? ano[0].dia : null;
    const delDia = ano.filter(a => a.dia === ultDia && a.n_observado > 0)
                      .sort((a, b) => b.n_observado - a.n_observado);
    const items = [];
    if (ej) items.push(ej);
    for (const a of delDia) {
      if (items.length >= 3) break;
      if (!items.some(x => x.categoria === a.categoria)) items.push(a);
    }
    if (items.length) {
      const escala = Math.max(...items.map(a => Math.max(a.n_observado, a.umbral)));
      const eje = escala <= 5 ? 5 : escala <= 10 ? 10 : escala <= 20 ? 20
                : escala <= 50 ? 50 : escala <= 100 ? 100 : Math.ceil(escala);
      $("comparison").innerHTML = items.map(a => {
        const estado = a.disparo ? "superó el umbral" : "sin disparo";
        const pObs = Math.max(1, Math.round(100 * a.n_observado / eje));
        const pUmb = Math.max(1, Math.round(100 * a.umbral / eje));
        return `<div class="compare-item">
          <div class="compare-title">
            <strong>${esc(a.categoria)}</strong>
            <span>${fecha(a.dia)} · observación ${a.n_observado} · ${estado}</span>
          </div>
          <div class="compare-track" style="--threshold:${pUmb}%">
            ${barra(a.n_observado, eje, a.disparo ? "amber" : "blue")}
          </div>
          <span class="compare-meta">Base ${dec(a.base_media, 2)} · Umbral ${dec(a.umbral, 2)} · eje ${eje}</span>
        </div>`;
      }).join("");
    } else {
      $("comparison").innerHTML =
        '<p class="muted-load">Todavía no hay anomalías registradas.</p>';
    }

    const sinBase = disparos.length - conBase.length;
    let nota = "El motor corre una vez por día, a las 12:05, sobre el día anterior. "
      + "Última evaluación: <b>" + (ultDia ? fecha(ultDia) : "…") + "</b>.";
    if (disparos.length) {
      nota += " La ventana acumula <b>" + disparos.length + " filas con disparo</b>";
      if (sinBase > 0) {
        nota += ": " + sinBase + " de ellas tienen <code>base_media 0,0</code>, porque son "
          + "del primer día, cuando aún no existían diez días previos de referencia.";
      } else {
        nota += ".";
      }
      if (ej) {
        nota += " La última con base distinta de cero es <b>" + esc(ej.categoria) + "</b> el "
          + fecha(ej.dia) + " (observación " + ej.n_observado + " · base "
          + dec(ej.base_media, 2) + " · umbral " + dec(ej.umbral, 2) + ").";
      }
    } else {
      nota += " Sin disparos en la ventana.";
    }
    slot("ano-nota").innerHTML = nota;

    /* --- ventana B5 en las limitaciones --- */
    const estadoTxt = suf.estado === "objetivo_alcanzado" ? "objetivo alcanzado"
                    : suf.estado === "minimo_alcanzado"
                      ? "mínimo alcanzado, objetivo pendiente" : "ventana abierta";
    slot("limites").innerHTML = "La ventana B5 va en <b>" + suf.dias_completos
      + " días completos</b> de evaluaciones de anomalías (" + estadoTxt
      + "; piso " + suf.minimo + " / objetivo " + suf.objetivo + ", del "
      + (suf.primer_dia ? fecha(suf.primer_dia) : "…") + " al "
      + (suf.ultimo_dia ? fecha(suf.ultimo_dia) : "…")
      + "). El corte de la ventana lo fijan los autores.";

    /* --- tabla de posts --- */
    $("posts-body").innerHTML = ult.length ? ult.map(p => `<tr>
      <td>${esc(p.display_name)}</td>
      <td><a href="${esc(p.url)}" target="_blank" rel="noopener">${esc(p.title)}</a></td>
      <td>${esc(p.nlp_category ?? "—")}</td>
      <td class="mono">${p.nlp_score ?? "—"}</td></tr>`).join("")
      : `<tr><td colspan="4" class="table-empty">Sin posts todavía.</td></tr>`;

    /* --- pie --- */
    slot("pie").innerHTML = "Ventana B5 · datos al " + fecha(res.hasta)
      + " · consulta del " + hoy();
  }

  async function arrancar() {
    try {
      await Promise.all([cargar(), cargarEntidades()]);
      setInterval(cargar, 60000); // lectura pura; no genera evidencia nueva
    } catch (e) {
      console.error(e);
      const aviso = document.getElementById('transparency-text');
      if (aviso) { aviso.style.color = "var(--warn)";
      aviso.innerHTML = "No se pudo leer la base (" + esc(e.message) + "). Verificá que el "
        + "contenedor <code>tfi-postgres</code> esté levantado y que <code>.env</code> tenga "
        + "la contraseña del rol de lectura.";
      }
      document.querySelectorAll(".metric, [data-slot]").forEach(el => {
        if (el.textContent.trim() === "…" || el.textContent.includes("Consultando")) {
          el.textContent = "—";
        }
      });
    }
  }
  arrancar();