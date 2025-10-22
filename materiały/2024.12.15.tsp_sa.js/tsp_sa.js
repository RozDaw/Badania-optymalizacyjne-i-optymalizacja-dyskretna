/*
  W programie są dwie zmienne:
    tspData: zmienna przechowywująca dane problemu
    logData: zmienna przechowywująca log z kolejnych kroków algorytmu
             obliczana jest 1 zaraz po wygenerowaniu nowej instancji,
             animacja itp leci już z <logData> nic nie liczy
  oraz klasy (zbiory statycznych funkcji)
    SA: klasa dostarcza <logData> dla algorytmu symulowanego wyżarzania
    CANVAS: klasa rysująca <logData> na stronie
    ACTION: klasa zawierająca metody interfejsu
*/

class TSPDATA
{ //dane tsp
  SetRand()
  { //ustawia losowo wierzchołki odległe od siebie o co najmniej 2
    let nodeN=40;
    this.nodes=[];
    for(let i=0;i<nodeN;)
    {
      let [x,y]=[Math.floor(Math.random()*100), Math.floor(Math.random()*50)]
      let ok=1;
      for(let i=0;i<this.nodes.length;i++)
      {
        let dx = (x-this.nodes[i].x);
        let dy = (y-this.nodes[i].y);
        if (dx*dx+dy*dy<4) ok=0;
      }
      if(ok==1){i++;this.nodes.push({x:x,y:y});}
    }
  }
  GetEdgeDist(a,b)
  { //podaje odleglość pomiędzy wierzchołkami o indeksach <a> i <b>
    let [dx,dy] = [this.nodes[a].x-this.nodes[b].x,
                   this.nodes[a].y-this.nodes[b].y];
    return Math.floor(0.5+Math.sqrt(dx*dx+dy*dy))
  }
  GetPathDist(path)
  { //podaje długość ścieżki <path>
    let length=0;
    for(let i=1;i<path.length;i++)
      length += this.GetEdgeDist( path[i-1],path[i] );
    return length;
  }
  GetNodeXY(id)
  { //podaje współrzędne wierzchoł
	  return{ x: 4*this.nodes[id].x, y:4*this.nodes[id].y }
  }
}

class SA
{ //algorytm symulowanego wyżarzania
  static GetLogRun(tsp)
  { //wykonuje algorytm SA: zwraca <log>
    let temp = 2000;                      // początkowa temperatura
    let path = SA.GetStartPath(tspData);  // początkowa ścieżka
    let dist = tsp.GetPathDist(path);     // długość początkowej scieżki
    let best = {dist:dist, path:path};    // najlepsze znalezione rozwiązanie
    let log  = [                          // log z pracy algorytmu
      {},                                 // log[0]: rysuje tylko dane tsp
      {dist:dist, path:path, temp:temp}]; // log[1]: tylko parametry startowe
    for(let n=0; n<400; n++)
    {
      temp = temp * 0.978;
      SA.SetLogStep( {log:log, tsp:tsp, best:best, temp:temp, stepN:100} );
    }
    best.temp = temp;
    log.push(best);
    return log;
  }
  static SetLogStep(input)
  { //wykonuje jeden etap algorytmu: modyfikuje <input.log, input.best>
    let path = Array.from( input.log[input.log.length-1].path )
    let c0 = input.tsp.GetPathDist(path);
    let praw=0,akce=0,delta=0;
    for(let i=0; i<input.stepN; i++)
    {
      let move = SA.GetRandAB(input.tsp.nodes.length);
      SA.SetPathMove( path, move );
      var c1 = input.tsp.GetPathDist(path);
      if(c1<input.best.dist){input.best.dist=c1;input.best.path=Array.from(path);}
      if(c1>c0)
      { delta=c1-c0;
        praw = Math.exp( (c0-c1)/input.temp );
        akce = ( Math.random()<praw );
      }
      if(c1<=c0||akce)  c0=c1; //akceptuje ruch
      else SA.SetPathMove( path,move ); //odrzucenie ruchu
    }
    input.log.push( {dist:c0,path:path,temp:input.temp,praw:praw,akce:akce,delta:delta} );
  }
  static GetStartPath(tsp)
  { //zwraca zinicjowanie algorytmu: <dist,path,temp>
    let path=[];
    for(let i=0;i<tsp.nodes.length;i++) path.push(i); path.push(0);
    return path;
  }
  static GetRandAB(size)
  { //losuje pare różnch liczb <A,B> z przedziału [1,size-1]
    var a=1+Math.floor(Math.random()*(size-1));
    var b=1+Math.floor(Math.random()*(size-2)); if(b>=a)b++;
    if(a>b) [a,b]=[b,a];
    return [a,b];
  }
  static SetPathMove(path,move)
  { //dokonuje zamiany <move> na ścieżce <path>
    var a=move[0], b=move[1];
    while(a<b){[path[a],path[b]]=[path[b],path[a]]; a++;b--;}
  }
}

