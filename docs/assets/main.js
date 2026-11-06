(function(){"use strict";
document.documentElement.classList.add("js");
var esc=function(s){return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;")};
var R={
bash:[["c",/#.*/],["s",/"[^"\n]*"|'[^'\n]*'/],["o",/(?:^|\s)--?[A-Za-z][\w-]*/],["f",/\b(?:clight|pip|python|git|twine|cd|echo)\b/],["n",/\b\d+(?:\.\d+)*\b/]],
py:[["c",/#.*/],["s",/"""[\s\S]*?"""|"[^"\n]*"|'[^'\n]*'/],["k",/\b(?:from|import|class|def|return|if|not|pass|self|True|False|None)\b/],["f",/\b[A-Za-z_]\w*(?=\()/],["p",/\bcli\b/],["n",/\b\d+\b/]],
json:[["p",/"[^"\n]*"(?=\s*:)/],["s",/"[^"\n]*"/],["n",/-?\b\d+(?:\.\d+)?\b/],["k",/\b(?:true|false|null)\b/]],
yaml:[["c",/#.*/],["p",/^\s*-?\s*[\w.-]+(?=:)/m],["s",/"[^"\n]*"|'[^'\n]*'/],["n",/\b\d+(?:\.\d+)*\b/]],
text:[]};
var A={sh:"bash",shell:"bash",python:"py",yml:"yaml",js:"json",javascript:"json",kotlin:"text",http:"text"};
var T=function(c){return c==="x"?"x":c};
function hl(src,lang){lang=A[lang]||lang;var rules=R[lang]||[];if(!rules.length)return esc(src);
var parts=[],names=[];rules.forEach(function(r){names.push(r[0]);parts.push("("+r[1].source+")")});
var re=new RegExp(parts.join("|"),"gm"),out="",last=0,m;
while((m=re.exec(src))){if(m[0]===""){re.lastIndex++;continue}
var i=0;for(;i<names.length;i++)if(m[i+1]!==undefined)break;
out+=esc(src.slice(last,m.index))+'<span class="tok-'+T(names[i])+'">'+esc(m[0])+"</span>";last=m.index+m[0].length}
return out+esc(src.slice(last))}
function copy(t,btn){var done=function(){var o=btn.innerHTML;btn.innerHTML='<svg class="icon" aria-hidden="true"><use href="#i-check"/></svg>Copied';setTimeout(function(){btn.innerHTML=o},1800)};
if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(t).then(done,function(){fb()})}else fb();
function fb(){var a=document.createElement("textarea");a.value=t;a.style.cssText="position:fixed;opacity:0";document.body.appendChild(a);a.select();try{document.execCommand("copy")}catch(e){}a.remove();done()}}
function code(){document.querySelectorAll("pre > code").forEach(function(c){var pre=c.parentNode,raw=c.textContent.replace(/^\n/,"").replace(/\s+$/,""),lang=c.getAttribute("data-lang")||"text",title=c.getAttribute("data-title")||lang;
try{c.innerHTML=hl(raw,lang)}catch(e){c.textContent=raw}
pre.setAttribute("tabindex","0");var w=document.createElement("div");w.className="code";
w.innerHTML='<div class="code-bar"><i></i><i></i><i></i><b>'+esc(title)+'</b><button type="button" class="copy"><svg class="icon" aria-hidden="true"><use href="#i-copy"/></svg>Copy</button></div>';
pre.parentNode.insertBefore(w,pre);w.appendChild(pre);w.querySelector(".copy").addEventListener("click",function(){copy(raw,this)})})}
function menu(){var b=document.querySelector(".burger");if(!b)return;var h=document.documentElement,t=document.getElementById(b.getAttribute("aria-controls"));
function set(o){h.classList.toggle("menu-open",o);b.setAttribute("aria-expanded",o);b.setAttribute("aria-label",o?"Close menu":"Open menu");b.querySelector("use").setAttribute("href",o?"#i-x":"#i-menu")}
window.CL_closeMenu=function(){set(false)};b.addEventListener("click",function(){set(!h.classList.contains("menu-open"))});
document.addEventListener("keydown",function(e){if(e.key==="Escape")set(false)});
if(t)t.addEventListener("click",function(e){if(e.target.closest("a"))set(false)});
window.addEventListener("resize",function(){if(window.innerWidth>820)set(false)})}
function docs(){var secs=[].slice.call(document.querySelectorAll(".doc-section"));if(!secs.length)return;
var links=[].slice.call(document.querySelectorAll("[data-section]")),base=document.title.split(" | ").pop();
function show(id,push){if(!secs.some(function(s){return s.id===id}))id=secs[0].id;
secs.forEach(function(s){s.classList.toggle("active",s.id===id)});
links.forEach(function(a){if(a.getAttribute("data-section")===id)a.setAttribute("aria-current","true");else a.removeAttribute("aria-current")});
var h=document.getElementById(id).querySelector("h1");document.title=(h?h.textContent:id)+" | "+base;
if(push)history.pushState(null,"","#"+id);window.scrollTo(0,0);if(window.CL_closeMenu)window.CL_closeMenu()}
document.addEventListener("click",function(e){var a=e.target.closest("[data-section],[data-goto]");if(!a)return;e.preventDefault();show(a.getAttribute("data-section")||a.getAttribute("data-goto"),true)});
window.addEventListener("popstate",function(){show(location.hash.slice(1),false)});
show(location.hash.slice(1),false);setTimeout(function(){window.scrollTo(0,0)},0)}
document.addEventListener("DOMContentLoaded",function(){code();menu();docs()});
})();
