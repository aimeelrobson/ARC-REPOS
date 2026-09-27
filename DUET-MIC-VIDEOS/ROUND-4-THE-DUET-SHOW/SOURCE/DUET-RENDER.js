const {chromium}=require('playwright-core');const fs=require('fs');const {execFileSync}=require('child_process');
const FF='/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2';
const mode=process.argv[2];const FPS=30;
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
 const pg=await b.newPage({viewport:{width:1080,height:1920}});
 await pg.goto('http://localhost:8777/index.html');await pg.waitForFunction('window.ready');
 const dur=await pg.evaluate('window.DUR');const dir='frames';fs.rmSync(dir,{recursive:true,force:true});fs.mkdirSync(dir);
 const times=mode==='preview'?(process.argv[3]||'0.1,0.9,1.5,2.5,3.6,4.5,5.4,6.6,8.6,9.8,10.35,11.9').split(',').map(Number):[...Array(Math.round(dur*FPS)).keys()].map(i=>i/FPS);
 for(let i=0;i<times.length;i++){await pg.evaluate(t=>seek(t),times[i]);await pg.screenshot({path:`${dir}/${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:93})}
 if(mode==='preview')execFileSync(FF,['-v','error','-y','-i',`${dir}/%04d.jpg`,'-vf',`scale=270:-1,tile=${times.length}x1`,'-frames:v','1','preview.jpg']);
 else execFileSync(FF,['-v','error','-y','-framerate',''+FPS,'-i',`${dir}/%04d.jpg`,'-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-preset','slow','-movflags','+faststart','out.mp4']);
 console.log('done');await b.close()})();