class CANVAS
{ // wyświetlanie przy pomocy Canvas //
  static Init()
  { //ustawia parametry canvasów
    let width = 440
    let height = 240;
    let devicePixelRatio = window.devicePixelRatio || 1;
    for(let i=0;i<6;i++ )
    { let can = ['canPath','canDist','canPraw','canTemp','canDelta','canPWykres'][i];
      let canvas = document.getElementById(can);
      let ctx = canvas.getContext("2d");
      canvas.width  =  width * devicePixelRatio;
      canvas.height =  height * devicePixelRatio;
      canvas.style.width  = width + 'px';
      canvas.style.height = height + 'px';
      ctx.scale(devicePixelRatio, devicePixelRatio)
    }
  }
  static Update(frame)
  { //odswieża canvasy
    CANVAS.DrawPath( frame )
    CANVAS.DrawDist( frame )
    CANVAS.DrawPraw( frame )
    CANVAS.DrawTemp( frame )
    CANVAS.DrawDelta( frame )
    CANVAS.DrawPWykres( frame )
  }
  static DrawPath(frame)
  { //rysuje na canvas
    let canvas = document.getElementById('canPath');
    let ctx = canvas.getContext("2d");
    let path = logData[frame].path;
    //siatka
    CANVAS.#CtxDrawBackground(ctx);
    //sciezka
    if(path)
    {
      ctx.beginPath();
      ctx.strokeStyle = '#aa7'
      ctx.lineWidth = '3'
      ctx.lineJoin = "round";
      for(let i=0; i<path.length; i++)
      {
        let axy = tspData.GetNodeXY( path[i] );
        let [eX,eY] = [20.5+axy.x, 20.5+axy.y]
        if(i==0) ctx.moveTo(eX,eY)
        else ctx.lineTo(eX,eY)
      }
      ctx.stroke();
    }
    //węzły
    ctx.fillStyle = '#474';
    ctx.lineWidth = '1'
    for(let i=0;i<tspData.nodes.length;i++)
    {
      ctx.beginPath();
      let xy = tspData.GetNodeXY(i);
      let [eX,eY] =[20+xy.x, 20+xy.y]
      ctx.arc(eX,eY,4,0,6.3);ctx.fill();
    }
  }
  static DrawDist(frame)
  { //rysuje na canvas
    let canvas = document.getElementById('canDist');
    let ctx = canvas.getContext("2d");
    //siatka
    CANVAS.#CtxDrawBackground(ctx,'osie');
    if(logData[frame].dist==undefined)return;
    //sciezka
    ctx.beginPath();
    ctx.strokeStyle = '#aa7'
    ctx.lineWidth = '2'
    ctx.lineJoin = "round";
    ctx.moveTo(20,60)
    let scala = 160/logData[1].dist;
    for(let i=1;i<=frame;i++)
      ctx.lineTo(20+i,220-scala*logData[i].dist)
    ctx.stroke();
    ctx.textAlign = "right";
    ctx.font = "16px Courier";ctx.fillStyle = '#666'
    ctx.fillText( 'dist='+logData[frame].dist,400,35);
  }
  static DrawPraw(frame)
  { //rysuje na canvas
    let canvas = document.getElementById('canPraw');
    let ctx = canvas.getContext("2d");
    //siatka
    CANVAS.#CtxDrawBackground(ctx,'osie');
    ctx.beginPath();
    for(let i=1;i<=frame;i++)
    {
      if(logData[i].akce) ctx.fillStyle = '#474';
      else ctx.fillStyle= '#b66';
      ctx.beginPath();
      let r=2; if(i==frame) r=6;
      ctx.arc(20+i,220-200*logData[i].praw,r,0,6.3);
      ctx.fill();
    }
    ctx.textAlign = "right";
    ctx.font = "16px Courier";ctx.fillStyle = '#666'
    if(logData[frame].praw!=undefined)
      ctx.fillText( 'P='+logData[frame].praw.toFixed(3),400,35);
  }
  static DrawTemp(frame)
  { //rysuje na canvas
    let canvas = document.getElementById('canTemp');
    let ctx = canvas.getContext("2d");
    //siatka
    CANVAS.#CtxDrawBackground(ctx,'osie');
    //sciezka
    ctx.beginPath();
    ctx.strokeStyle = '#aa7'
    ctx.lineWidth = '2'
    ctx.moveTo(20,20)
    let scala = 200/logData[1].temp;
    for(let i=1;i<=frame;i++)
      ctx.lineTo(20+i,220-scala*logData[i].temp)
    ctx.stroke();
    ctx.textAlign = "right";
    ctx.font = "16px Courier";ctx.fillStyle = '#666'
    if(logData[frame].temp)
      ctx.fillText( 't='+logData[frame].temp.toPrecision(4).substring(0,5),400,35);
  }
  static DrawDelta(frame)
  { //rysuje na canvas
    let canvas = document.getElementById('canDelta');
    let ctx = canvas.getContext("2d");
    //siatka
    CANVAS.#CtxDrawBackground(ctx,'osie');
    ctx.beginPath();
    for(let i=1;i<=frame;i++)
    {
      if(logData[i].akce) ctx.fillStyle = '#474';
      else ctx.fillStyle= '#b66';
      ctx.beginPath();
      let delta = 2*logData[i].delta;
      if(delta>400) delta=410;
      let r=2; if(i==frame) r=6;
      ctx.arc(20+delta,220-i/2,r,0,6.3);
      ctx.fill();
    }
    ctx.textAlign = "right";
    ctx.font = "16px Courier";ctx.fillStyle = '#666'
    if(logData[frame].delta)
      ctx.fillText( 'd='+logData[frame].delta,400,35);
  }
  static DrawPWykres(frame)
  { //rysuje na canvas
    let canvas = document.getElementById('canPWykres');
    let ctx = canvas.getContext("2d");
    //siatka
    CANVAS.#CtxDrawBackground(ctx,'osie');
    if(logData[frame].temp==undefined)return;
    //wykres
    let temp=logData[frame].temp;
    ctx.beginPath();
    ctx.strokeStyle = '#aa7'
    ctx.lineWidth = '2'
    ctx.moveTo(20,20)
    for(let i=1;i<=200;i++)
    { let y=Math.exp(-i/temp)
      ctx.lineTo(20+2*i,220-y*200)
    }
    ctx.stroke();
    //punkt
    let delta = 2*logData[frame].delta;
    if(delta>400) delta=410;
    let prawd = logData[frame].praw

    ctx.font = "16px Courier";
    ctx.textAlign = "right";
    ctx.fillStyle = '#666';
    if(logData[frame].temp)
    { ctx.fillText( 't=',340,35);
      ctx.textAlign = "right";
      ctx.fillText( temp.toPrecision(4).substring(0,5) ,400,35);
    }
    if(logData[frame].delta)
    { ctx.fillText( 'd=',340,50);
      ctx.textAlign = "right";
      ctx.fillText( logData[frame].delta,400,50);
    }
    if(logData[frame].praw!=undefined)
    { ctx.fillText( 'P=',340,65);
      ctx.textAlign = "right";
      ctx.fillText( prawd.toFixed(3),400,65);
    }
    if(praw&&delta)
    { if(logData[frame].akce) ctx.fillStyle = '#474';
      else ctx.fillStyle= '#b66';
      ctx.beginPath();
      ctx.arc(20+delta,220-200*prawd,6,0,6.3);
      ctx.fill();
    }

  }
  static #CtxDrawGrid(ctx,grid)
  { //rysuje siatke na <ctx>, parametry siatki to <grid>
    ctx.beginPath();
    for(let a=0;a<=grid.nX;a++)
    { let x=0.5+grid.marginX+grid.sizeX*a/grid.nX;
      let y0=0.5+grid.marginY-grid.rY;
      let y1=0.5+grid.marginY+grid.sizeY+grid.rY
      ctx.moveTo(x,y0); ctx.lineTo(x,y1);
    }
    for(let b=0;b<=grid.nY;b++)
    { let y=0.5+grid.marginY+grid.sizeY*b/grid.nY;
      let x0=0.5+grid.marginX-grid.rX;
      let x1=0.5+grid.marginX+grid.sizeX+grid.rX;
      ctx.moveTo(x0,y); ctx.lineTo(x1,y);
    }
    ctx.stroke();
  }
  static #CtxDrawBackground(ctx,type)
  { //rysuje tlo pod rysunki (3xsiatka+osie)
    ctx.beginPath();
    ctx.fillStyle = "#211";
    ctx.fillRect(0,0,440,240);
    ctx.fill();
    ctx.strokeStyle = '#251515'; ctx.lineWidth = '1';
    CANVAS.#CtxDrawGrid(ctx,{marginX:20,marginY:20,sizeX:400,sizeY:200,nX:100,nY:50,rX:8,rY:8});
    ctx.strokeStyle = '#281818'; ctx.lineWidth = '1';
    CANVAS.#CtxDrawGrid(ctx,{marginX:20,marginY:20,sizeX:400,sizeY:200,nX:20,nY:10,rX:8,rY:8});
    ctx.strokeStyle = '#2a1a1a'; ctx.lineWidth = '1';
    CANVAS.#CtxDrawGrid(ctx,{marginX:20,marginY:20,sizeX:400,sizeY:200,nX:10,nY:5,rX:10,rY:10});
    if(type=='osie')
    {
      ctx.beginPath();
      ctx.strokeStyle = '#433'; ctx.lineWidth = '1';
      ctx.moveTo(20,10);ctx.lineTo(20,230);
      ctx.moveTo(10,220);ctx.lineTo(430,220);
      ctx.stroke();
    }
  }
}

