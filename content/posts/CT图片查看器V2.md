project: 自己制作的html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NIfTI Viewer</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: system-ui, sans-serif; background: #1a1a1a; color: #e0e0e0; padding: 16px; min-width: 360px; }
h1 { font-size: 15px; font-weight: 500; margin-bottom: 14px; color: #fff; letter-spacing: .3px; }

/* upload zone */
.upload-zone { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 14px; }
.upload-card { background: #242424; border: 1.5px dashed #444; border-radius: 9px; padding: 12px 10px;
  text-align: center; cursor: pointer; transition: border-color .2s, background .2s; position: relative; }
.upload-card:hover { border-color: #5b9bd5; background: #1e2a36; }
.upload-card.loaded { border-style: solid; border-color: #3a6a3a; background: #1e2a1e; }
.upload-card.loaded-label { border-color: #6a4a1e; background: #2a1e10; }
.upload-card input[type=file] { position: absolute; inset: 0; opacity: 0; cursor: pointer; width: 100%; height: 100%; }
.upload-card .uc-icon { font-size: 20px; margin-bottom: 5px; }
.upload-card .uc-title { font-size: 12px; font-weight: 500; color: #ccc; }
.upload-card .uc-sub { font-size: 11px; color: #666; margin-top: 3px; }
.upload-card .uc-name { font-size: 11px; color: #7bc47b; margin-top: 4px; word-break: break-all; }
.upload-card.loaded-label .uc-name { color: #d4a35a; }
.badge { display: inline-block; font-size: 10px; padding: 2px 7px; border-radius: 10px; margin-top: 5px; }
.badge-img { background: #1a3a1a; color: #7bc47b; }
.badge-lbl { background: #3a2a0a; color: #d4a35a; }

/* controls */
.controls { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 10px; }
.ctrl-box { background: #242424; border-radius: 8px; padding: 10px 14px; }
.ctrl-box label { font-size: 11px; color: #777; display: block; margin-bottom: 5px; }
.ctrl-row { display: flex; align-items: center; gap: 8px; }
input[type=range] { flex: 1; accent-color: #5b9bd5; }
input[type=number] { width: 64px; background: #151515; border: 1px solid #3a3a3a; border-radius: 5px;
  color: #e0e0e0; font-size: 13px; font-weight: 500; padding: 3px 5px; text-align: center; }
.presets { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 10px; }
.presets button { font-size: 11px; padding: 4px 10px; background: #242424; border: 1px solid #3a3a3a;
  border-radius: 5px; color: #bbb; cursor: pointer; }
.presets button:hover { background: #333; color: #fff; }
.axis-bar { display: grid; grid-template-columns: repeat(3, 1fr); gap: 4px; margin-bottom: 10px; }
.axis-bar button { font-size: 12px; padding: 6px; background: #242424; border: 1px solid #3a3a3a;
  border-radius: 5px; color: #999; cursor: pointer; }
.axis-bar button.active { background: #1a3a5c; border-color: #5b9bd5; color: #5b9bd5; }
.slice-row { background: #242424; border-radius: 8px; padding: 10px 14px; margin-bottom: 12px; }
.row-head { display: flex; justify-content: space-between; margin-bottom: 5px; }
.row-head label { font-size: 11px; color: #777; }
.row-head span { font-size: 12px; font-weight: 500; }
.total-row { display: flex; align-items: center; justify-content: space-between; margin-top: 8px; }
.total-row span { font-size: 11px; color: #777; }
.total-row div { display: flex; align-items: center; gap: 6px; }
.sm-btn { font-size: 11px; padding: 3px 10px; background: #2a2a2a; border: 1px solid #444;
  border-radius: 5px; color: #bbb; cursor: pointer; }
.sm-btn:hover { background: #333; }

/* viewer */
.viewer-wrap { position: relative; background: #000; border-radius: 10px; overflow: hidden;
  max-width: 420px; margin: 0 auto 12px; aspect-ratio: 1; }
#viewer { width: 100%; height: 100%; display: block; image-rendering: pixelated; }
.ov { position: absolute; font-size: 11px; font-family: monospace; pointer-events: none; }
.ov-tl { top: 8px; left: 10px; color: #aaa; }
.ov-tr { top: 8px; right: 10px; color: #777; }
.ov-bl { bottom: 8px; left: 10px; color: #aaa; }

/* label controls */
.label-ctrl { background: #242424; border-radius: 8px; padding: 10px 14px; margin-bottom: 12px; display: none; }
.label-ctrl label { font-size: 11px; color: #777; display: block; margin-bottom: 6px; }
.alpha-row { display: flex; align-items: center; gap: 8px; }
.color-legend { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }
.color-swatch { display: flex; align-items: center; gap: 5px; font-size: 11px; color: #aaa; }
.color-swatch span { width: 12px; height: 12px; border-radius: 2px; display: inline-block; }

/* save panel */
.save-panel { background: #242424; border-radius: 8px; padding: 12px 14px; margin-bottom: 12px; }
.save-panel label { font-size: 11px; color: #777; display: block; margin-bottom: 8px; }
.save-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; }
.save-row2 { display: flex; gap: 8px; margin-top: 8px; align-items: center; flex-wrap: wrap; }
.save-row2 span { font-size: 11px; color: #777; }
select { background: #151515; border: 1px solid #3a3a3a; border-radius: 5px; color: #ccc;
  font-size: 12px; padding: 4px 8px; }
.save-btn { font-size: 12px; padding: 6px 16px; background: #1a3a5c; border: 1px solid #5b9bd5;
  border-radius: 6px; color: #9ecfff; cursor: pointer; font-weight: 500; }
.save-btn:hover { background: #254d73; }
.save-btn.batch { background: #2a1a3a; border-color: #9b7bd5; color: #d0b0ff; }
.save-btn.batch:hover { background: #3a2a55; }

#status { font-size: 12px; color: #5b9bd5; margin-bottom: 10px; min-height: 16px; }
#status.error { color: #e06060; }
#status.ok { color: #7bc47b; }
@media(max-width:480px){ .controls{grid-template-columns:1fr;} .save-grid{grid-template-columns:1fr 1fr;} }
</style>
</head>
<body>
<h1>NIfTI Viewer</h1>

<!-- ── 上传区 ─────────────────────────────────── -->
<div class="upload-zone">
  <div class="upload-card" id="card-img">
    <input type="file" accept=".nii,.gz" onchange="handleUpload(this,'img')">
    <div class="uc-icon">🧠</div>
    <div class="uc-title">影像 .nii</div>
    <div class="uc-sub">.nii / .nii.gz</div>
    <div class="uc-name" id="name-img">未上传</div>
  </div>
  <div class="upload-card" id="card-lbl">
    <input type="file" accept=".nii,.gz" onchange="handleUpload(this,'lbl')">
    <div class="uc-icon">🏷️</div>
    <div class="uc-title">标签 .nii <span style="color:#666;font-weight:400">（可选）</span></div>
    <div class="uc-sub">.nii / .nii.gz</div>
    <div class="uc-name" id="name-lbl">未上传</div>
  </div>
</div>

<div id="status"></div>

<!-- ── 窗宽窗位 ───────────────────────────────── -->
<div class="controls">
  <div class="ctrl-box">
    <label>窗宽 WW</label>
    <div class="ctrl-row">
      <input type="range" id="ww" min="1" max="4000" value="400" step="1">
      <input type="number" id="ww-num" min="1" max="4000" value="400">
    </div>
  </div>
  <div class="ctrl-box">
    <label>窗位 WL</label>
    <div class="ctrl-row">
      <input type="range" id="wl" min="-1000" max="3000" value="40" step="1">
      <input type="number" id="wl-num" min="-1000" max="3000" value="40">
    </div>
  </div>
</div>
<div class="presets">
  <button onclick="setPreset(400,40)">软组织</button>
  <button onclick="setPreset(1500,-600)">肺窗</button>
  <button onclick="setPreset(2500,480)">骨窗</button>
  <button onclick="setPreset(80,40)">脑窗</button>
  <button onclick="setPreset(350,60)">腹部</button>
</div>

<!-- ── 方位 ─────────────────────────────────────── -->
<div class="axis-bar">
  <button id="btn-axial" class="active" onclick="setAxis('axial')">轴状位</button>
  <button id="btn-coronal" onclick="setAxis('coronal')">冠状位</button>
  <button id="btn-sagittal" onclick="setAxis('sagittal')">矢状位</button>
</div>

<!-- ── 切片 ─────────────────────────────────────── -->
<div class="slice-row">
  <div class="row-head">
    <label>切片</label>
    <span id="slice-label">33 / 64</span>
  </div>
  <input type="range" id="slice" min="0" max="63" value="32" step="1" style="width:100%;accent-color:#5b9bd5">
  <div class="total-row">
    <span>演示切片总数</span>
    <div>
      <input type="number" id="total-slices" min="8" max="512" value="64" step="1" style="width:60px">
      <button class="sm-btn" onclick="applySliceCount()">应用</button>
    </div>
  </div>
</div>

<!-- ── 标签透明度控制（有标签时显示）─────────────── -->
<div class="label-ctrl" id="label-ctrl">
  <label>标签叠加透明度</label>
  <div class="alpha-row">
    <input type="range" id="alpha" min="0" max="100" value="50" step="1" style="flex:1;accent-color:#d4a35a">
    <span id="alpha-val" style="font-size:13px;font-weight:500;min-width:32px">50%</span>
  </div>
  <div class="color-legend" id="color-legend"></div>
</div>

<!-- ── 查看器 ─────────────────────────────────── -->
<div class="viewer-wrap">
  <canvas id="viewer"></canvas>
  <div class="ov ov-tl" id="ov-ww">WW:400  WL:40</div>
  <div class="ov ov-tr" id="ov-axis">Axial</div>
  <div class="ov ov-bl" id="ov-pos">S:33</div>
</div>

<!-- ── 保存面板 ───────────────────────────────── -->
<div class="save-panel">
  <label>保存切片图片</label>
  <div class="save-grid">
    <div>
      <div style="font-size:11px;color:#777;margin-bottom:4px">格式</div>
      <select id="fmt">
        <option value="png">PNG</option>
        <option value="jpeg">JPEG</option>
      </select>
    </div>
    <div>
      <div style="font-size:11px;color:#777;margin-bottom:4px">分辨率</div>
      <select id="res">
        <option value="512">512×512</option>
        <option value="1024">1024×1024</option>
        <option value="256">256×256</option>
      </select>
    </div>
    <div>
      <div style="font-size:11px;color:#777;margin-bottom:4px">叠加标签</div>
      <select id="overlay-opt">
        <option value="1">是</option>
        <option value="0">否</option>
      </select>
    </div>
  </div>
  <div class="save-row2">
    <button class="save-btn" onclick="saveCurrent()">💾 保存当前切片</button>
    <button class="save-btn batch" onclick="saveBatch()">📦 批量保存全部切片</button>
    <span id="batch-progress"></span>
  </div>
</div>

<script>
// ─── 状态 ────────────────────────────────────────────────
const state = { ww:400, wl:40, slice:32, axis:'axial' };
let imgVol=null, lblVol=null;
let imgDims=[64,64,64], lblDims=null;

const SZ = 512;
const canvas = document.getElementById('viewer');
const ctx = canvas.getContext('2d');
canvas.width=SZ; canvas.height=SZ;

// ─── 标签颜色表（最多32色，0为背景透明）─────────────────
const LABEL_COLORS = [
  null,
  [255,80,80],[80,180,255],[80,255,130],[255,200,60],
  [220,100,255],[60,220,220],[255,130,60],[160,255,80],
  [255,80,180],[100,140,255],[255,255,80],[80,255,200],
  [200,80,255],[255,160,100],[80,200,100],[200,200,60],
  [255,100,140],[140,200,255],[180,255,140],[255,180,80],
  [160,100,255],[80,240,180],[255,140,200],[100,200,160],
  [220,160,255],[255,220,120],[120,180,200],[200,255,180],
  [255,120,100],[160,220,100],[100,160,220],[220,200,160]
];

// ─── 合成幻影 ────────────────────────────────────────────
function makeSyntheticVolume(nx,ny,nz){
  const vol=new Float32Array(nx*ny*nz);
  const cx=nx/2,cy=ny/2,cz=nz/2;
  for(let z=0;z<nz;z++) for(let y=0;y<ny;y++) for(let x=0;x<nx;x++){
    const dx=x-cx,dy=y-cy,dz=(z-cz)*(nz/nx);
    const d=Math.sqrt(dx*dx+dy*dy+dz*dz);
    let v=-1000;
    if(d<nx*.42)v=-600;
    if(d<nx*.38)v=50;
    if(d<nx*.26)v=40;
    if(d<nx*.16){const a=Math.atan2(dy,dx);v=40+(Math.sin(a*3+z*.25)*.5+.5)*100;}
    if(Math.abs(d-nx*.38)<nx*.035){v=900+(Math.sin(x*.7)*Math.cos(y*.6)*Math.sin(z*.5))*250;}
    const ex=x-(cx+nx*.15),ey=y-(cy-ny*.1),ez=z-(cz+nz*.05);
    if(Math.sqrt(ex*ex+ey*ey+ez*ez)<nx*.06)v=200;
    vol[z*nx*ny+y*nx+x]=v+(Math.random()-.5)*8;
  }
  return vol;
}
function resetVolume(nz){
  imgDims=[64,64,nz];
  imgVol=makeSyntheticVolume(64,64,nz);
  lblVol=null; lblDims=null;
}
resetVolume(64);

// ─── 切片提取 ────────────────────────────────────────────
function getSlice(vol,dims,axis,idx){
  const[nx,ny,nz]=dims;
  if(axis==='axial'){
    const zi=Math.min(idx,nz-1),w=nx,h=ny,data=new Float32Array(w*h);
    for(let y=0;y<ny;y++) for(let x=0;x<nx;x++) data[y*w+x]=vol[zi*nx*ny+y*nx+x];
    return{w,h,data};
  } else if(axis==='coronal'){
    const yi=Math.min(idx,ny-1),w=nx,h=nz,data=new Float32Array(w*h);
    for(let z=0;z<nz;z++) for(let x=0;x<nx;x++) data[z*w+x]=vol[z*nx*ny+yi*nx+x];
    return{w,h,data};
  } else {
    const xi=Math.min(idx,nx-1),w=ny,h=nz,data=new Float32Array(w*h);
    for(let z=0;z<nz;z++) for(let y=0;y<ny;y++) data[z*w+y]=vol[z*nx*ny+y*nx+xi];
    return{w,h,data};
  }
}

// ─── 窗函数 ─────────────────────────────────────────────
function applyWindow(v,ww,wl){
  const lo=wl-ww/2,hi=wl+ww/2;
  return v<=lo?0:v>=hi?255:Math.round((v-lo)/ww*255);
}

// ─── 渲染到指定 canvas ─────────────────────────────────
function renderToCanvas(targetCtx, targetSZ, sliceIdx, withOverlay) {
  const{ww,wl,axis}=state;
  const{w,h,data}=getSlice(imgVol,imgDims,axis,sliceIdx);
  const img=targetCtx.createImageData(targetSZ,targetSZ);
  const scx=targetSZ/w,scy=targetSZ/h;

  // 绘制灰度影像
  for(let py=0;py<targetSZ;py++){
    for(let px=0;px<targetSZ;px++){
      const sx=Math.min(Math.floor(px/scx),w-1);
      const sy=Math.min(Math.floor(py/scy),h-1);
      const g=applyWindow(data[sy*w+sx],ww,wl);
      const i=(py*targetSZ+px)*4;
      img.data[i]=g;img.data[i+1]=g;img.data[i+2]=g;img.data[i+3]=255;
    }
  }
  targetCtx.putImageData(img,0,0);

  // 叠加标签
  if(withOverlay && lblVol && lblDims){
    const alpha=parseInt(document.getElementById('alpha').value)/100;
    const{w:lw,h:lh,data:ldata}=getSlice(lblVol,lblDims,axis,sliceIdx);
    const lscx=targetSZ/lw,lscy=targetSZ/lh;
    // 用 offscreen 合成标签层
    const lblCanvas=new OffscreenCanvas(targetSZ,targetSZ);
    const lblCtx=lblCanvas.getContext('2d');
    const lblImg=lblCtx.createImageData(targetSZ,targetSZ);
    for(let py=0;py<targetSZ;py++){
      for(let px=0;px<targetSZ;px++){
        const sx=Math.min(Math.floor(px/lscx),lw-1);
        const sy=Math.min(Math.floor(py/lscy),lh-1);
        const lval=Math.round(ldata[sy*lw+sx]);
        if(lval===0) continue;
        const ci=lval % LABEL_COLORS.length;
        const col=LABEL_COLORS[ci]||LABEL_COLORS[1];
        const i=(py*targetSZ+px)*4;
        lblImg.data[i]=col[0];lblImg.data[i+1]=col[1];lblImg.data[i+2]=col[2];lblImg.data[i+3]=Math.round(alpha*255);
      }
    }
    lblCtx.putImageData(lblImg,0,0);
    targetCtx.drawImage(lblCanvas,0,0);
  }
}

function render(){
  renderToCanvas(ctx, SZ, state.slice, true);
  const max=getAxisMax(state.axis);
  document.getElementById('ov-ww').textContent=`WW:${state.ww}  WL:${state.wl}`;
  document.getElementById('slice-label').textContent=`${state.slice+1} / ${max}`;
  document.getElementById('ov-pos').textContent=`S:${state.slice+1}`;
  document.getElementById('ov-axis').textContent={axial:'Axial',coronal:'Coronal',sagittal:'Sagittal'}[state.axis];
}

function getAxisMax(a){return a==='axial'?imgDims[2]:a==='coronal'?imgDims[1]:imgDims[0];}

// ─── 颜色图例 ────────────────────────────────────────────
function updateLegend(){
  if(!lblVol) return;
  const seen=new Set();
  for(let i=0;i<lblVol.length;i++){const v=Math.round(lblVol[i]);if(v>0)seen.add(v);}
  const vals=[...seen].sort((a,b)=>a-b).slice(0,20);
  const leg=document.getElementById('color-legend');
  leg.innerHTML=vals.map(v=>{
    const col=LABEL_COLORS[v%LABEL_COLORS.length]||LABEL_COLORS[1];
    return`<div class="color-swatch"><span style="background:rgb(${col[0]},${col[1]},${col[2]})"></span>标签 ${v}</div>`;
  }).join('');
}

// ─── UI ─────────────────────────────────────────────────
function syncSlider(){
  const max=getAxisMax(state.axis)-1;
  const sl=document.getElementById('slice');
  sl.max=max;
  if(state.slice>max)state.slice=Math.floor(max/2);
  sl.value=state.slice;
}
function setAxis(a){
  state.axis=a;
  ['axial','coronal','sagittal'].forEach(x=>document.getElementById('btn-'+x).classList.toggle('active',x===a));
  syncSlider(); render();
}
function setPreset(ww,wl){
  state.ww=ww;state.wl=wl;
  document.getElementById('ww').value=ww;document.getElementById('wl').value=wl;
  document.getElementById('ww-num').value=ww;document.getElementById('wl-num').value=wl;
  render();
}
function applySliceCount(){
  const n=parseInt(document.getElementById('total-slices').value)||64;
  resetVolume(n); state.slice=Math.floor(n/2); syncSlider(); render();
  document.getElementById('label-ctrl').style.display='none';
}
function bindPair(sid,nid,key){
  const sl=document.getElementById(sid),num=document.getElementById(nid);
  sl.addEventListener('input',()=>{state[key]=parseInt(sl.value);num.value=sl.value;render();});
  num.addEventListener('change',()=>{
    const v=Math.max(parseInt(num.min),Math.min(parseInt(num.max),parseInt(num.value)));
    state[key]=v;sl.value=v;num.value=v;render();
  });
}
bindPair('ww','ww-num','ww'); bindPair('wl','wl-num','wl');
document.getElementById('slice').addEventListener('input',e=>{state.slice=parseInt(e.target.value);render();});
document.getElementById('alpha').addEventListener('input',e=>{
  document.getElementById('alpha-val').textContent=e.target.value+'%'; render();
});

// ─── NIfTI 解析 ─────────────────────────────────────────
async function decompressGzip(buf){
  const ds=new DecompressionStream('gzip');
  const w=ds.writable.getWriter(),r=ds.readable.getReader();
  w.write(new Uint8Array(buf)); w.close();
  const chunks=[]; let total=0;
  while(true){const{done,value}=await r.read();if(done)break;chunks.push(value);total+=value.length;}
  const out=new Uint8Array(total); let off=0;
  for(const c of chunks){out.set(c,off);off+=c.length;}
  return out.buffer;
}
function parseNIfTI(buf){
  const dv=new DataView(buf);
  let sizeof_hdr=dv.getInt32(0,true);
  let le=true;
  if(sizeof_hdr!==348&&sizeof_hdr!==540){
    sizeof_hdr=dv.getInt32(0,false);
    if(sizeof_hdr===348||sizeof_hdr===540) le=false;
    else throw new Error('无效 NIfTI 头 sizeof_hdr='+sizeof_hdr);
  }
  const isNii2=(sizeof_hdr===540);
  let datatype,dims,vox_offset,scl_slope,scl_inter;
  if(!isNii2){
    datatype=dv.getInt16(70,le);
    const ndim=dv.getInt16(40,le); dims=[];
    for(let i=1;i<=Math.min(ndim,7);i++) dims.push(dv.getInt16(40+i*2,le));
    vox_offset=dv.getFloat32(108,le); if(vox_offset<352)vox_offset=352;
    scl_slope=dv.getFloat32(112,le); scl_inter=dv.getFloat32(116,le);
  } else {
    datatype=dv.getInt16(12,le);
    const ndim=dv.getInt32(16,le); dims=[];
    for(let i=1;i<=Math.min(ndim,7);i++) dims.push(Number(dv.getBigInt64(16+i*8,le)));
    vox_offset=Number(dv.getBigInt64(168,le));
    scl_slope=dv.getFloat64(176,le); scl_inter=dv.getFloat64(184,le);
  }
  const nx=dims[0]||1,ny=dims[1]||1,nz=dims[2]||1;
  if(nx<1||ny<1||nz<1) throw new Error('无效维度 '+nx+'×'+ny+'×'+nz);
  const offset=Math.round(vox_offset);
  const imgBuf=buf.slice(offset);
  const typeMap={2:Uint8Array,4:Int16Array,8:Int32Array,16:Float32Array,64:Float64Array,256:Int8Array,512:Uint16Array,768:Uint32Array};
  const T=typeMap[datatype]; if(!T) throw new Error('不支持 datatype='+datatype);
  const raw=new T(imgBuf,0,Math.min(nx*ny*nz, Math.floor(imgBuf.byteLength/T.BYTES_PER_ELEMENT)));
  const slope=(scl_slope===0||isNaN(scl_slope))?1:scl_slope;
  const inter=isNaN(scl_inter)?0:scl_inter;
  const vol=new Float32Array(nx*ny*nz);
  for(let i=0;i<vol.length;i++) vol[i]=raw[i]*slope+inter;
  return{vol,nx,ny,nz};
}
function autoWindow(vol){
  const step=Math.max(1,Math.floor(vol.length/10000));
  const s=[]; for(let i=0;i<vol.length;i+=step)s.push(vol[i]);
  s.sort((a,b)=>a-b);
  const p2=s[Math.floor(s.length*.02)],p98=s[Math.floor(s.length*.98)];
  return{ww:Math.max(1,Math.round(p98-p2)),wl:Math.round((p2+p98)/2)};
}

// ─── 上传处理 ────────────────────────────────────────────
async function handleUpload(input, kind){
  const file=input.files[0]; if(!file) return;
  const st=document.getElementById('status');
  st.className=''; st.textContent=`正在读取 ${kind==='img'?'影像':'标签'} (${Math.round(file.size/1024)}KB)...`;
  try{
    let buf=await file.arrayBuffer();
    const magic=new Uint8Array(buf,0,2);
    if(magic[0]===0x1f&&magic[1]===0x8b){
      st.textContent='解压 gzip...'; buf=await decompressGzip(buf);
    }
    const{vol,nx,ny,nz}=parseNIfTI(buf);
    if(kind==='img'){
      imgVol=vol; imgDims=[nx,ny,nz];
      state.slice=Math.floor(nz/2);
      document.getElementById('total-slices').value=nz;
      const{ww,wl}=autoWindow(vol); setPreset(ww,wl);
      document.getElementById('card-img').className='upload-card loaded';
      document.getElementById('name-img').innerHTML=`<span class="badge badge-img">已加载</span><br>${file.name}`;
      setAxis('axial');
      st.className='ok'; st.textContent=`影像已加载: ${nx}×${ny}×${nz}`;
    } else {
      lblVol=vol; lblDims=[nx,ny,nz];
      document.getElementById('card-lbl').className='upload-card loaded-label';
      document.getElementById('name-lbl').innerHTML=`<span class="badge badge-lbl">已加载</span><br>${file.name}`;
      document.getElementById('label-ctrl').style.display='block';
      updateLegend(); render();
      st.className='ok'; st.textContent=`标签已加载: ${nx}×${ny}×${nz}`;
    }
    render();
  } catch(e){
    st.className='error'; st.textContent='解析失败: '+e.message; console.error(e);
  }
  input.value='';
}

// ─── 保存功能 ────────────────────────────────────────────
function makeExportCanvas(sliceIdx, exportSZ, withOverlay){
  const c=document.createElement('canvas');
  c.width=exportSZ; c.height=exportSZ;
  const ec=c.getContext('2d');
  ec.fillStyle='#000'; ec.fillRect(0,0,exportSZ,exportSZ);
  renderToCanvas(ec, exportSZ, sliceIdx, withOverlay);
  return c;
}
function downloadCanvas(c, filename, fmt){
  const mime=fmt==='jpeg'?'image/jpeg':'image/png';
  const a=document.createElement('a');
  a.href=c.toDataURL(mime,0.95); a.download=filename; a.click();
}
function saveCurrent(){
  const fmt=document.getElementById('fmt').value;
  const sz=parseInt(document.getElementById('res').value);
  const ov=document.getElementById('overlay-opt').value==='1';
  const axisName=state.axis;
  const c=makeExportCanvas(state.slice, sz, ov);
  downloadCanvas(c, `slice_${axisName}_${state.slice+1}.${fmt}`, fmt);
}
async function saveBatch(){
  const fmt=document.getElementById('fmt').value;
  const sz=parseInt(document.getElementById('res').value);
  const ov=document.getElementById('overlay-opt').value==='1';
  const axisName=state.axis;
  const total=getAxisMax(state.axis);
  const prog=document.getElementById('batch-progress');

  // 动态加载 JSZip
  prog.textContent='加载 JSZip...';
  if(!window.JSZip){
    await new Promise((res,rej)=>{
      const s=document.createElement('script');
      s.src='https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js';
      s.onload=res; s.onerror=rej; document.head.appendChild(s);
    });
  }
  const zip=new JSZip();
  for(let i=0;i<total;i++){
    prog.textContent=`打包中 ${i+1}/${total}...`;
    const c=makeExportCanvas(i, sz, ov);
    const mime=fmt==='jpeg'?'image/jpeg':'image/png';
    const dataUrl=c.toDataURL(mime,0.95);
    const base64=dataUrl.split(',')[1];
    zip.file(`${axisName}_${String(i+1).padStart(4,'0')}.${fmt}`, base64, {base64:true});
    // 让 UI 喘口气
    if(i%5===0) await new Promise(r=>setTimeout(r,0));
  }
  prog.textContent='生成 zip...';
  const blob=await zip.generateAsync({type:'blob'});
  const url=URL.createObjectURL(blob);
  const a=document.createElement('a');
  a.href=url; a.download=`nifti_${axisName}_slices.zip`; a.click();
  URL.revokeObjectURL(url);
  prog.textContent=`✓ 已导出 ${total} 张`;
}

render();
</script>
</body>
</html>