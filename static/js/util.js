//createElement.min.js
(function(e){var t="(-?[_a-zA-Z]+[_a-zA-Z0-9-]*)",n="^(?:"+t+")|^#"+t+"|^\\."+t+"|^\\["+t+"(?:([*$|~^]?=)([\"'])((?:(?=(\\\\?))\\8.)*?)\\6)?\\]";document.createElement=function(t){for(var r=e.call(this,"div"),i,s="";t&&(i=t.match(n));){if(i[1])r=e.call(this,i[1]);if(i[2])r.id=i[2];if(i[3])s+=" "+i[3];if(i[4])r.setAttribute(i[4],i[7]||"");t=t.slice(i[0].length)}if(s)r.className=s.slice(1);return r}})(document.createElement)