class ACTION
{ // zbiór funkcji: wywoływanych po kliknięciu //
  //
  static ClickRand()
  {
    clearTimeout(timer);
    tspData.SetRand();
    slider.value='0';
    slider.max='0';
    CANVAS.Update(0);
  }
  //
  static ClickSA()
  {
    clearTimeout(timer);
    logData = SA.GetLogRun( tspData );
    slider.max= logData.length-1;
    slider.value='0';
    ACTION.Loop();
  }
  //
  static ClickReport()
  {
    //data
    let text = 'data:\n'
    text += tspData.nodes.length+'\n';
    for(let i=0; i<tspData.nodes.length; i++)
    { text += tspData.nodes[i].x.toString().padStart(2,' ')+' '
            + tspData.nodes[i].y.toString().padStart(2,' ')+'   ';
    }
    text += '\n';
    //path
    text += '\nstep : length : path\n'
    for(let n=1; n<logData.length; n++)
    {
      let dist = logData[n].dist;
      let path = logData[n].path;
      text += n.toString().padStart(4,' ')+' : '
              +dist.toString().padStart(6,' ')+' : ';
      for(let i=0; i<path.length; i++)
      text += path[i]+' ';
      text += ' \n';
    }
    ACTION.NewWindowData(text);
  }
  //
  static ClickSlider(value)
  {
    clearTimeout(timer);
    value = parseInt(value)
    CANVAS.Update(value)
  }
  //
  static Loop()
  {
    let frame = parseInt(slider.value)
    if(frame==slider.max)
      CANVAS.Update(frame);
    if(frame<slider.max)
    {
      frame +=1;
      slider.value = frame;
      CANVAS.Update(frame);
      if(frame<slider.max)
       timer=setTimeout(ACTION.Loop,20 );
    }
  }
  //
  static NewWindowData(data)
  { var blob = new Blob([data], {type:"text/plain"});
    var url = URL.createObjectURL(blob);
    var link = document.createElement("a");
    link.href = url;
    window.open(link)
    URL.revokeObjectURL(url);
  }
  //
  static Key(key)
  {
    var el = document.getElementById('txtA');
    if(key.code=="ArrowRight")
    {
      let frame = parseInt(slider.value)+1;
      if(frame<logData.length)
      { slider.value = frame;
        CANVAS.Update(frame);
      }
    }
    if(key.code=="ArrowLeft")
    {
      let frame = parseInt(slider.value)-1;
      if(frame>=0)
      { slider.value = frame;
        CANVAS.Update(frame);
      }
    }
  }
}

{ // MAIN: funkcja uruchamiana przy starcie strony //
  timer=0;
  tspData=new TSPDATA()
  tspData.SetRand();
  logData=[]
  document.onselectstart = function(){return false;};
  document.getElementById('btnRand'  ).addEventListener('click',ACTION.ClickRand);
  document.getElementById('btnSA'    ).addEventListener('click',ACTION.ClickSA );
  document.getElementById('btnReport').addEventListener('click',ACTION.ClickReport);
  document.addEventListener("keydown", ACTION.Key);
  var slider = document.getElementById("slider");
  slider.oninput = function(){ACTION.ClickSlider(this.value);}
  CANVAS.Init();
  ACTION.ClickSA();
}
