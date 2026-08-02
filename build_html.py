# -*- coding: utf-8 -*-
import json, datetime

with open("menu_data.json", encoding="utf-8") as f:
    DATA = json.load(f)

# Calendario: cada menu (A, B, C) se mantiene 3 semanas seguidas antes de cambiar
# al siguiente. Un ciclo completo = 9 semanas, empezando lunes 27 julio 2026.
start = datetime.date(2026, 7, 27)
rotation = ["A", "B", "C"]
calendar = []
for i, menu in enumerate(rotation):
    bloque_inicio = start + datetime.timedelta(weeks=3 * i)
    bloque_fin = bloque_inicio + datetime.timedelta(days=20)  # 3 semanas = 21 dias
    calendar.append({
        "n": i + 1,
        "inicio": bloque_inicio.strftime("%d/%m"),
        "fin": bloque_fin.strftime("%d/%m"),
        "menu": menu,
    })

DIAS_ORDEN = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]

html_json = json.dumps(DATA, ensure_ascii=False)
cal_json = json.dumps(calendar, ensure_ascii=False)
dias_json = json.dumps(DIAS_ORDEN, ensure_ascii=False)

TEMPLATE = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Menu semanal rotativo sin gluten</title>
<style>
:root{
  --verde:#3f6b4f; --verde-claro:#e8f2ea; --naranja:#d97b3f; --naranja-claro:#fbeee2;
  --gris:#5b5b5b; --gris-claro:#f4f3f0; --borde:#e2ded6; --blanco:#fff;
  --rojo:#b23b3b;
}
*{box-sizing:border-box;}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  background:var(--gris-claro);color:#2b2b2b;line-height:1.45;}
header{background:var(--verde);color:#fff;padding:18px 16px 14px;position:sticky;top:0;z-index:30;box-shadow:0 2px 6px rgba(0,0,0,.15);}
header h1{margin:0 0 2px;font-size:1.25rem;}
header p{margin:0;font-size:.82rem;opacity:.9;}
.wrap{max-width:760px;margin:0 auto;padding:0 12px 60px;}

.calendario{display:flex;flex-direction:column;gap:8px;margin:14px 0 18px;}
.calendario button{display:flex;align-items:center;justify-content:space-between;gap:10px;
  border:1px solid var(--borde);background:var(--blanco);border-radius:12px;padding:12px 14px;
  font-size:.85rem;text-align:left;cursor:pointer;color:#333;width:100%;}
.calendario button b{font-size:1.05rem;}
.calendario button .fechas{color:#888;font-size:.8rem;}
.calendario button.activa{outline:2px solid var(--naranja);}
.calendario button.tagA b{color:#3f6b4f;} .calendario button.tagB b{color:#2f6690;} .calendario button.tagC b{color:#a8503b;}

.tabs-semana{display:flex;gap:8px;margin:10px 0 16px;position:sticky;top:64px;background:var(--gris-claro);
  padding:8px 0;z-index:20;}
.tabs-semana button{flex:1;padding:10px 6px;border-radius:10px;border:1px solid var(--borde);background:var(--blanco);
  font-weight:600;font-size:.95rem;cursor:pointer;color:#555;}
.tabs-semana button.activa{background:var(--verde);color:#fff;border-color:var(--verde);}

.subtabs{display:flex;gap:6px;overflow-x:auto;padding-bottom:4px;margin-bottom:12px;-webkit-overflow-scrolling:touch;}
.subtabs button{flex:0 0 auto;padding:8px 14px;border-radius:20px;border:1px solid var(--borde);background:var(--blanco);
  font-size:.85rem;cursor:pointer;color:#444;white-space:nowrap;}
.subtabs button.activa{background:var(--naranja);color:#fff;border-color:var(--naranja);}

.prep-domingo{background:var(--naranja-claro);border:1px solid #f0d3b8;border-radius:12px;padding:12px 14px;margin-bottom:16px;}
.prep-domingo h3{margin:0 0 10px;font-size:1rem;color:var(--naranja);}
.paso-domingo{background:#fff;border:1px solid #f0d3b8;border-radius:10px;padding:10px 12px;margin-bottom:8px;}
.paso-domingo:last-child{margin-bottom:0;}
.paso-titulo{font-weight:700;font-size:.9rem;color:#8a4d1f;margin-bottom:4px;}
.prep-domingo ul{margin:0 0 6px;padding-left:20px;font-size:.86rem;}
.prep-domingo .como{font-size:.82rem;color:#5b4632;background:#fff8f0;border-radius:8px;padding:8px 10px;}
.nota-seguridad{font-size:.82rem;color:#7a3b12;background:#fff1de;border:1px solid #f0d3b8;border-radius:8px;padding:8px 10px;margin-bottom:10px;}
.separador-tanda{border:none;border-top:2px dashed #f0d3b8;margin:18px 0;}

.dia-panel{display:none;}
.dia-panel.activa{display:block;}

.comida{background:var(--blanco);border:1px solid var(--borde);border-radius:12px;padding:12px 14px;margin-bottom:10px;}
.comida h4{margin:0 0 6px;font-size:.78rem;text-transform:uppercase;letter-spacing:.04em;color:var(--verde);}
.comida .titulo{font-weight:600;margin:0 0 6px;font-size:.98rem;}
.persona-block{margin-bottom:8px;padding-bottom:8px;border-bottom:1px dashed var(--borde);}
.persona-block:last-child{border-bottom:none;margin-bottom:0;padding-bottom:0;}
.persona-nombre{font-size:.75rem;font-weight:700;color:var(--naranja);margin-bottom:2px;}
ul.ingredientes{margin:4px 0;padding-left:18px;font-size:.88rem;}
ul.ingredientes li{margin-bottom:2px;}
.extra{background:var(--verde-claro);border-radius:8px;padding:6px 10px;margin-top:6px;font-size:.85rem;}
.extra b{color:var(--verde);}
.nota{font-size:.8rem;color:#666;margin-top:6px;font-style:italic;}
.libre{color:#888;font-size:.9rem;font-style:italic;}

.compra-cat{background:var(--blanco);border:1px solid var(--borde);border-radius:12px;padding:12px 14px;margin-bottom:10px;}
.compra-cat h4{margin:0 0 8px;font-size:.9rem;color:var(--verde);}
.compra-cat ul{margin:0;padding-left:0;list-style:none;font-size:.9rem;}
.compra-cat li{padding:4px 0;border-bottom:1px solid #f0efec;display:flex;justify-content:space-between;gap:8px;}
.compra-cat li:last-child{border-bottom:none;}
.compra-cat li span.cant{color:var(--naranja);font-weight:600;white-space:nowrap;}

.reparto{color:#888;font-size:.82em;font-style:italic;}
.leyenda{font-size:.78rem;color:#777;margin:4px 0 16px;}
footer{text-align:center;font-size:.75rem;color:#999;padding:20px 0;}
h2.titulo-semana{font-size:1.05rem;color:var(--verde);margin:4px 0 2px;}
p.sub-semana{font-size:.82rem;color:#777;margin:0 0 12px;}
details.notas-generales{background:var(--verde-claro);border:1px solid #cfe3d4;border-radius:12px;
  padding:10px 14px;margin:14px 0;}
details.notas-generales summary{font-weight:700;color:var(--verde);cursor:pointer;font-size:.92rem;}
details.notas-generales ul{margin:8px 0 2px;padding-left:18px;font-size:.85rem;}
details.notas-generales li{margin-bottom:5px;}
</style>
</head>
<body>
<header>
  <h1>Menu semanal &mdash; sin gluten</h1>
  <p>3 menus (A, B, C) &middot; cada uno se repite 3 semanas seguidas antes de cambiar al siguiente</p>
</header>
<div class="wrap">

  <details class="notas-generales" open>
    <summary>Como funciona esto (leer primero)</summary>
    <ul>
      <li><b>No cambia cada semana:</b> hay 3 menus distintos, <b>Menu A</b>, <b>Menu B</b> y <b>Menu C</b>. Cada uno se cocina y se compra igual durante <b>3 semanas seguidas</b> (mismo menu, misma compra, mismo cocinado). Al terminar esas 3 semanas se cambia al siguiente menu.</li>
      <li><b>Calendario de abajo:</b> cada tarjeta es un bloque de 3 semanas con sus fechas reales. Se empieza el lunes 27 de julio de 2026 con el Menu A hasta el 16 de agosto; el 17 de agosto se pasa al Menu B; y asi. Pulsando una tarjeta se abre ese menu.</li>
      <li><b>Cocinado en dos tandas (seguridad alimentaria):</b> nada se cocina para toda la semana de golpe. El domingo se cocina solo lo que se va a comer hasta el miercoles (tanda 1), y el miercoles por la tarde se hace una segunda tanda mas pequeña para jueves-sabado (tanda 2). Asi ningun arroz, pasta, carne o pescado pasa mas de 3 dias en la nevera. Ademas, las <b>cenas se cocinan siempre al momento</b> (la proteina y las guarniciones tipo patata/boniato), no se guardan de un dia para otro: solo se preparan con antelacion los tuppers de la comida (y algun snack), que son los que se llevan fuera y hay menos tiempo de hacer por la mañana.</li>
      <li><b>Sin gluten estricto:</b> comprar siempre avena, tortitas de arroz, salsa de soja y similares con sello "sin gluten" certificado (no basta con que el ingrediente sea naturalmente libre de gluten, por el riesgo de contaminacion cruzada en fabrica).</li>
      <li><b>Embarazo:</b> todos los lacteos son pasteurizados; nada de embutido curado crudo (jamon serrano, lomo, chorizo); pescados siempre bien cocinados (nunca crudos ni poco hechos) y limitados a atun/salmon/pescado blanco (se evitan especies con mercurio alto); marisco siempre muy hecho; sin alcohol en ninguna receta.</li>
      <li><b>Comidas libres:</b> maximo 1-2 por semana (marcadas en el menu, normalmente el sabado y/o coincidiendo con algun plan social).</li>
      <li><b>Hidratacion:</b> especialmente cuidada los dias de carrera, bici larga y Hyrox; agua con normalidad el resto de comidas.</li>
      <li><b>Extra Ruben:</b> las lineas marcadas como "Extra" se suman a la cantidad compartida para ajustar a sus dias de mas entrenamiento (2700-4000+ kcal segun el dia).</li>
      <li><b>Reparto por persona:</b> en las comidas compartidas (almuerzo, comida y cena) cada ingrediente muestra entre parentesis una propuesta de reparto (aprox. 45% Lydia / 55% Ruben antes de sumar lo de "Extra"), pensada solo como punto de partida orientativo para pesar/repartir el plato; ajustadlo libremente segun el hambre de cada dia.</li>
      <li><b>Cantidades:</b> todas en crudo/seco (carnes y pescados en crudo; arroz, pasta y legumbre en seco/escurrido antes de cocer).</li>
    </ul>
  </details>

  <div id="calendario" class="calendario"></div>

  <div class="tabs-semana">
    <button data-semana="A" onclick="mostrarSemana('A')">Menu A</button>
    <button data-semana="B" onclick="mostrarSemana('B')">Menu B</button>
    <button data-semana="C" onclick="mostrarSemana('C')">Menu C</button>
  </div>

  <h2 class="titulo-semana" id="tituloSemana"></h2>
  <p class="sub-semana" id="fechasSemana"></p>
  <p class="sub-semana">Se cocina y compra igual las 3 semanas que dure este menu. Cantidades combinadas para 2 personas, en crudo/seco, con una propuesta de reparto por persona entre parentesis (ver "Como funciona esto" arriba). Las lineas "Extra Ruben" se añaden aparte en dias de mas entrenamiento.</p>

  <div class="subtabs" id="subtabsVista">
    <button data-vista="menu" class="activa" onclick="mostrarVista('menu')">Menu por dias</button>
    <button data-vista="compra" onclick="mostrarVista('compra')">Lista de la compra</button>
  </div>

  <div id="vistaMenu">
    <div class="prep-domingo" id="prepDomingo"></div>
    <div class="subtabs" id="subtabsDias"></div>
    <div id="diasContainer"></div>
  </div>

  <div id="vistaCompra" style="display:none;">
    <div id="compraContainer"></div>
  </div>

  <footer>Preparado para Ruben y Lydia &middot; compra los viernes &middot; cocinado en dos tandas: domingo y miercoles</footer>
</div>

<script>
const DATA = __DATA_JSON__;
const CALENDARIO = __CAL_JSON__;
const DIAS_ORDEN = __DIAS_JSON__;

let semanaActual = "A";
let diaActual = "Lunes";
let vistaActual = "menu";

function pintarCalendario(){
  const cont = document.getElementById("calendario");
  cont.innerHTML = "";
  CALENDARIO.forEach(w => {
    const b = document.createElement("button");
    b.className = "tag" + w.menu + (w.menu === semanaActual ? " activa" : "");
    b.innerHTML = "<span><b>Menu " + w.menu + "</b><br><span class='fechas'>" + w.inicio + " - " + w.fin + " (3 semanas)</span></span>";
    b.onclick = () => mostrarSemana(w.menu);
    cont.appendChild(b);
  });
}

function fechasDeMenu(sem){
  const w = CALENDARIO.find(x => x.menu === sem);
  return w ? ("Del " + w.inicio + " al " + w.fin + " (3 semanas seguidas con este menu)") : "";
}

function mostrarSemana(sem){
  semanaActual = sem;
  document.querySelectorAll(".tabs-semana button").forEach(b => {
    b.classList.toggle("activa", b.dataset.semana === sem);
  });
  document.getElementById("tituloSemana").textContent = "Menu " + sem;
  document.getElementById("fechasSemana").textContent = fechasDeMenu(sem);
  pintarCalendario();
  pintarPrepDomingo();
  pintarSubtabsDias();
  diaActual = "Lunes";
  pintarDia();
  pintarCompra();
}

function mostrarVista(v){
  vistaActual = v;
  document.querySelectorAll("#subtabsVista button").forEach(b => b.classList.toggle("activa", b.dataset.vista === v));
  document.getElementById("vistaMenu").style.display = v === "menu" ? "block" : "none";
  document.getElementById("vistaCompra").style.display = v === "compra" ? "block" : "none";
}

function pintarTanda(p){
  let html = "<h3>" + p.titulo + "</h3>";
  if(p.nota_seguridad) html += "<div class='nota-seguridad'>" + p.nota_seguridad + "</div>";
  p.pasos.forEach(paso => {
    html += "<div class='paso-domingo'>";
    html += "<div class='paso-titulo'>" + paso.titulo + "</div>";
    html += "<ul>" + paso.ingredientes.map(i => "<li>" + i.cantidad + " " + i.unidad + " de " + i.nombre + "</li>").join("") + "</ul>";
    html += "<div class='como'>" + paso.instrucciones + "</div>";
    html += "</div>";
  });
  return html;
}

function pintarPrepDomingo(){
  const el = document.getElementById("prepDomingo");
  const semana = DATA[semanaActual];
  let html = pintarTanda(semana.prep_domingo);
  if(semana.prep_miercoles){
    html += "<hr class='separador-tanda'>";
    html += pintarTanda(semana.prep_miercoles);
  }
  el.innerHTML = html;
}

function pintarSubtabsDias(){
  const cont = document.getElementById("subtabsDias");
  cont.innerHTML = "";
  DIAS_ORDEN.forEach(d => {
    if(!(d in DATA[semanaActual].dias)) return;
    const b = document.createElement("button");
    b.textContent = d;
    b.dataset.dia = d;
    b.className = d === diaActual ? "activa" : "";
    b.onclick = () => { diaActual = d; pintarDia(); document.querySelectorAll("#subtabsDias button").forEach(x=>x.classList.toggle("activa", x.dataset.dia===d)); };
    cont.appendChild(b);
  });
}

const LYDIA_RATIO = 0.45;

function formatNum(n){
  return Number.isInteger(n) ? n : Math.round(n*10)/10;
}

function repartoTexto(i){
  let lydiaQty;
  if(i.unidad === "ud"){
    lydiaQty = Math.round(i.cantidad * LYDIA_RATIO);
  } else {
    lydiaQty = Math.round(i.cantidad * LYDIA_RATIO);
  }
  const rubenQty = Math.round((i.cantidad - lydiaQty) * 10) / 10;
  return " <span class='reparto'>(" + lydiaQty + " " + i.unidad + " Lydia / " + rubenQty + " " + i.unidad + " Ruben)</span>";
}

function ingredientesHTML(lista, conReparto){
  if(!lista || lista.length === 0) return "";
  return "<ul class='ingredientes'>" + lista.map(i => {
    let linea = i.cantidad + " " + i.unidad + " de " + i.nombre;
    if(conReparto) linea += repartoTexto(i);
    return "<li>" + linea + "</li>";
  }).join("") + "</ul>";
}

function comidaHTML(nombreComida, comida){
  let html = "<div class='comida'><h4>" + nombreComida + "</h4>";
  if(comida.Lydia || comida.Ruben){
    ["Lydia","Ruben"].forEach(persona => {
      if(!comida[persona]) return;
      const c = comida[persona];
      html += "<div class='persona-block'><div class='persona-nombre'>" + persona + "</div>";
      html += "<div class='titulo'>" + c.titulo + "</div>";
      html += ingredientesHTML(c.base, false);
      if(c.extra_ruben && c.extra_ruben.length){
        html += "<div class='extra'><b>Extra:</b>" + ingredientesHTML(c.extra_ruben, false) + "</div>";
      }
      if(c.nota) html += "<div class='nota'>" + c.nota + "</div>";
      html += "</div>";
    });
  } else {
    if(!comida.base || comida.base.length === 0){
      html += "<p class='titulo'>" + comida.titulo + "</p>";
      if(comida.nota) html += "<p class='libre'>" + comida.nota + "</p>";
    } else {
      html += "<div class='titulo'>" + comida.titulo + "</div>";
      html += ingredientesHTML(comida.base, true);
      if(comida.extra_ruben && comida.extra_ruben.length){
        html += "<div class='extra'><b>Extra Ruben (se suma a lo de arriba):</b>" + ingredientesHTML(comida.extra_ruben, false) + "</div>";
      }
      if(comida.nota) html += "<div class='nota'>" + comida.nota + "</div>";
    }
  }
  html += "</div>";
  return html;
}

function pintarDia(){
  const cont = document.getElementById("diasContainer");
  const comidas = DATA[semanaActual].dias[diaActual];
  if(!comidas){ cont.innerHTML = ""; return; }
  const orden = ["Desayuno","Almuerzo","Comida","Merienda","Cena"];
  let html = "";
  orden.forEach(nombreComida => {
    if(comidas[nombreComida]) html += comidaHTML(nombreComida, comidas[nombreComida]);
  });
  cont.innerHTML = html;
  document.querySelectorAll("#subtabsDias button").forEach(x=>x.classList.toggle("activa", x.dataset.dia===diaActual));
}

function recolectarIngredientes(semana){
  let items = [];
  // Los ingredientes "derivados" (pollo, salmon, atun, arroz, pasta, patata, boniato...) ya se
  // cuentan a partir de las comidas del dia a dia; en los pasos de las tandas de cocinado son
  // solo informativos, para no sumarlos dos veces en la lista de la compra.
  const tandas = [semana.prep_domingo, semana.prep_miercoles].filter(Boolean);
  tandas.forEach(tanda => {
    tanda.pasos.forEach(paso => {
      items = items.concat(paso.ingredientes.filter(i => !i.derivado));
    });
  });
  Object.values(semana.dias).forEach(comidas => {
    Object.values(comidas).forEach(comida => {
      if(comida.Lydia || comida.Ruben){
        ["Lydia","Ruben"].forEach(p => {
          if(comida[p]){
            items = items.concat(comida[p].base || []);
            items = items.concat(comida[p].extra_ruben || []);
          }
        });
      } else {
        items = items.concat(comida.base || []);
        items = items.concat(comida.extra_ruben || []);
      }
    });
  });
  return items;
}

function pintarCompra(){
  const items = recolectarIngredientes(DATA[semanaActual]);
  const agg = {};
  items.forEach(it => {
    const key = it.nombre + "||" + it.unidad + "||" + it.categoria;
    if(!agg[key]) agg[key] = {nombre: it.nombre, unidad: it.unidad, categoria: it.categoria, cantidad: 0};
    agg[key].cantidad += it.cantidad;
  });
  const porCategoria = {};
  Object.values(agg).forEach(i => {
    if(i.cantidad <= 0) return;
    const cat = i.categoria || "Otros";
    if(!porCategoria[cat]) porCategoria[cat] = [];
    porCategoria[cat].push(i);
  });
  const ordenCategorias = ["Frescos: verdura y hortaliza","Fruta fresca","Carne, aves y huevos","Pescaderia",
    "Lacteos (pasteurizados)","Despensa: cereales, pan y pasta","Despensa: legumbres y conservas",
    "Frutos secos y semillas","Aceites, salsas y condimentos","Otros"];
  let html = "";
  ordenCategorias.forEach(cat => {
    if(!porCategoria[cat]) return;
    const lista = porCategoria[cat].sort((a,b)=>a.nombre.localeCompare(b.nombre));
    html += "<div class='compra-cat'><h4>" + cat + "</h4><ul>";
    lista.forEach(i => {
      const cantidad = Number.isInteger(i.cantidad) ? i.cantidad : Math.round(i.cantidad*10)/10;
      html += "<li><span>" + i.nombre + "</span><span class='cant'>" + cantidad + " " + i.unidad + "</span></li>";
    });
    html += "</ul></div>";
  });
  document.getElementById("compraContainer").innerHTML = html;
}

document.addEventListener("DOMContentLoaded", () => {
  mostrarSemana("A");
});
</script>
</body>
</html>
"""

html = TEMPLATE.replace("__DATA_JSON__", html_json).replace("__CAL_JSON__", cal_json).replace("__DIAS_JSON__", dias_json)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html generado,", len(html), "bytes")
