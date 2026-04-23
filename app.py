<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>LUMINA SOUL — ถอดรหัสพิมพ์เขียวชีวิต</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Cinzel:wght@400;600&family=Sarabun:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>
<style>
:root{
  --p:#6B2FBE;--pm:#9B59D0;--pl:#C084FC;
  --pk:#D966A8;--pkl:#F472B6;
  --deep:#1E0A3C;--txt:#2D1558;--mut:#8B6BAE;
  --gl:rgba(255,255,255,0.93);--bd:rgba(155,89,208,0.14);
  --gold:#C9A84C;--gold2:#F0D080;--gold3:#E8C040;
  --bg:linear-gradient(155deg,#EAD8FF 0%,#F3EAFF 35%,#FAF2FF 65%,#FFF5FC 100%);
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html{scroll-behavior:smooth;}
body{background:var(--bg);min-height:100vh;color:var(--txt);
  font-family:'Sarabun',sans-serif;font-weight:400;line-height:1.8;overflow-x:hidden;}
.page{display:none;}.page.active{display:block;}

/* AURA */
.aura{position:fixed;inset:0;pointer-events:none;z-index:0;overflow:hidden;}
.aura-a{position:absolute;top:-20%;left:-15%;width:70vw;height:70vw;border-radius:50%;
  background:radial-gradient(circle,rgba(168,90,255,.18) 0%,transparent 65%);animation:dA 16s ease-in-out infinite;}
.aura-b{position:absolute;bottom:-15%;right:-15%;width:60vw;height:60vw;border-radius:50%;
  background:radial-gradient(circle,rgba(217,102,168,.13) 0%,transparent 65%);animation:dB 19s ease-in-out infinite;}
@keyframes dA{0%,100%{transform:translate(0,0)}50%{transform:translate(5%,8%)}}
@keyframes dB{0%,100%{transform:translate(0,0)}50%{transform:translate(-6%,-5%)}}

/* NAV */
nav{position:fixed;top:0;left:0;right:0;z-index:200;
  padding:.72rem 1.2rem;display:flex;align-items:center;justify-content:space-between;
  background:rgba(237,224,255,.92);backdrop-filter:blur(24px);border-bottom:1px solid var(--bd);}
.nav-logo{display:flex;align-items:center;gap:.48rem;text-decoration:none;cursor:pointer;}
.logo-svg{width:30px;height:30px;filter:drop-shadow(0 0 5px rgba(155,89,208,.3));}
.logo-text{font-family:'Cinzel',serif;font-size:.82rem;font-weight:600;letter-spacing:.13em;
  background:linear-gradient(135deg,var(--p),var(--pm),var(--pk));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.nav-right{display:flex;align-items:center;gap:.38rem;}
.lang-toggle{display:flex;background:rgba(255,255,255,.55);border-radius:100px;border:1px solid var(--bd);overflow:hidden;}
.lang-btn{padding:.24rem .6rem;font-size:.68rem;font-weight:600;color:var(--mut);background:none;border:none;cursor:pointer;transition:all .2s;}
.lang-btn.active{background:linear-gradient(135deg,var(--pm),var(--pk));color:#fff;}
.nav-line{display:flex;align-items:center;gap:.28rem;padding:.24rem .72rem;border-radius:100px;
  background:linear-gradient(135deg,#06C755,#04A844);color:#fff;font-size:.68rem;font-weight:700;
  text-decoration:none;box-shadow:0 2px 8px rgba(6,199,85,.22);transition:all .3s;}
.nav-line:hover{transform:translateY(-1px);}
.line-ico{width:12px;height:12px;}

/* SHARED */
section{position:relative;z-index:1;}
.container{max-width:800px;margin:0 auto;padding:0 1.1rem;}
.div{position:relative;z-index:1;text-align:center;color:rgba(168,90,255,.22);font-size:.75rem;letter-spacing:.5em;padding:.4rem 0;}
.s-lbl{font-family:'Cinzel',serif;font-size:.55rem;letter-spacing:.24em;color:var(--pl);text-transform:uppercase;text-align:center;margin-bottom:.4rem;}
.s-ttl{font-family:'Cormorant Garamond',serif;font-size:clamp(1.4rem,4.5vw,2.3rem);font-weight:300;text-align:center;color:var(--deep);margin-bottom:.5rem;line-height:1.2;}
.s-ttl em{font-style:italic;background:linear-gradient(135deg,var(--p),var(--pk));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.s-sub{text-align:center;color:var(--mut);font-size:.84rem;max-width:460px;margin:0 auto 1.8rem;line-height:1.8;}
.rev{opacity:0;transform:translateY(16px);transition:opacity .58s,transform .58s;}
.rev.in{opacity:1;transform:none;}

/* ══════════ PAGE 1 ══════════ */
.hero{position:relative;z-index:1;text-align:center;padding:5rem 1.2rem 0;}
.compass-wrap{display:flex;justify-content:center;margin-bottom:.8rem;}
.compass-hero{width:78px;height:78px;
  filter:drop-shadow(0 0 14px rgba(155,89,208,.42)) drop-shadow(0 0 5px rgba(217,102,168,.28));
  animation:float-c 5s ease-in-out infinite;}
@keyframes float-c{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}

.hero-eyebrow{font-family:'Cinzel',serif;font-size:.55rem;letter-spacing:.34em;color:var(--pl);text-transform:uppercase;margin-bottom:.45rem;display:block;}
.hero-h1{
  font-family:'Sarabun',sans-serif;font-size:clamp(2.3rem,9vw,4.4rem);font-weight:700;
  line-height:1.05;letter-spacing:-.01em;margin-bottom:.28rem;
  background:linear-gradient(270deg,#9B59D0,#D966A8,#C084FC,#7B3FBE,#F472B6,#9B59D0);
  background-size:300% 300%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  animation:gradShift 4s ease-in-out infinite;}
@keyframes gradShift{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
.hero-sub-en{font-family:'Cinzel',serif;font-size:.56rem;letter-spacing:.18em;color:var(--pl);text-transform:uppercase;margin-bottom:.32rem;display:block;}
.hero-tagline{font-size:clamp(.84rem,2vw,.94rem);color:var(--p);font-weight:600;margin-bottom:.28rem;}
.hero-desc{font-size:clamp(.75rem,1.6vw,.84rem);color:var(--mut);max-width:320px;margin:0 auto .78rem;line-height:1.8;}

.pain-card{background:var(--gl);border:1.5px solid rgba(168,90,255,.16);border-radius:18px;
  padding:1.1rem 1.3rem;max-width:480px;margin:0 auto .72rem;
  box-shadow:0 5px 18px rgba(120,60,200,.08);position:relative;overflow:hidden;}
.pain-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;
  background:linear-gradient(90deg,var(--p),var(--pm),var(--pk),var(--gold));}
.pain-line{font-size:clamp(.83rem,1.9vw,.95rem);color:var(--deep);line-height:1.9;}
.pain-line strong{background:linear-gradient(135deg,var(--p),var(--pk));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;font-weight:700;}
.pain-em{font-family:'Cormorant Garamond',serif;font-size:clamp(.95rem,2.3vw,1.2rem);font-style:italic;color:var(--p);margin-top:.5rem;display:block;line-height:1.4;}
.know-strip{display:flex;flex-wrap:wrap;justify-content:center;gap:.3rem;margin-bottom:.6rem;}
.know-tag{background:var(--gl);border:1px solid rgba(168,90,255,.14);border-radius:100px;padding:.17rem .64rem;font-size:.68rem;color:var(--p);font-weight:500;}
.urgency{display:inline-flex;align-items:center;gap:.34rem;font-size:.67rem;color:var(--mut);}
.u-dot{width:5px;height:5px;border-radius:50%;background:#9B59D0;animation:blink 2s ease-in-out infinite;flex-shrink:0;}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}

/* FORM */
.form-section{padding:1.3rem 0 1.8rem;}
.form-above{text-align:center;margin-bottom:.8rem;}
.form-above-title{font-family:'Cormorant Garamond',serif;font-size:clamp(1.25rem,3.6vw,1.9rem);font-weight:300;color:var(--deep);margin-bottom:.18rem;}
.form-above-title em{font-style:italic;background:linear-gradient(135deg,var(--p),var(--pk));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.form-above-sub{font-size:.77rem;color:var(--mut);line-height:1.7;}
.form-card{background:rgba(255,255,255,.94);border:1.5px solid rgba(192,132,252,.2);
  border-radius:22px;padding:1.8rem 1.5rem;max-width:600px;margin:0 auto;
  box-shadow:0 16px 46px rgba(110,50,200,.09),inset 0 1px 0 rgba(255,255,255,.9);
  position:relative;overflow:hidden;}
.form-card::before{content:'';position:absolute;top:0;left:0;right:0;height:4px;
  background:linear-gradient(90deg,var(--p),var(--pm),var(--pk),var(--gold),var(--pk),var(--pm));
  background-size:200% 100%;animation:shimmer 4s linear infinite;}
@keyframes shimmer{0%{background-position:0%}100%{background-position:200%}}
.form-title{font-family:'Cormorant Garamond',serif;font-size:1.28rem;font-weight:400;color:var(--deep);text-align:center;margin-bottom:.18rem;}
.form-sub{text-align:center;font-size:.7rem;color:var(--mut);margin-bottom:1.3rem;}
.field{display:flex;flex-direction:column;gap:.24rem;margin-bottom:.7rem;}
.field label{font-size:.67rem;font-weight:600;color:var(--p);letter-spacing:.04em;}
.field input,.field select,.field textarea{
  padding:.57rem .85rem;border:1.5px solid rgba(192,132,252,.18);border-radius:10px;
  font-family:'Sarabun',sans-serif;font-size:.87rem;color:var(--txt);
  background:rgba(250,245,255,.6);outline:none;width:100%;
  transition:border-color .22s,box-shadow .22s,transform .14s;}
.field input:focus,.field select:focus,.field textarea:focus{
  border-color:var(--pl);box-shadow:0 0 0 3px rgba(192,132,252,.1);
  background:rgba(255,255,255,.96);transform:translateY(-1px);}
.field textarea{resize:vertical;min-height:74px;}
.field select{appearance:none;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='11' height='7'%3E%3Cpath d='M1 1l4.5 4.5L10 1' stroke='%239B59D0' stroke-width='1.4' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");
  background-repeat:no-repeat;background-position:right .8rem center;padding-right:1.85rem;cursor:pointer;}
.birth-row{display:grid;grid-template-columns:68px 1fr 88px;gap:.48rem;}
.opt-box{border:1.5px dashed rgba(192,132,252,.24);border-radius:12px;padding:.7rem .85rem;margin-bottom:.7rem;}
.opt-label{font-size:.63rem;font-weight:600;color:var(--pl);margin-bottom:.48rem;display:flex;align-items:center;gap:.26rem;}
.half-row{display:grid;grid-template-columns:1fr 1fr;gap:.48rem;}
.half-row .field input{min-width:0;}
.pills{display:flex;flex-wrap:wrap;gap:.3rem;}
.pi{display:none;}
.pl-lb{padding:.22rem .72rem;border-radius:100px;border:1.5px solid rgba(192,132,252,.2);font-size:.7rem;color:var(--mut);cursor:pointer;transition:all .2s;background:rgba(250,245,255,.68);}
.pi:checked+.pl-lb{background:linear-gradient(135deg,var(--pm),var(--pk));color:#fff;border-color:transparent;box-shadow:0 3px 10px rgba(155,89,208,.24);}
.pl-lb:hover{border-color:var(--pl);color:var(--p);}

/* GOLD SUBMIT */
.submit-btn{width:100%;padding:.9rem;border:none;border-radius:100px;margin-top:.42rem;
  background:linear-gradient(135deg,#B8900A 0%,#E8C040 30%,#F5D870 50%,#E8C040 70%,#B8900A 100%);
  background-size:200% 100%;color:#3A2000;font-family:'Sarabun',sans-serif;font-size:.95rem;font-weight:700;
  letter-spacing:.05em;cursor:pointer;position:relative;overflow:hidden;
  box-shadow:0 8px 22px rgba(184,144,10,.32);animation:goldShift 3s ease-in-out infinite;transition:transform .3s;}
@keyframes goldShift{0%,100%{background-position:0% 50%}50%{background-position:100% 50%;box-shadow:0 12px 28px rgba(184,144,10,.46)}}
.submit-btn::before{content:'';position:absolute;inset:0;background:linear-gradient(135deg,rgba(255,255,255,.22),transparent 50%);border-radius:100px;pointer-events:none;}
.submit-btn:hover:not(:disabled){transform:translateY(-2px);}
.submit-btn:disabled{opacity:.5;cursor:not-allowed;animation:none;}
.demo-btn{display:block;width:100%;margin-top:.5rem;padding:.46rem;border-radius:100px;
  border:1.5px dashed rgba(155,89,208,.26);background:transparent;color:var(--mut);
  font-family:'Sarabun',sans-serif;font-size:.74rem;cursor:pointer;transition:all .24s;}
.demo-btn:hover{border-color:var(--pl);color:var(--p);}

/* LOADING */
#loading-state{display:none;text-align:center;padding:2.6rem 1rem;max-width:600px;margin:0 auto;}
.spin-wrap{position:relative;width:60px;height:60px;margin:0 auto 1.1rem;}
.spin-o{width:60px;height:60px;border-radius:50%;border:3px solid transparent;border-top-color:var(--pm);border-right-color:var(--pk);animation:spin 1.2s linear infinite;position:absolute;}
.spin-i{width:38px;height:38px;border-radius:50%;border:2px solid transparent;border-bottom-color:var(--pl);border-left-color:var(--gold);animation:spin 1.9s linear infinite reverse;position:absolute;top:11px;left:11px;}
@keyframes spin{to{transform:rotate(360deg)}}
.load-steps{list-style:none;margin-top:.5rem;}
.ls{font-size:.76rem;color:var(--mut);padding:.14rem 0;opacity:.28;transition:opacity .4s,color .4s;}
.ls.active{opacity:1;color:var(--p);font-weight:600;}
.ls.done{opacity:.5;text-decoration:line-through;}
.ls.active::before{content:'→ ';}
.ls.done::before{content:'✓ ';}

/* BENEFIT CARDS */
.benefits{padding:2rem 0;}
.bc-list{display:flex;flex-direction:column;gap:.55rem;}
.bc{background:rgba(255,255,255,.85);border:1px solid rgba(192,132,252,.15);border-radius:13px;padding:.75rem .95rem;display:flex;align-items:center;gap:.75rem;transition:all .22s;}
.bc:hover{transform:translateX(3px);box-shadow:0 4px 14px rgba(120,60,200,.07);}
.bc-icon{font-size:1.35rem;flex-shrink:0;width:36px;height:36px;background:rgba(240,230,255,.7);border-radius:9px;display:flex;align-items:center;justify-content:center;}
.bc-title{font-size:.82rem;font-weight:700;color:var(--deep);margin-bottom:.05rem;}
.bc-desc{font-size:.69rem;color:var(--mut);line-height:1.5;}

/* FREE GIFTS SECTION */
.free-section{padding:2rem 0;}
.free-grid{display:grid;grid-template-columns:1fr 1fr;gap:.7rem;}
@media(max-width:480px){.free-grid{grid-template-columns:1fr;}}
.free-card{background:rgba(255,255,255,.88);border:1px solid rgba(201,168,76,.22);border-radius:14px;padding:1rem 1.1rem;position:relative;overflow:hidden;}
.free-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2.5px;
  background:linear-gradient(90deg,var(--gold),var(--gold2),var(--gold));}
.free-icon{font-size:1.2rem;margin-bottom:.35rem;display:block;}
.free-title{font-size:.82rem;font-weight:700;color:var(--deep);margin-bottom:.15rem;}
.free-desc{font-size:.7rem;color:var(--mut);line-height:1.55;}
.free-note{text-align:center;margin-top:1.2rem;font-size:.8rem;color:var(--p);font-weight:600;}
.free-note em{font-style:normal;
  background:linear-gradient(135deg,var(--gold),var(--gold2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}

/* WHY */
.why{padding:1.8rem 0;}
.wc-list{display:flex;flex-direction:column;gap:.55rem;}
.wc{background:rgba(255,255,255,.85);border:1px solid var(--bd);border-radius:13px;padding:.72rem .95rem;display:flex;align-items:flex-start;gap:.72rem;}
.wc-icon{font-size:1.25rem;flex-shrink:0;margin-top:.04rem;}
.wc-title{font-size:.8rem;font-weight:700;color:var(--deep);margin-bottom:.06rem;}
.wc-text{font-size:.68rem;color:var(--mut);line-height:1.55;}

/* PROOF */
.proof{background:linear-gradient(135deg,rgba(155,89,208,.06),rgba(217,102,168,.04));border:1px solid rgba(155,89,208,.13);border-radius:13px;padding:1rem 1.2rem;margin-top:1.1rem;position:relative;overflow:hidden;}
.proof::before{content:'"';position:absolute;top:-.55rem;left:.45rem;font-family:'Cormorant Garamond',serif;font-size:5rem;color:rgba(155,89,208,.09);line-height:1;pointer-events:none;}
.proof-txt{font-size:.78rem;color:#4A2E78;line-height:1.85;font-style:italic;position:relative;z-index:1;}
.proof-cut{display:inline-block;background:rgba(155,89,208,.11);border-radius:4px;padding:.07rem .38rem;font-style:normal;font-size:.69rem;color:var(--p);font-weight:700;margin-top:.28rem;}
.proof-by{font-size:.65rem;color:var(--mut);margin-top:.58rem;}

/* REVIEWS */
.reviews{padding:2rem 0;}
.rv-list{display:flex;flex-direction:column;gap:.62rem;}
.rv{background:rgba(255,255,255,.88);border:1px solid rgba(217,102,168,.16);border-radius:13px;padding:.9rem 1rem;}
.rv-stars{color:var(--pk);font-size:.73rem;letter-spacing:.06em;margin-bottom:.35rem;}
.rv-story{font-size:.76rem;color:#4A2E78;line-height:1.72;margin-bottom:.58rem;}
.rv-story strong{color:var(--p);font-weight:700;}
.rv-author{display:flex;align-items:center;gap:.48rem;}
.rv-av{width:26px;height:26px;border-radius:50%;flex-shrink:0;background:linear-gradient(135deg,var(--pl),var(--pkl));display:flex;align-items:center;justify-content:center;font-size:.67rem;color:#fff;font-weight:700;}
.rv-name{font-size:.71rem;font-weight:700;color:var(--deep);}
.rv-meta{font-size:.62rem;color:var(--mut);}

footer{position:relative;z-index:1;text-align:center;padding:1.6rem 1rem;border-top:1px solid var(--bd);}
.ft-logo{font-family:'Cinzel',serif;font-size:.82rem;letter-spacing:.2em;background:linear-gradient(135deg,var(--p),var(--pk));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:.28rem;}
.ft-sub{font-size:.64rem;color:var(--mut);margin-bottom:.85rem;}
.ft-links{display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;}
.ft-links a{font-size:.63rem;color:var(--mut);text-decoration:none;}
.ft-links a:hover{color:var(--pm);}

/* ══════════ PAGE 2 ══════════ */
#page-result{min-height:100vh;}
.result-body{position:relative;z-index:1;max-width:580px;margin:0 auto;padding:4.8rem 1.2rem 3rem;}

/* USER HEADER */
.uh{text-align:center;margin-bottom:1.8rem;}
.uh-badge{display:inline-block;padding:.2rem .88rem;border-radius:100px;
  background:linear-gradient(135deg,rgba(192,132,252,.15),rgba(240,168,216,.11));
  border:1px solid rgba(192,132,252,.26);font-size:.6rem;color:var(--pm);
  letter-spacing:.1em;font-family:'Cinzel',serif;margin-bottom:.6rem;}
.uh-name{font-family:'Cormorant Garamond',serif;font-size:clamp(1.55rem,5vw,2.1rem);font-weight:300;color:var(--deep);margin-bottom:.28rem;}
.uh-name em{font-style:italic;background:linear-gradient(135deg,var(--p),var(--pk));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.uh-key{font-size:.7rem;color:var(--mut);letter-spacing:.05em;}

/* MANDALA — purple/pink/gold only */
.mandala-section{margin-bottom:1.6rem;text-align:center;}
canvas#mandala-c{border-radius:50%;
  filter:drop-shadow(0 0 20px rgba(155,89,208,.32)) drop-shadow(0 0 8px rgba(201,168,76,.2));}
.mandala-caption{font-family:'Cinzel',serif;font-size:.54rem;letter-spacing:.18em;color:var(--pl);text-transform:uppercase;margin-top:.5rem;}

/* KEY NUMBERS */
.key-nums{display:grid;grid-template-columns:repeat(3,1fr);gap:.65rem;margin-bottom:1.6rem;}
.kn{background:rgba(255,255,255,.92);border:1px solid var(--bd);border-radius:14px;padding:.75rem .55rem;text-align:center;transition:all .22s;}
.kn:hover{transform:translateY(-2px);box-shadow:0 5px 16px rgba(155,89,208,.1);}
.kn-val{font-family:'Cormorant Garamond',serif;font-size:1.9rem;font-weight:600;line-height:1;
  background:linear-gradient(135deg,var(--p),var(--pk));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:.15rem;}
.kn-title{font-size:.6rem;color:var(--deep);font-weight:700;margin-bottom:.06rem;}
.kn-sub{font-size:.58rem;color:var(--mut);line-height:1.4;}

/* PREVIEW */
.preview-section{margin-bottom:1.5rem;}
.preview-label{font-family:'Cinzel',serif;font-size:.54rem;letter-spacing:.2em;color:var(--pl);text-transform:uppercase;margin-bottom:.75rem;display:block;}
.preview-card{background:rgba(255,255,255,.92);border:1px solid rgba(192,132,252,.18);border-radius:18px;padding:1.5rem 1.35rem;position:relative;overflow:hidden;}
.preview-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;
  background:linear-gradient(90deg,var(--p),var(--pm),var(--pk));}
.pb{margin-bottom:1rem;}
.pb:last-child{margin-bottom:0;}
.pb-icon{font-size:1rem;margin-bottom:.26rem;display:block;}
.pb-heading{font-family:'Cormorant Garamond',serif;font-size:1.08rem;font-weight:600;color:var(--deep);margin-bottom:.35rem;line-height:1.3;}
.pb-text{font-size:.87rem;color:#3E2068;line-height:1.95;}
.pb-sep{border:none;border-top:1px solid rgba(192,132,252,.1);margin:.9rem 0;}

/* fade subtle */
.preview-fade{position:relative;}
.preview-fade::after{content:'';position:absolute;bottom:0;left:0;right:0;height:80px;
  background:linear-gradient(transparent,rgba(255,255,255,.95));pointer-events:none;}
.preview-more{text-align:center;font-size:.7rem;color:rgba(139,107,174,.55);font-style:italic;margin:.35rem 0 1.3rem;letter-spacing:.02em;}

/* HOOK BEFORE PAYWALL */
.hook-box{background:linear-gradient(135deg,rgba(107,47,190,.05),rgba(217,102,168,.04));
  border:1px solid rgba(155,89,208,.14);border-radius:14px;padding:1.2rem 1.3rem;margin-bottom:1.4rem;}
.hook-title{font-family:'Cormorant Garamond',serif;font-size:1rem;font-weight:600;color:var(--deep);margin-bottom:.7rem;text-align:center;}
.hook-pct{text-align:center;font-size:.78rem;color:var(--p);font-weight:600;margin-bottom:.8rem;}
.hook-list{list-style:none;display:flex;flex-direction:column;gap:.4rem;}
.hook-list li{display:flex;align-items:flex-start;gap:.5rem;font-size:.8rem;color:var(--txt);line-height:1.55;}
.hook-list li::before{content:'✦';color:var(--pk);font-size:.58rem;flex-shrink:0;margin-top:.18rem;}

/* PAYWALL */
.paywall-card{background:linear-gradient(145deg,rgba(107,47,190,.06),rgba(217,102,168,.05));
  border:1.5px solid rgba(155,89,208,.26);border-radius:22px;
  padding:1.7rem 1.4rem;text-align:center;margin-bottom:.8rem;position:relative;overflow:hidden;}
.paywall-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;
  background:linear-gradient(90deg,var(--p),var(--pm),var(--pk),var(--gold));}
.pw-lock{font-size:1.9rem;margin-bottom:.45rem;}
.pw-title{font-family:'Cormorant Garamond',serif;font-size:1.35rem;font-weight:500;color:var(--deep);margin-bottom:.28rem;}
.pw-sub{font-size:.8rem;color:var(--mut);margin-bottom:1.1rem;line-height:1.65;}
.pw-price{font-family:'Cormorant Garamond',serif;font-size:2.5rem;font-weight:600;
  background:linear-gradient(135deg,var(--gold),var(--gold2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1;margin-bottom:.18rem;}
.pw-price-note{font-size:.7rem;color:var(--mut);margin-bottom:1.1rem;}
.pw-close{font-family:'Cormorant Garamond',serif;font-size:.95rem;font-style:italic;color:var(--p);margin-top:1.1rem;margin-bottom:.7rem;line-height:1.55;}
.pw-feats{list-style:none;text-align:left;margin-bottom:1.2rem;display:flex;flex-direction:column;gap:.42rem;}
.pw-feats li{display:flex;align-items:flex-start;gap:.48rem;font-size:.79rem;color:var(--txt);line-height:1.55;}
.pw-feats li::before{content:'✦';color:var(--pk);font-size:.58rem;flex-shrink:0;margin-top:.18rem;}

/* PREMIUM CTA BUTTON — animated shimmer glow */
.cta-btn{display:block;width:100%;padding:1rem;border:none;border-radius:100px;cursor:pointer;
  font-family:'Sarabun',sans-serif;font-size:.98rem;font-weight:700;letter-spacing:.04em;
  text-decoration:none;text-align:center;color:#fff;position:relative;overflow:hidden;
  background:linear-gradient(135deg,var(--p) 0%,var(--pm) 40%,var(--pk) 70%,var(--pm) 100%);
  background-size:200% 200%;
  animation:ctaGlow 3s ease-in-out infinite;
  transition:transform .3s;}
.cta-btn::before{content:'';position:absolute;inset:0;border-radius:100px;
  background:linear-gradient(135deg,rgba(255,255,255,.22) 0%,transparent 50%,rgba(255,255,255,.08) 100%);
  pointer-events:none;}
.cta-btn::after{content:'';position:absolute;top:-50%;left:-60%;width:40%;height:200%;
  background:rgba(255,255,255,.15);transform:skewX(-20deg);
  animation:swipe 3s ease-in-out infinite 1.5s;}
@keyframes ctaGlow{
  0%,100%{background-position:0% 50%;box-shadow:0 8px 24px rgba(107,47,190,.38),0 0 0 0 rgba(155,89,208,.2)}
  50%{background-position:100% 50%;box-shadow:0 12px 32px rgba(107,47,190,.55),0 0 0 8px rgba(155,89,208,.08)}
}
@keyframes swipe{0%{left:-60%}100%{left:120%}}
.cta-btn:hover{transform:translateY(-2px);}
.cta-note{font-size:.67rem;color:var(--mut);margin-top:.5rem;}

.back-btn{display:block;text-align:center;margin-top:.85rem;background:none;border:none;
  color:var(--mut);font-size:.72rem;cursor:pointer;text-decoration:underline;font-family:'Sarabun',sans-serif;}
</style>
</head>
<body>
<div class="aura"><div class="aura-a"></div><div class="aura-b"></div></div>

<!-- NAV -->
<nav>
  <div class="nav-logo" onclick="goHome()">
    <svg class="logo-svg" viewBox="0 0 40 40" fill="none">
      <circle cx="20" cy="20" r="18.5" stroke="url(#cg1)" stroke-width="1.3" opacity=".72"/>
      <circle cx="20" cy="20" r="12" stroke="url(#cg1)" stroke-width="1"/>
      <circle cx="20" cy="20" r="5.5" stroke="url(#cg1)" stroke-width=".8" opacity=".8"/>
      <line x1="20" y1="1.5" x2="20" y2="38.5" stroke="url(#cg1)" stroke-width=".7" opacity=".38"/>
      <line x1="1.5" y1="20" x2="38.5" y2="20" stroke="url(#cg1)" stroke-width=".7" opacity=".38"/>
      <line x1="7" y1="7" x2="33" y2="33" stroke="url(#cg1)" stroke-width=".6" opacity=".25"/>
      <line x1="33" y1="7" x2="7" y2="33" stroke="url(#cg1)" stroke-width=".6" opacity=".25"/>
      <polygon points="20,2 22,20 20,18 18,20" fill="url(#cg1)" opacity=".92"/>
      <polygon points="20,38 18,20 20,22 22,20" fill="url(#cg2)" opacity=".82"/>
      <circle cx="20" cy="1.5" r="1.7" fill="url(#cg1)"/>
      <circle cx="38.5" cy="20" r="1.7" fill="url(#cg1)"/>
      <circle cx="20" cy="38.5" r="1.7" fill="url(#cg2)"/>
      <circle cx="1.5" cy="20" r="1.7" fill="url(#cg2)"/>
      <circle cx="20" cy="20" r="2.6" fill="url(#cg3)"/>
      <circle cx="20" cy="20" r="1.1" fill="white" opacity=".88"/>
      <defs>
        <linearGradient id="cg1" x1="0" y1="0" x2="40" y2="40" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stop-color="#9B59D0"/><stop offset="100%" stop-color="#C084FC"/>
        </linearGradient>
        <linearGradient id="cg2" x1="0" y1="0" x2="40" y2="40" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stop-color="#D966A8"/><stop offset="100%" stop-color="#F472B6"/>
        </linearGradient>
        <radialGradient id="cg3" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#C9A84C"/><stop offset="100%" stop-color="#9B59D0"/>
        </radialGradient>
      </defs>
    </svg>
    <span class="logo-text">LUMINA SOUL</span>
  </div>
  <div class="nav-right">
    <div class="lang-toggle">
      <button class="lang-btn active" onclick="setLang('th')" id="btn-th">TH</button>
      <button class="lang-btn" onclick="setLang('en')" id="btn-en">EN</button>
    </div>
    <a href="https://lin.ee/sjS20F8" class="nav-line" target="_blank">
      <svg class="line-ico" viewBox="0 0 24 24" fill="white"><path d="M19.365 9.863c.349 0 .63.285.63.631 0 .345-.281.63-.63.63H17.61v1.125h1.755c.349 0 .63.283.63.63 0 .344-.281.629-.63.629h-2.386c-.345 0-.627-.285-.627-.629V8.108c0-.345.282-.63.63-.63h2.386c.346 0 .627.285.627.63 0 .349-.281.63-.63.63H17.61v1.125h1.755zm-3.855 3.016c0 .27-.174.51-.432.596-.064.021-.133.031-.199.031-.211 0-.391-.09-.51-.25l-2.443-3.317v2.94c0 .344-.279.629-.631.629-.346 0-.626-.285-.626-.629V8.108c0-.27.173-.51.43-.595.06-.023.136-.033.194-.033.195 0 .375.104.495.254l2.462 3.33V8.108c0-.345.282-.63.63-.63.345 0 .63.285.63.63v4.771zm-5.741 0c0 .344-.282.629-.631.629-.345 0-.627-.285-.627-.629V8.108c0-.345.282-.63.63-.63.346 0 .628.285.628.63v4.771zm-2.466.629H4.917c-.345 0-.63-.285-.63-.629V8.108c0-.345.285-.63.63-.63.348 0 .63.285.63.63v4.141h1.756c.348 0 .629.283.629.63 0 .344-.281.629-.629.629M24 10.314C24 4.943 18.615.572 12 .572S0 4.943 0 10.314c0 4.811 4.27 8.842 10.035 9.608.391.082.923.258 1.058.59.12.301.079.766.038 1.08l-.164 1.02c-.045.301-.24 1.186 1.049.645 1.291-.539 6.916-4.078 9.436-6.975C23.176 14.393 24 12.458 24 10.314"/></svg>
      LINE
    </a>
  </div>
</nav>

<!-- ══════════ PAGE 1 ══════════ -->
<div id="page-form" class="page active">

<section class="hero">
  <div class="compass-wrap">
    <svg class="compass-hero" viewBox="0 0 100 100" fill="none">
      <circle cx="50" cy="50" r="47" stroke="url(#hg1)" stroke-width="1.3" opacity=".55"/>
      <circle cx="50" cy="50" r="36" stroke="url(#hg1)" stroke-width="1.1" opacity=".72"/>
      <circle cx="50" cy="50" r="24" stroke="url(#hg1)" stroke-width="1" opacity=".85"/>
      <circle cx="50" cy="50" r="12" stroke="url(#hg2)" stroke-width="1" opacity=".9"/>
      <line x1="50" y1="3" x2="50" y2="97" stroke="url(#hg1)" stroke-width=".75" opacity=".35"/>
      <line x1="3" y1="50" x2="97" y2="50" stroke="url(#hg1)" stroke-width=".75" opacity=".35"/>
      <line x1="16" y1="16" x2="84" y2="84" stroke="url(#hg1)" stroke-width=".65" opacity=".22"/>
      <line x1="84" y1="16" x2="16" y2="84" stroke="url(#hg1)" stroke-width=".65" opacity=".22"/>
      <polygon points="50,4 54,50 50,44 46,50" fill="url(#hg1)" opacity=".95"/>
      <polygon points="50,96 46,50 50,56 54,50" fill="url(#hg2)" opacity=".88"/>
      <polygon points="96,50 88,47 88,53" fill="url(#hg1)" opacity=".65"/>
      <polygon points="4,50 12,47 12,53" fill="url(#hg2)" opacity=".65"/>
      <circle cx="83" cy="17" r="2" fill="url(#hg2)" opacity=".58"/>
      <circle cx="17" cy="83" r="2" fill="url(#hg1)" opacity=".58"/>
      <circle cx="83" cy="83" r="2" fill="url(#hg2)" opacity=".58"/>
      <circle cx="17" cy="17" r="2" fill="url(#hg1)" opacity=".58"/>
      <circle cx="50" cy="50" r="5" fill="url(#hg3)"/>
      <circle cx="50" cy="50" r="2.2" fill="white" opacity=".88"/>
      <defs>
        <linearGradient id="hg1" x1="0" y1="0" x2="100" y2="100" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stop-color="#9B59D0"/><stop offset="100%" stop-color="#C084FC"/>
        </linearGradient>
        <linearGradient id="hg2" x1="0" y1="0" x2="100" y2="100" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stop-color="#D966A8"/><stop offset="100%" stop-color="#F472B6"/>
        </linearGradient>
        <radialGradient id="hg3" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#C9A84C"/><stop offset="60%" stop-color="#9B59D0"/>
        </radialGradient>
      </defs>
    </svg>
  </div>
  <span class="hero-eyebrow" data-th="DECODE YOUR COSMIC BLUEPRINT" data-en="DECODE YOUR COSMIC BLUEPRINT">DECODE YOUR COSMIC BLUEPRINT</span>
  <h1 class="hero-h1" data-th="พิมพ์เขียวชีวิต" data-en="Life Blueprint">พิมพ์เขียวชีวิต</h1>
  <span class="hero-sub-en" data-th="คุณเกิดมาทำอะไร? จักรวาลมีคำตอบ" data-en="Why were you born? The universe has the answer">คุณเกิดมาทำอะไร? จักรวาลมีคำตอบ</span>
  <p class="hero-desc" data-th="โหราศาสตร์ · พลังงาน · จิตวิญญาณ · การสะท้อนชีวิตเฉพาะคุณ" data-en="Astrology · Energy · Spirituality · Your personal life reflection">โหราศาสตร์ · พลังงาน · จิตวิญญาณ · การสะท้อนชีวิตเฉพาะคุณ</p>

  <div class="pain-card rev">
    <p class="pain-line" data-th="คุณพยายามเปลี่ยนแล้ว<br>แต่ชีวิต<strong>ยังวนอยู่ที่เดิม</strong><br>เรื่องเดิม คนเดิม ความรู้สึกเดิม<br>แม้แต่ตัวเองก็ยังไม่เข้าใจว่าทำไม" data-en="You've tried to change<br>But life keeps <strong>repeating the same loop</strong><br>Same patterns, same feelings, same results<br>And you still can't figure out why">คุณพยายามเปลี่ยนแล้ว<br>แต่ชีวิต<strong>ยังวนอยู่ที่เดิม</strong><br>เรื่องเดิม คนเดิม ความรู้สึกเดิม<br>แม้แต่ตัวเองก็ยังไม่เข้าใจว่าทำไม</p>
    <em class="pain-em" data-th="นั่นไม่ใช่ความผิดพลาด — มันคือสัญญาณที่รอให้คุณอ่านออก" data-en="That's not failure — it's a signal waiting to be decoded">นั่นไม่ใช่ความผิดพลาด — มันคือสัญญาณที่รอให้คุณอ่านออก</em>
  </div>
  <div class="know-strip">
    <span class="know-tag" data-th="🔄 loop ที่ติดอยู่" data-en="🔄 Your stuck loop">🔄 loop ที่ติดอยู่</span>
    <span class="know-tag" data-th="🔥 พลังที่กดไว้" data-en="🔥 Suppressed power">🔥 พลังที่กดไว้</span>
    <span class="know-tag" data-th="💞 ความสัมพันธ์สะท้อนอะไร" data-en="💞 What relationships mirror">💞 ความสัมพันธ์สะท้อนอะไร</span>
    <span class="know-tag" data-th="🌀 ภารกิจชีวิต" data-en="🌀 Life mission">🌀 ภารกิจชีวิต</span>
  </div>
  <div class="urgency">
    <span class="u-dot"></span>
    <span data-th="ระบบกำลังเปิดให้ใช้งาน · ไม่ใช่ instant tool ธรรมดา" data-en="System live · Not your average instant tool">ระบบกำลังเปิดให้ใช้งาน · ไม่ใช่ instant tool ธรรมดา</span>
  </div>
</section>

<div class="div">✦ ✦ ✦</div>

<!-- FORM -->
<section class="form-section" id="form-section">
  <div class="container">
    <div class="form-above rev">
      <h2 class="form-above-title"><em data-th="เริ่มถอดรหัสชีวิตของคุณ" data-en="Start Decoding Your Life">เริ่มถอดรหัสชีวิตของคุณ</em></h2>
      <p class="form-above-sub" data-th="ใช้เวลาไม่ถึง 1 นาที · คุณจะเห็นสิ่งที่ไม่เคยเห็นมาก่อน" data-en="Under 1 minute · You'll see what you've never seen before">ใช้เวลาไม่ถึง 1 นาที · คุณจะเห็นสิ่งที่ไม่เคยเห็นมาก่อน</p>
    </div>
    <div class="form-card rev" id="form-state">
      <h3 class="form-title" data-th="✦ พิมพ์เขียวชีวิตของคุณ" data-en="✦ Your Life Blueprint">✦ พิมพ์เขียวชีวิตของคุณ</h3>
      <p class="form-sub" data-th="ข้อมูลใช้เพื่อวิเคราะห์เท่านั้น · ปลอดภัย 100%" data-en="For analysis only · 100% secure">ข้อมูลใช้เพื่อวิเคราะห์เท่านั้น · ปลอดภัย 100%</p>
      <div class="field"><label data-th="ชื่อ" data-en="Name">ชื่อ</label><input type="text" id="f-name" placeholder="เช่น เอ็ม, มินตรา"/></div>
      <div class="field"><label>Line ID</label><input type="text" id="f-line" placeholder="@yourlineid"/></div>
      <div class="field">
        <label data-th="วันเกิด" data-en="Date of Birth">วันเกิด</label>
        <div class="birth-row">
          <input type="number" id="f-day" placeholder="วัน" min="1" max="31"/>
          <select id="f-month">
            <option value="">เดือน</option>
            <option value="1">มกราคม</option><option value="2">กุมภาพันธ์</option>
            <option value="3">มีนาคม</option><option value="4">เมษายน</option>
            <option value="5">พฤษภาคม</option><option value="6">มิถุนายน</option>
            <option value="7">กรกฎาคม</option><option value="8">สิงหาคม</option>
            <option value="9">กันยายน</option><option value="10">ตุลาคม</option>
            <option value="11">พฤศจิกายน</option><option value="12">ธันวาคม</option>
          </select>
          <input type="number" id="f-year" placeholder="ปี พ.ศ."/>
        </div>
      </div>
      <div class="opt-box">
        <div class="opt-label">⚡ <span data-th="เพิ่มความแม่นยำ (ไม่บังคับ)" data-en="Boost accuracy (optional)">เพิ่มความแม่นยำ (ไม่บังคับ)</span></div>
        <div class="half-row">
          <div class="field" style="margin:0"><label data-th="เวลาเกิด" data-en="Birth Time">เวลาเกิด</label><input type="time" id="f-time"/></div>
          <div class="field" style="margin:0"><label data-th="สถานที่เกิด" data-en="Place of Birth">สถานที่เกิด</label><input type="text" id="f-place" placeholder="เช่น กรุงเทพ"/></div>
        </div>
      </div>
      <div class="field">
        <label data-th="ถอดรหัสเรื่องอะไร" data-en="What to decode">ถอดรหัสเรื่องอะไร</label>
        <div class="pills">
          <input type="radio" name="cat" id="c-self" value="self" class="pi" checked/><label for="c-self" class="pl-lb" data-th="ตัวตน & พลัง" data-en="Self & Energy">ตัวตน & พลัง</label>
          <input type="radio" name="cat" id="c-love" value="love" class="pi"/><label for="c-love" class="pl-lb" data-th="ความรัก" data-en="Love">ความรัก</label>
          <input type="radio" name="cat" id="c-career" value="career" class="pi"/><label for="c-career" class="pl-lb" data-th="การงาน & เงิน" data-en="Career & Money">การงาน & เงิน</label>
          <input type="radio" name="cat" id="c-path" value="path" class="pi"/><label for="c-path" class="pl-lb" data-th="เส้นทางชีวิต" data-en="Life Path">เส้นทางชีวิต</label>
          <input type="radio" name="cat" id="c-block" value="block" class="pi"/><label for="c-block" class="pl-lb" data-th="สิ่งที่ติดอยู่" data-en="What's Blocking">สิ่งที่ติดอยู่</label>
        </div>
      </div>
      <div class="field"><label data-th="คำถามของคุณ" data-en="Your question">คำถามของคุณ</label><textarea id="f-question" placeholder="เช่น ฉันติดอะไรอยู่ ทำไมรู้สึกหลงทาง ชีวิตควรไปทางไหน..."></textarea></div>
      <button class="submit-btn" id="submit-btn" onclick="submitForm()"><span data-th="✦ เริ่มถอดรหัสชีวิตฟรี" data-en="✦ Start Decoding — Free">✦ เริ่มถอดรหัสชีวิตฟรี</span></button>
      <button class="demo-btn" onclick="runDemo()" data-th="ทดลองดูตัวอย่างผลลัพธ์ (demo)" data-en="Preview sample result (demo)">ทดลองดูตัวอย่างผลลัพธ์ (demo)</button>
    </div>
    <div id="loading-state">
      <div class="spin-wrap"><div class="spin-o"></div><div class="spin-i"></div></div>
      <ul class="load-steps">
        <li class="ls" id="ls1" data-th="กำลังอ่านพลังชีวิตของคุณ..." data-en="Reading your life energy...">กำลังอ่านพลังชีวิตของคุณ...</li>
        <li class="ls" id="ls2" data-th="กำลังวิเคราะห์ pattern เลขศาสตร์..." data-en="Analyzing numerology patterns...">กำลังวิเคราะห์ pattern เลขศาสตร์...</li>
        <li class="ls" id="ls3" data-th="กำลังเชื่อม pattern กับคำถามของคุณ..." data-en="Connecting patterns to your question...">กำลังเชื่อม pattern กับคำถามของคุณ...</li>
        <li class="ls" id="ls4" data-th="กำลังวาด Soul Blueprint Mandala..." data-en="Drawing your Soul Blueprint Mandala...">กำลังวาด Soul Blueprint Mandala...</li>
      </ul>
    </div>
  </div>
</section>

<div class="div">✦ ✦ ✦</div>

<!-- WHAT YOU GET FREE -->
<section class="free-section">
  <div class="container">
    <p class="s-lbl rev" data-th="preview ฟรี — เห็นทันทีหลังกรอก" data-en="Free preview — appears right after you submit">preview ฟรี — เห็นทันทีหลังกรอก</p>
    <h2 class="s-ttl rev"><em data-th="กรอกแล้วเห็นทันที" data-en="See It the Moment You Submit">กรอกแล้วเห็นทันที</em></h2>
    <p class="s-sub rev" data-th="ไม่ใช่คำทำนายเหมารวม · ระบบอ่านจากวันเกิดและคำถามของคุณโดยเฉพาะ" data-en="Not generic predictions · The system reads from your exact birth data and question">ไม่ใช่คำทำนายเหมารวม · ระบบอ่านจากวันเกิดและคำถามของคุณโดยเฉพาะ</p>
    <div class="free-grid rev">
      <div class="free-card">
        <span class="free-icon">🔄</span>
        <div class="free-title" data-th="loop ที่ทำให้ชีวิตคุณวนซ้ำ" data-en="The loop making your life repeat">loop ที่ทำให้ชีวิตคุณวนซ้ำ</div>
        <div class="free-desc" data-th="ระบบจะบอกว่า pattern อะไรที่คุณทำซ้ำโดยไม่รู้ตัว และทำไมมันถึงยังไม่หยุด" data-en="The system reveals what pattern you repeat unconsciously — and why it hasn't stopped">ระบบจะบอกว่า pattern อะไรที่คุณทำซ้ำโดยไม่รู้ตัว และทำไมมันถึงยังไม่หยุด</div>
      </div>
      <div class="free-card">
        <span class="free-icon">⚡</span>
        <div class="free-title" data-th="พลังชีวิตแกนกลางของคุณ" data-en="Your core life energy">พลังชีวิตแกนกลางของคุณ</div>
        <div class="free-desc" data-th="ระบบจะเผยพลังที่คุณมีมาตั้งแต่เกิด แต่อาจยังไม่เคยรู้ว่ามันคืออะไร" data-en="Reveals the energy you were born with — that you may never have known you had">ระบบจะเผยพลังที่คุณมีมาตั้งแต่เกิด แต่อาจยังไม่เคยรู้ว่ามันคืออะไร</div>
      </div>
      <div class="free-card">
        <span class="free-icon">🌀</span>
        <div class="free-title" data-th="สิ่งที่ชีวิตกำลังพยายามบอกคุณ" data-en="What life is trying to tell you right now">สิ่งที่ชีวิตกำลังพยายามบอกคุณ</div>
        <div class="free-desc" data-th="ถ้ารู้สึกว่าชีวิตกำลังส่งสัญญาณบางอย่าง แต่ยังอ่านไม่ออก ระบบจะช่วยถอดรหัสมัน" data-en="If life feels like it's signaling something you can't quite read — the system decodes it">ถ้ารู้สึกว่าชีวิตกำลังส่งสัญญาณบางอย่าง แต่ยังอ่านไม่ออก ระบบจะช่วยถอดรหัสมัน</div>
      </div>
      <div class="free-card">
        <span class="free-icon">🔍</span>
        <div class="free-title" data-th="คำตอบตรงๆ สำหรับคำถามที่คุณถาม" data-en="A direct answer to the question you asked">คำตอบตรงๆ สำหรับคำถามที่คุณถาม</div>
        <div class="free-desc" data-th="ระบบวิเคราะห์จากคำถามที่คุณพิมพ์มา ไม่ใช่คำตอบสำเร็จรูป แต่ตรงกับสิ่งที่คุณกำลังเผชิญ" data-en="Analyzed from the exact question you typed — not a template, but matched to what you're facing">ระบบวิเคราะห์จากคำถามที่คุณพิมพ์มา ไม่ใช่คำตอบสำเร็จรูป แต่ตรงกับสิ่งที่คุณกำลังเผชิญ</div>
      </div>
    </div>
    <p class="free-note rev" data-th="ทั้งหมดนี้ <em>ฟรี</em> · เพื่อให้คุณเห็นก่อนว่ามันแม่นแค่ไหน" data-en="All of this is <em>free</em> · So you can see how accurate it is before deciding">ทั้งหมดนี้ <em>ฟรี</em> · เพื่อให้คุณเห็นก่อนว่ามันแม่นแค่ไหน</p>
  </div>
</section>

<div class="div">✦ ✦ ✦</div>

<!-- BENEFITS -->
<section class="benefits">
  <div class="container">
    <p class="s-lbl rev" data-th="คำถามที่คุณไม่เคยถามตัวเอง" data-en="Questions You Never Asked Yourself">คำถามที่คุณไม่เคยถามตัวเอง</p>
    <h2 class="s-ttl rev"><em data-th="แต่คำตอบมีอยู่ในพิมพ์เขียวชีวิตของคุณตลอดมา" data-en="But the answers have always been in your blueprint">แต่คำตอบมีอยู่ในพิมพ์เขียวชีวิตของคุณตลอดมา</em></h2>
    <div class="bc-list">
      <div class="bc rev"><div class="bc-icon">🔄</div><div><div class="bc-title" data-th="ทำไมชีวิตถึงวนลูปเดิมซ้ำๆ ทั้งที่คุณพยายามเปลี่ยนแล้ว?" data-en="Why does life keep repeating the same loop even when you try to change?">ทำไมชีวิตถึงวนลูปเดิมซ้ำๆ ทั้งที่คุณพยายามเปลี่ยนแล้ว?</div><div class="bc-desc" data-th="ไม่ใช่เพราะคุณไม่พยายาม แต่เพราะยังไม่เห็น pattern ที่กำลังดึงคุณกลับ" data-en="Not because you're not trying — but because you haven't seen the pattern pulling you back">ไม่ใช่เพราะคุณไม่พยายาม แต่เพราะยังไม่เห็น pattern ที่กำลังดึงคุณกลับ</div></div></div>
      <div class="bc rev"><div class="bc-icon">🔥</div><div><div class="bc-title" data-th="พลังอะไรในตัวคุณที่คุณยังไม่เคยใช้มันตรงๆ?" data-en="What power do you have that you've never truly used?">พลังอะไรในตัวคุณที่คุณยังไม่เคยใช้มันตรงๆ?</div><div class="bc-desc" data-th="มีพลังบางอย่างที่ถูกกดไว้ตั้งแต่เด็ก ระบบจะช่วยให้คุณเห็นว่ามันคืออะไร" data-en="There's a power suppressed since childhood — the system shows you exactly what it is">มีพลังบางอย่างที่ถูกกดไว้ตั้งแต่เด็ก ระบบจะช่วยให้คุณเห็นว่ามันคืออะไร</div></div></div>
      <div class="bc rev"><div class="bc-icon">💞</div><div><div class="bc-title" data-th="ความสัมพันธ์ที่ผ่านมากำลังสะท้อนอะไรให้คุณ?" data-en="What have your past relationships been reflecting back to you?">ความสัมพันธ์ที่ผ่านมากำลังสะท้อนอะไรให้คุณ?</div><div class="bc-desc" data-th="ทุกความสัมพันธ์ที่เจ็บปวด มีข้อความซ่อนอยู่ที่ยังรอให้คุณอ่านออก" data-en="Every painful relationship carries a hidden message still waiting for you to read">ทุกความสัมพันธ์ที่เจ็บปวด มีข้อความซ่อนอยู่ที่ยังรอให้คุณอ่านออก</div></div></div>
      <div class="bc rev"><div class="bc-icon">🌀</div><div><div class="bc-title" data-th="ชีวิตกำลังพยายามสอนอะไรคุณตอนนี้ — และคุณยังไม่เห็นมัน?" data-en="What is life trying to teach you right now — that you still can't see?">ชีวิตกำลังพยายามสอนอะไรคุณตอนนี้ — และคุณยังไม่เห็นมัน?</div><div class="bc-desc" data-th="บทเรียนที่วนซ้ำจะหยุดก็ต่อเมื่อคุณเห็นมัน ไม่ใช่เมื่อคุณหนีจากมัน" data-en="Repeating lessons only stop when you see them — not when you run from them">บทเรียนที่วนซ้ำจะหยุดก็ต่อเมื่อคุณเห็นมัน ไม่ใช่เมื่อคุณหนีจากมัน</div></div></div>
    </div>
  </div>
</section>

<div class="div">✦ ✦ ✦</div>

<!-- WHY ACCURATE -->
<section class="why">
  <div class="container">
    <p class="s-lbl rev" data-th="ทำไมมันถึงแม่น" data-en="Why It's So Accurate">ทำไมมันถึงแม่น</p>
    <h2 class="s-ttl rev"><em data-th="ไม่ใช่การทำนาย แต่คือการสะท้อนโครงพลังชีวิตของคุณ" data-en="Not Prediction — It Reflects Your Life's Energy Structure">ไม่ใช่การทำนาย แต่คือการสะท้อนโครงพลังชีวิตของคุณ</em></h2>
    <p class="s-sub rev" data-th="ระบบไม่ได้เดาอนาคต แต่วิเคราะห์โครงพลังที่มีอยู่แล้วในตัวคุณ และ pattern ที่กำลังเกิดขึ้นจริง" data-en="The system doesn't guess the future — it analyzes the energy structure already within you, and the patterns currently playing out">ระบบไม่ได้เดาอนาคต แต่วิเคราะห์โครงพลังที่มีอยู่แล้วในตัวคุณ และ pattern ที่กำลังเกิดขึ้นจริง</p>
    <div class="wc-list">
      <div class="wc rev"><span class="wc-icon">🔢</span><div><div class="wc-title" data-th="เลขศาสตร์เชิงลึกจากวันเกิดจริง" data-en="Deep Numerology from Your Exact Birth Date">เลขศาสตร์เชิงลึกจากวันเกิดจริง</div><div class="wc-text" data-th="วิเคราะห์จากวันเดือนปีเกิดของคุณ สร้างแผนที่พลังงานเฉพาะบุคคล ไม่มีคนสองคนที่เหมือนกัน" data-en="Analyzed from your exact birth date — a unique energy map, no two people alike">วิเคราะห์จากวันเดือนปีเกิดของคุณ สร้างแผนที่พลังงานเฉพาะบุคคล ไม่มีคนสองคนที่เหมือนกัน</div></div></div>
      <div class="wc rev"><span class="wc-icon">🌙</span><div><div class="wc-title" data-th="Pattern ชีวิตจริงจากคำถามของคุณ" data-en="Real Life Patterns from Your Own Question">Pattern ชีวิตจริงจากคำถามของคุณ</div><div class="wc-text" data-th="ไม่ใช่คำทำนายลอยๆ แต่วิเคราะห์จาก pattern ที่คุณบอกผ่านคำถามที่ถาม" data-en="Not generic — patterns analyzed from the very question you wrote">ไม่ใช่คำทำนายลอยๆ แต่วิเคราะห์จาก pattern ที่คุณบอกผ่านคำถามที่ถาม</div></div></div>
      <div class="wc rev"><span class="wc-icon">🧠</span><div><div class="wc-title" data-th="การกลั่นกรองโดยผู้เชี่ยวชาญด้านจิตวิญญาณ" data-en="Refined by Spiritual Practitioners">การกลั่นกรองโดยผู้เชี่ยวชาญด้านจิตวิญญาณ</div><div class="wc-text" data-th="ระบบประมวลผลเชิงลึก ผ่านการออกแบบโดยผู้เชี่ยวชาญที่เข้าใจพิมพ์เขียวชีวิตมนุษย์" data-en="Deep processing, designed by experts who deeply understand the human life blueprint">ระบบประมวลผลเชิงลึก ผ่านการออกแบบโดยผู้เชี่ยวชาญที่เข้าใจพิมพ์เขียวชีวิตมนุษย์</div></div></div>
      <div class="wc rev"><span class="wc-icon">🪞</span><div><div class="wc-title" data-th="สะท้อน ไม่ใช่ทำนาย" data-en="It Reflects — Doesn't Predict">สะท้อน ไม่ใช่ทำนาย</div><div class="wc-text" data-th="ระบบไม่ได้บอกอนาคต แต่สะท้อนสิ่งที่คุณมีอยู่แล้วในตัวแต่ยังไม่เคยเห็น" data-en="Doesn't predict the future — reflects what you already carry but cannot yet see">ระบบไม่ได้บอกอนาคต แต่สะท้อนสิ่งที่คุณมีอยู่แล้วในตัวแต่ยังไม่เคยเห็น</div></div></div>
    </div>
    <div class="proof rev">
      <p class="proof-txt">"ฉันไม่คิดว่าแค่วันเกิดจะบอกได้ว่า…ทำไมฉันถึงเลือกคนแบบเดิมซ้ำๆ ทุกครั้ง พอได้อ่านพิมพ์เขียว มันบอกชัดมากว่าฉันกำลังทำอะไรอยู่ <span class="proof-cut">[ ส่วนต่อไปอยู่ในรายงานฉบับเต็ม ]</span>"</p>
      <div class="proof-by">— มินตรา ว. · ผู้ใช้งานจริง</div>
    </div>
  </div>
</section>

<div class="div">✦ ✦ ✦</div>

<!-- REVIEWS -->
<section class="reviews">
  <div class="container">
    <p class="s-lbl rev" data-th="เสียงจากผู้ใช้จริง" data-en="Real Stories">เสียงจากผู้ใช้จริง</p>
    <h2 class="s-ttl rev"><em data-th="พวกเขารู้สึกยังไง" data-en="How They Felt">พวกเขารู้สึกยังไง</em></h2>
    <div class="rv-list">
      <div class="rv rev"><div class="rv-stars">★★★★★</div><p class="rv-story" data-th="ลองดูดวงมาหลายปี แต่ไม่เคยรู้สึก <strong>"นี่มันฉัน"</strong> แบบนี้มาก่อน อ่านแล้วขนลุกเลย มันพูดถึงสิ่งที่ฉันไม่เคยบอกใครสักคน" data-en="Tried fortune telling for years, never felt <strong>'this is me'</strong> like this. Got chills — it mentioned things I've never told anyone.">ลองดูดวงมาหลายปี แต่ไม่เคยรู้สึก <strong>"นี่มันฉัน"</strong> แบบนี้มาก่อน อ่านแล้วขนลุกเลย</p><div class="rv-author"><div class="rv-av">ม</div><div><div class="rv-name">มินตรา ว.</div><div class="rv-meta">Bangkok</div></div></div></div>
      <div class="rv rev"><div class="rv-stars">★★★★★</div><p class="rv-story" data-th="แค่ดูฟรียัง <strong>จุกมาก</strong> จนต้องซื้อฉบับเต็มทันที อ่านแล้วร้องไห้เพราะมัน describe pattern ที่ทำซ้ำมา 5 ปีโดยไม่รู้ตัว" data-en="Even the free version <strong>hit so hard</strong> I got the full report immediately. Cried — described a 5-year pattern I never noticed.">แค่ดูฟรียัง <strong>จุกมาก</strong> จนต้องซื้อฉบับเต็มทันที อ่านแล้วร้องไห้เพราะ pattern ที่ทำซ้ำมา 5 ปี</p><div class="rv-author"><div class="rv-av">ก</div><div><div class="rv-name">กัลยา ร.</div><div class="rv-meta">Online</div></div></div></div>
      <div class="rv rev"><div class="rv-stars">★★★★★</div><p class="rv-story" data-th="มันบอกชัดมากว่าทำไมฉันถึง <strong>ตัดสินใจแบบเดิมซ้ำๆ</strong> ตอนนี้ชีวิตเริ่มเปลี่ยนแล้ว" data-en="Clearly explained why I <strong>kept making the same decisions</strong>. My life started changing after that.">มันบอกชัดมากว่าทำไมฉันถึง <strong>ตัดสินใจแบบเดิมซ้ำๆ</strong> ตอนนี้ชีวิตเริ่มเปลี่ยนแล้ว</p><div class="rv-author"><div class="rv-av">ป</div><div><div class="rv-name">ปภาวิน ส.</div><div class="rv-meta">Chiang Mai</div></div></div></div>
    </div>
  </div>
</section>

<footer>
  <div class="ft-logo">LUMINA SOUL</div>
  <p class="ft-sub" data-th="ถอดรหัสพิมพ์เขียวชีวิต · Spiritual Blueprint System" data-en="Life Blueprint Decoder · Spiritual Blueprint System">ถอดรหัสพิมพ์เขียวชีวิต · Spiritual Blueprint System</p>
  <div class="ft-links">
    <a href="#" data-th="นโยบายความเป็นส่วนตัว" data-en="Privacy Policy">นโยบายความเป็นส่วนตัว</a>
    <a href="#" data-th="เงื่อนไขการใช้งาน" data-en="Terms">เงื่อนไขการใช้งาน</a>
    <a href="https://lin.ee/sjS20F8" target="_blank">LINE</a>
  </div>
</footer>
</div>

<!-- ══════════ PAGE 2 ══════════ -->
<div id="page-result" class="page">
  <div class="result-body">

    <div class="uh">
      <div class="uh-badge">✦ SOUL BLUEPRINT ✦</div>
      <h1 class="uh-name">พิมพ์เขียวชีวิตของ<br><em id="r-name-display">—</em></h1>
      <p class="uh-key" id="r-soul-key-display"></p>
    </div>

    <!-- MANDALA — purple/pink/gold palette only -->
    <div class="mandala-section">
      <canvas id="mandala-c" width="230" height="230"></canvas>
      <p class="mandala-caption" data-th="Soul Blueprint Mandala · วาดจากพลังชีวิตของคุณ" data-en="Soul Blueprint Mandala · Drawn from your life energy">Soul Blueprint Mandala · วาดจากพลังชีวิตของคุณ</p>
    </div>

    <!-- KEY NUMBERS -->
    <div class="key-nums" id="r-key-nums"></div>

    <!-- PREVIEW -->
    <div class="preview-section">
      <span class="preview-label" data-th="✦ พิมพ์เขียวชีวิตของคุณ (ตัวอย่าง)" data-en="✦ Your Life Blueprint (Preview)">✦ พิมพ์เขียวชีวิตของคุณ (ตัวอย่าง)</span>
      <div class="preview-card preview-fade" id="r-preview-card"></div>
      <p class="preview-more" data-th="↑ ข้อความด้านบนเป็นเพียงส่วนหนึ่ง รายงานฉบับเต็มมีมากกว่านี้มาก" data-en="↑ The above is just a glimpse. The full report goes much deeper.">↑ ข้อความด้านบนเป็นเพียงส่วนหนึ่ง รายงานฉบับเต็มมีมากกว่านี้มาก</p>
    </div>

    <!-- HOOK -->
    <div class="hook-box">
      <h3 class="hook-title" data-th="สิ่งที่คุณเห็นตอนนี้เป็นแค่ 10–20% ของทั้งหมด" data-en="What you see now is only 10–20% of the full picture">สิ่งที่คุณเห็นตอนนี้เป็นแค่ 10–20% ของทั้งหมด</h3>
      <p class="hook-pct" data-th="ในฉบับเต็ม คุณจะเห็น..." data-en="In the full report, you'll discover...">ในฉบับเต็ม คุณจะเห็น...</p>
      <ul class="hook-list" id="hook-th">
        <li>รากของปัญหาที่แท้จริงที่ทำให้ชีวิตคุณยังไม่เปลี่ยน</li>
        <li>pattern ที่ทำให้ชีวิตคุณวนซ้ำ และวิธีหลุดออกจากมัน</li>
        <li>บาดแผลลึกที่คุณแบกไว้โดยไม่รู้ตัว</li>
        <li>พลังที่คุณมีแต่ยังไม่เคยใช้เต็มที่</li>
        <li>และทางออกที่ตรงกับคุณจริงๆ</li>
      </ul>
      <ul class="hook-list" id="hook-en" style="display:none">
        <li>The real root of what's keeping your life from changing</li>
        <li>The pattern making your life repeat — and how to break free</li>
        <li>The deep wound you carry without knowing</li>
        <li>The power you have but haven't fully used</li>
        <li>And the way forward that's truly right for you</li>
      </ul>
    </div>

    <!-- PAYWALL -->
    <div class="paywall-card">
      <div class="pw-lock">🔐</div>
      <h2 class="pw-title" data-th="ปลดล็อกพิมพ์เขียวชีวิตฉบับเต็ม" data-en="Unlock Your Full Life Blueprint">ปลดล็อกพิมพ์เขียวชีวิตฉบับเต็ม</h2>
      <p class="pw-sub" data-th="รายงานของคุณถูกสร้างขึ้นแล้วจากข้อมูลเฉพาะของคุณ<br>นี่ไม่ใช่คำทำนายทั่วไป แต่มันคือ &quot;โครงสร้างชีวิตของคุณ&quot;" data-en="Your report was created from your specific data<br>This isn't generic fortune telling — it's your life's structure">รายงานของคุณถูกสร้างขึ้นแล้วจากข้อมูลเฉพาะของคุณ<br>นี่ไม่ใช่คำทำนายทั่วไป แต่มันคือ "โครงสร้างชีวิตของคุณ"</p>
      <div class="pw-price">฿149</div>
      <div class="pw-price-note" data-th="ชำระครั้งเดียว · PDF ส่วนตัว · ไม่หมดอายุ" data-en="One-time payment · Personal PDF · Never expires">ชำระครั้งเดียว · PDF ส่วนตัว · ไม่หมดอายุ</div>
      <ul class="pw-feats" id="pw-th">
        <li>วิเคราะห์พลังชีวิตแกนกลางของคุณ</li>
        <li>สิ่งที่ชีวิตกำลังพยายามบอกคุณตอนนี้</li>
        <li>pattern หรือ loop ที่ทำให้คุณยังไปต่อไม่ได้</li>
        <li>บาดแผลลึกที่คุณแบกไว้โดยไม่รู้ตัว</li>
        <li>ของขวัญหรือพลังที่คุณยังไม่เคยใช้เต็มที่</li>
        <li>บทเรียนสำคัญที่ชีวิตกำลังสอนคุณ</li>
        <li>สิ่งที่ควรระวังในช่วงนี้</li>
        <li>คำตอบตรงๆ สำหรับคำถามที่คุณถาม</li>
        <li>แนวทาง next step ที่เหมาะกับคุณจริง</li>
        <li>Soul Blueprint Mandala ส่วนตัวแบบเต็ม</li>
        <li>รายงาน PDF พรีเมียม · ส่งทาง LINE ภายใน 15 นาที</li>
      </ul>
      <ul class="pw-feats" id="pw-en" style="display:none">
        <li>Analysis of your core life energy</li>
        <li>What life is trying to tell you right now</li>
        <li>The pattern or loop preventing you from moving forward</li>
        <li>The deep wound you carry unconsciously</li>
        <li>The gift or power you haven't fully used</li>
        <li>The important lesson life is teaching you</li>
        <li>What to be mindful of right now</li>
        <li>A direct answer to the question you asked</li>
        <li>A next step pathway designed for you alone</li>
        <li>Full personal Soul Blueprint Mandala</li>
        <li>Premium PDF report · via LINE · within 15 minutes</li>
      </ul>
      <p class="pw-close" data-th="สิ่งนี้อาจเป็นครั้งแรก<br>ที่คุณ &quot;เห็นตัวเองชัดขนาดนี้&quot;" data-en="This may be the first time<br>you've ever seen yourself this clearly">สิ่งนี้อาจเป็นครั้งแรก<br>ที่คุณ "เห็นตัวเองชัดขนาดนี้"</p>
      <a href="https://lin.ee/sjS20F8" class="cta-btn" target="_blank">
        <span data-th="💜 รับรายงานฉบับเต็มทาง LINE" data-en="💜 Get Full Report via LINE">💜 รับรายงานฉบับเต็มทาง LINE</span>
      </a>
      <p class="cta-note" data-th="ทักว่า 'ปลดล็อก' พร้อมชื่อของคุณ · ทีมงานจะติดต่อกลับทันที" data-en="Message 'unlock' with your name · Our team responds immediately">ทักว่า 'ปลดล็อก' พร้อมชื่อของคุณ · ทีมงานจะติดต่อกลับทันที</p>
    </div>

    <button class="back-btn" onclick="goHome()" data-th="← ถอดรหัสใหม่" data-en="← Start over">← ถอดรหัสใหม่</button>
  </div>

  <footer>
    <div class="ft-logo">LUMINA SOUL</div>
    <p class="ft-sub" data-th="ถอดรหัสพิมพ์เขียวชีวิต · Spiritual Blueprint System" data-en="Life Blueprint Decoder · Spiritual Blueprint System">ถอดรหัสพิมพ์เขียวชีวิต · Spiritual Blueprint System</p>
    <div class="ft-links">
      <a href="#" data-th="นโยบายความเป็นส่วนตัว" data-en="Privacy Policy">นโยบายความเป็นส่วนตัว</a>
      <a href="#" data-th="เงื่อนไขการใช้งาน" data-en="Terms">เงื่อนไขการใช้งาน</a>
      <a href="https://lin.ee/sjS20F8" target="_blank">LINE</a>
    </div>
  </footer>
</div>

<script>
// ── LANG ──
let lang='th';
function setLang(l){
  lang=l;
  document.getElementById('btn-th').classList.toggle('active',l==='th');
  document.getElementById('btn-en').classList.toggle('active',l==='en');
  document.querySelectorAll('[data-th],[data-en]').forEach(el=>{
    const v=el.getAttribute('data-'+l);
    if(!v)return;
    if(el.tagName==='INPUT'||el.tagName==='TEXTAREA'){const ph=el.getAttribute('data-'+l+'-placeholder');if(ph)el.placeholder=ph;}
    else{el.innerHTML=v;}
  });
  const mths={th:['','มกราคม','กุมภาพันธ์','มีนาคม','เมษายน','พฤษภาคม','มิถุนายน','กรกฎาคม','สิงหาคม','กันยายน','ตุลาคม','พฤศจิกายน','ธันวาคม'],
    en:['','January','February','March','April','May','June','July','August','September','October','November','December']};
  const sel=document.getElementById('f-month');const cv=sel.value;
  [...sel.options].forEach((o,i)=>o.textContent=i===0?(l==='th'?'เดือน':'Month'):mths[l][i]);sel.value=cv;
  // toggle lang-specific lists
  ['hook-th','hook-en','pw-th','pw-en','inside-list-th','inside-list-en'].forEach(id=>{
    const el=document.getElementById(id);if(!el)return;
    el.style.display=(id.endsWith('-'+l))?'flex':'none';
  });
}

// ── PAGE ──
function showPage(id){
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  window.scrollTo({top:0,behavior:'smooth'});
}
function goHome(){
  document.getElementById('form-state').style.display='block';
  document.getElementById('loading-state').style.display='none';
  showPage('page-form');
}

// ── SCROLL REVEAL ──
const obs=new IntersectionObserver(e=>e.forEach(x=>{if(x.isIntersecting){x.target.classList.add('in');obs.unobserve(x.target);}}),{threshold:.08});
document.querySelectorAll('.rev').forEach(el=>obs.observe(el));

// ── LOAD STEPS ──
let lt;
function startLoad(){
  const ids=['ls1','ls2','ls3','ls4'];
  ids.forEach(id=>document.getElementById(id).className='ls');
  document.getElementById(ids[0]).classList.add('active');let i=0;
  lt=setInterval(()=>{if(i<ids.length-1){document.getElementById(ids[i]).className='ls done';i++;document.getElementById(ids[i]).classList.add('active');}},1400);
}
function stopLoad(){clearInterval(lt);}

// ── NUMEROLOGY (for mandala visuals only) ──
function reduce(n){while(n>9&&n!==11&&n!==22&&n!==33)n=String(n).split('').reduce((a,d)=>a+parseInt(d),0);return n;}
function calcNums(day,month,year){
  const y=year>2400?year-543:year;
  const lp=reduce(reduce(day)+reduce(month)+String(y).split('').reduce((a,d)=>a+parseInt(d),0));
  const dest=reduce(day+month+String(y).split('').reduce((a,d)=>a+parseInt(d),0));
  const soul=reduce(reduce(day)+reduce(month));
  return{lp,dest,soul};
}

// ── MANDALA — spiritual energy code map ──
let animId;
function drawMandala(lp,dest,soul){
  const canvas=document.getElementById('mandala-c');
  const ctx=canvas.getContext('2d');
  const W=230,H=230,cx=115,cy=115;
  const palettes=[
    {c1:'#9B59D0',c2:'#D966A8',c3:'#C9A84C'},
    {c1:'#7B3FBE',c2:'#F472B6',c3:'#E8C040'},
    {c1:'#C084FC',c2:'#D966A8',c3:'#F0D080'},
  ];
  const pal=palettes[lp%3];
  const {c1,c2,c3}=pal;
  let rot=0;
  if(animId)cancelAnimationFrame(animId);

  function hex2rgba(hex,a){const r=parseInt(hex.slice(1,3),16),g=parseInt(hex.slice(3,5),16),b=parseInt(hex.slice(5,7),16);return`rgba(${r},${g},${b},${a})`;}
  function drawPolygon(ctx,n,r,rot0,stroke,fill,sw){
    ctx.beginPath();
    for(let i=0;i<n;i++){const a=rot0+(i/n)*Math.PI*2;const x=Math.cos(a)*r,y=Math.sin(a)*r;i===0?ctx.moveTo(x,y):ctx.lineTo(x,y);}
    ctx.closePath();if(fill){ctx.fillStyle=fill;ctx.fill();}
    if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=sw||1;ctx.stroke();}
  }

  function frame(){
    ctx.clearRect(0,0,W,H);
    ctx.save();ctx.translate(cx,cy);

    // ── Outer energy field (slow rotation) ──
    ctx.save();ctx.rotate(rot*.4);
    // Frequency rings — outer
    [108,96,84,72,60,48,36,24].forEach((r,i)=>{
      const a=.08-.008*i;
      ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);
      ctx.strokeStyle=i%2===0?c1:c2;ctx.globalAlpha=a*4;ctx.lineWidth=i<3?1.5:1;ctx.stroke();ctx.globalAlpha=1;
    });
    ctx.restore();

    // ── Rotating sacred geometry layer 1 ──
    ctx.save();ctx.rotate(rot);
    // 12-spoke wheel
    for(let s=0;s<12;s++){
      const a=(s/12)*Math.PI*2;
      ctx.beginPath();ctx.moveTo(18*Math.cos(a),18*Math.sin(a));ctx.lineTo(108*Math.cos(a),108*Math.sin(a));
      ctx.strokeStyle=c1;ctx.globalAlpha=.15;ctx.lineWidth=.7;ctx.stroke();ctx.globalAlpha=1;
    }
    // Outer 12-gon
    drawPolygon(ctx,12,108,0,hex2rgba(c1,.4),null,.9);
    ctx.restore();

    // ── Counter-rotating layer ──
    ctx.save();ctx.rotate(-rot*.7);
    // Hexagram (Star of David style — 2 triangles)
    drawPolygon(ctx,3,72,-Math.PI/2,hex2rgba(c1,.55),hex2rgba(c1,.04),1.2);
    drawPolygon(ctx,3,72,Math.PI/2,hex2rgba(c2,.55),hex2rgba(c2,.04),1.2);
    // Inner hexagon
    drawPolygon(ctx,6,38,0,hex2rgba(c3,.6),hex2rgba(c3,.06),1);
    ctx.restore();

    // ── Slow rotation layer — sigil/code lines ──
    ctx.save();ctx.rotate(rot*.25);
    // Life path number determines connection pattern
    const pts=[];
    const nPts=Math.max(7,lp+4);
    for(let p=0;p<nPts;p++){const a=(p/nPts)*Math.PI*2-Math.PI/2;pts.push({x:Math.cos(a)*88,y:Math.sin(a)*88});}
    // Connect every (soul) points for sigil effect
    const step=Math.max(2,soul%nPts||2);
    ctx.strokeStyle=c3;ctx.globalAlpha=.25;ctx.lineWidth=.8;
    for(let i=0;i<nPts;i++){
      const j=(i*step)%nPts;
      ctx.beginPath();ctx.moveTo(pts[i].x,pts[i].y);ctx.lineTo(pts[j].x,pts[j].y);ctx.stroke();
    }
    // Dot nodes
    pts.forEach(p=>{ctx.beginPath();ctx.arc(p.x,p.y,2,0,Math.PI*2);ctx.fillStyle=c3;ctx.globalAlpha=.7;ctx.fill();});
    ctx.globalAlpha=1;
    ctx.restore();

    // ── Petals (destiny count) — medium rotation ──
    ctx.save();ctx.rotate(rot*.6);
    const pN=Math.max(4,Math.min(dest,9));
    for(let p=0;p<pN;p++){
      const a=(p/pN)*Math.PI*2;
      ctx.save();ctx.rotate(a);
      ctx.beginPath();ctx.ellipse(0,-52,11,20,0,0,Math.PI*2);
      ctx.strokeStyle=c2;ctx.globalAlpha=.4;ctx.lineWidth=1;ctx.stroke();
      ctx.fillStyle=c2;ctx.globalAlpha=.06;ctx.fill();
      ctx.globalAlpha=1;ctx.restore();
    }
    ctx.restore();

    // ── Diamond nodes on ring 96 ──
    ctx.save();ctx.rotate(rot*.3);
    for(let d=0;d<lp;d++){
      const a=(d/lp)*Math.PI*2;
      const dx=96*Math.cos(a),dy=96*Math.sin(a);
      ctx.save();ctx.translate(dx,dy);ctx.rotate(a);
      ctx.beginPath();ctx.moveTo(0,-5);ctx.lineTo(3.5,0);ctx.lineTo(0,5);ctx.lineTo(-3.5,0);ctx.closePath();
      ctx.fillStyle=c3;ctx.globalAlpha=.88;ctx.fill();ctx.globalAlpha=1;ctx.restore();
    }
    ctx.restore();

    // ── Code tick marks on outer ring ──
    ctx.save();ctx.rotate(-rot*.2);
    for(let t=0;t<36;t++){
      const a=(t/36)*Math.PI*2;
      const len=t%3===0?8:4;
      const r0=108,r1=r0+len;
      ctx.beginPath();ctx.moveTo(Math.cos(a)*r0,Math.sin(a)*r0);ctx.lineTo(Math.cos(a)*r1,Math.sin(a)*r1);
      ctx.strokeStyle=t%3===0?c3:c1;ctx.globalAlpha=t%3===0?.7:.3;ctx.lineWidth=t%3===0?1.2:.7;ctx.stroke();
      ctx.globalAlpha=1;
    }
    ctx.restore();

    // ── Center core glow ──
    const cg=ctx.createRadialGradient(0,0,0,0,0,16);
    cg.addColorStop(0,'rgba(255,255,255,.98)');
    cg.addColorStop(.35,hex2rgba(c3,.85));
    cg.addColorStop(.7,hex2rgba(c1,.4));
    cg.addColorStop(1,'transparent');
    ctx.beginPath();ctx.arc(0,0,16,0,Math.PI*2);ctx.fillStyle=cg;ctx.fill();

    // Life path number
    ctx.fillStyle='rgba(30,10,60,.9)';
    ctx.font='bold 10px Cinzel,serif';ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.fillText(lp,0,0);

    ctx.restore();
    rot+=.002;
    animId=requestAnimationFrame(frame);
  }
  frame();
}

// ── RENDER BACKEND RESPONSE ──
function renderPreview(data){
  const fieldMap={
    intro:{icon:'🌙',lbl:{th:'สิ่งที่ชีวิตกำลังบอกคุณ',en:'What life is telling you'}},
    category_text:{icon:'🔮',lbl:{th:'พลังงานหลักของคุณ',en:'Your core energy'}},
    focus_text:{icon:'🎯',lbl:{th:'โฟกัสในช่วงนี้',en:'Your current focus'}},
    soul_text:{icon:'✨',lbl:{th:'พลังวิญญาณ',en:'Your soul energy'}},
    wound:{icon:'💔',lbl:{th:'บาดแผลที่ซ่อนอยู่',en:'Hidden wound'}},
    gift:{icon:'🎁',lbl:{th:'ของขวัญในพิมพ์เขียว',en:'Blueprint gift'}},
  };
  const blocks=[];
  let hasStructured=false;
  for(const[key,meta]of Object.entries(fieldMap)){
    if(data[key]){hasStructured=true;blocks.push({icon:meta.icon,heading:meta.lbl[lang],text:data[key]});}
  }
  if(!hasStructured){
    const raw=data.preview_text||data.preview||data.ai_preview||data.message||'';
    if(raw){raw.split(/\n+/).filter(p=>p.trim()).slice(0,3).forEach((p,i)=>{
      blocks.push({icon:i===0?'🌙':'',heading:i===0?(lang==='th'?'สิ่งที่ชีวิตกำลังบอกคุณ':'What life is telling you'):'',text:p});
    });}
  }
  if(blocks.length===0){blocks.push({icon:'🌙',heading:lang==='th'?'กำลังประมวลผล':'Processing',
    text:lang==='th'?'ระบบกำลังประมวลผลพิมพ์เขียวชีวิตของคุณ ผลลัพธ์จะถูกส่งผ่าน LINE ของคุณเร็วๆ นี้':'Your blueprint is being processed. Results will arrive via your LINE soon.'});}

  const card=document.getElementById('r-preview-card');
  card.innerHTML=blocks.slice(0,2).map((b,i)=>`
    <div class="pb">
      ${b.icon?`<span class="pb-icon">${b.icon}</span>`:''}
      ${b.heading?`<h3 class="pb-heading">${b.heading}</h3>`:''}
      <p class="pb-text">${b.text.replace(/\n/g,'<br>')}</p>
    </div>
    ${i<blocks.slice(0,2).length-1?'<hr class="pb-sep">':''}
  `).join('');
}

function renderKeyNums(data,cn){
  const nums=[
    {val:data.life_number||cn.lp,title:lang==='th'?'เลขชีวิต':'Life Path',sub:lang==='th'?'เส้นทางหลัก':'Core path'},
    {val:data.destiny_number||cn.dest,title:lang==='th'?'เลขภารกิจ':'Destiny',sub:lang==='th'?'พลังงานชีวิต':'Life energy'},
    {val:data.soul_number||cn.soul,title:lang==='th'?'เลขวิญญาณ':'Soul Urge',sub:lang==='th'?'ความต้องการลึกสุด':'Deepest need'},
  ];
  document.getElementById('r-key-nums').innerHTML=nums.map(n=>`
    <div class="kn"><div class="kn-val">${n.val!==undefined?n.val:'?'}</div>
    <div class="kn-title">${n.title}</div><div class="kn-sub">${n.sub}</div></div>
  `).join('');
}

// ── SHOW RESULT ──
function showResult(data,name,day,month,year){
  const cn=(day&&month&&year)?calcNums(day,month,year):{lp:7,dest:5,soul:3};
  document.getElementById('r-name-display').textContent=name||'—';
  document.getElementById('r-soul-key-display').textContent=data.soul_key||`Life Path ${cn.lp} · Destiny ${cn.dest} · Soul ${cn.soul}`;
  renderKeyNums(data,cn);
  renderPreview(data);
  // hook lang
  const hth=document.getElementById('hook-th');const hen=document.getElementById('hook-en');
  if(hth)hth.style.display=lang==='th'?'flex':'none';
  if(hen)hen.style.display=lang==='en'?'flex':'none';
  const pth=document.getElementById('pw-th');const pen=document.getElementById('pw-en');
  if(pth)pth.style.display=lang==='th'?'flex':'none';
  if(pen)pen.style.display=lang==='en'?'flex':'none';
  showPage('page-result');
  setTimeout(()=>drawMandala(cn.lp,cn.dest,cn.soul),100);
}

// ── SUBMIT ──
async function submitForm(){
  const name=document.getElementById('f-name').value.trim();
  const line_id=document.getElementById('f-line').value.trim();
  const birth_day=parseInt(document.getElementById('f-day').value)||null;
  const birth_month=parseInt(document.getElementById('f-month').value)||null;
  const birth_year=parseInt(document.getElementById('f-year').value)||null;
  const birth_time=document.getElementById('f-time').value;
  const birth_place=document.getElementById('f-place').value.trim();
  const category=document.querySelector('input[name="cat"]:checked').value;
  const question=document.getElementById('f-question').value.trim();
  if(!name||!birth_day||!birth_month||!birth_year||!question){
    alert(lang==='th'?'กรุณากรอก: ชื่อ วันเกิด เดือน ปี และคำถามของคุณ':'Please fill in: name, day, month, year, and your question');return;
  }
  const payload={name,line_id,birth_day,birth_month,birth_year,birth_time,birth_place,category,question,lang,source:'website_form_v2',is_paid:false};
  document.getElementById('form-state').style.display='none';
  document.getElementById('loading-state').style.display='block';
  document.getElementById('loading-state').scrollIntoView({behavior:'smooth',block:'center'});
  startLoad();
  try{
    const res=await fetch('/webhook/blueprint',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
    if(!res.ok)throw new Error('HTTP '+res.status);
    const d=await res.json();
    stopLoad();showResult(d,name,birth_day,birth_month,birth_year);
  }catch(err){
    stopLoad();
    document.getElementById('loading-state').style.display='none';
    document.getElementById('form-state').style.display='block';
    alert((lang==='th'?'เกิดข้อผิดพลาด กรุณาลองใหม่\n':'Error, please try again\n')+err.message);
  }
}

// ── DEMO ──
function runDemo(){
  const d={
    soul_key:'Life Path 7 · Destiny 5 · Soul Urge 3',
    life_number:7,destiny_number:5,soul_number:3,
    preview_text:lang==='th'
      ?`คุณไม่ได้ล้มเหลวเพราะคุณไม่เก่ง\n\nแต่เพราะคุณกำลังใช้พลังงานไปในทิศทางที่ขัดกับโครงพลังชีวิตของคุณเอง โดยไม่รู้ตัว\n\nสิ่งที่ทำให้คุณรู้สึกว่า "ทำไมฉันถึงยังอยู่ที่เดิม" — นั่นไม่ใช่ความอ่อนแอ แต่มันคือสัญญาณที่ชีวิตส่งมาให้คุณซ้ำๆ จนกว่าคุณจะอ่านมันออก`
      :`You haven't failed because you're not capable.\n\nYou've been channeling your energy in a direction that works against your own life's energy structure — without knowing it.\n\nThe feeling of "why am I still stuck here" isn't weakness. It's a signal life keeps sending until you finally decode it.`
  };
  showResult(d,lang==='th'?'ตัวอย่าง':'Demo',30,7,2535);
}
</script>
</body>
</html>
