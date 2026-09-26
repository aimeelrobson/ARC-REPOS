const {chromium}=require('playwright-core');const fs=require('fs');const {execFileSync}=require('child_process');
const FF='/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2';
const [mode,...vs]=process.argv.slice(2);const FPS=30;
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
 const pg=await b.newPage({viewport:{width:1080,height:1920}});
 for(const v of vs){await pg.goto('http://localhost:8766/index.html?v='+v);await pg.waitForFunction('window.ready');
  const dir=`fr${v}`;fs.rmSync(dir,{recursive:true,force:true});fs.mkdirSync(dir);
  const times=mode==='preview'?[.3,.9,1.5,2.1,2.7,3.3,3.9,4.8]:[...Array(5*FPS).keys()].map(i=>i/FPS);
  for(let i=0;i<times.length;i++){await pg.evaluate(t=>seek(t),times[i]);await pg.screenshot({path:`${dir}/${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:93})}
  if(mode==='preview')execFileSync(FF,['-v','error','-y','-i',`${dir}/%04d.jpg`,'-vf','scale=270:-1,tile=8x1','-frames:v','1',`prev${v}.jpg`]);
  else execFileSync(FF,['-v','error','-y','-framerate',''+FPS,'-i',`${dir}/%04d.jpg`,'-c:v','libx264','-pix_fmt','yuv420p','-crf','17','-preset','slow','-movflags','+faststart',`out${v}.mp4`]);
  console.log('done',v)}
 await b.close()})();
